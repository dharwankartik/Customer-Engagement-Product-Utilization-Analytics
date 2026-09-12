import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Engagement Analytics",
    layout="wide"
)

df = pd.read_csv("../Data/customer_engagement_analysis.csv")

st.title("Customer Engagement & Product Utilization Analytics")
st.write("Retention Strategy Dashboard")

st.sidebar.header("Filters")

engagement_filter = st.sidebar.multiselect(
    "Engagement Profile",
    options=df["EngagementProfile"].unique(),
    default=df["EngagementProfile"].unique()
)

filtered_df = df[df["EngagementProfile"].isin(engagement_filter)]

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Churned Customers", int(filtered_df["Exited"].sum()))
col3.metric(
    "Churn Rate",
    f"{filtered_df['Exited'].mean() * 100:.2f}%"
)

st.subheader("Engagement vs Churn")

engagement_churn = (
    filtered_df.groupby("IsActiveMember")["Exited"]
    .mean()
    .mul(100)
    .reset_index()
)

engagement_churn["Engagement"] = engagement_churn["IsActiveMember"].map({
    0: "Inactive",
    1: "Active"
})

st.bar_chart(
    engagement_churn.set_index("Engagement")["Exited"]
)

st.subheader("Product Utilization Impact")

product_churn = (
    filtered_df.groupby("NumOfProducts")["Exited"]
    .mean()
    .mul(100)
    .reset_index()
)

st.bar_chart(
    product_churn.set_index("NumOfProducts")["Exited"]
)

st.write("Churn rate by number of products used.")


st.subheader("High-Value Disengaged Customers")

balance_limit = st.sidebar.number_input(
    "Minimum Balance",
    min_value=0,
    value=50000,
    step=10000
)

high_value_customers = filtered_df[
    (filtered_df["IsActiveMember"] == 0) &
    (filtered_df["Balance"] >= balance_limit)
]

col1, col2 = st.columns(2)

col1.metric(
    "High-Value Disengaged Customers",
    len(high_value_customers)
)

col2.metric(
    "Their Churn Rate",
    f"{high_value_customers['Exited'].mean() * 100:.2f}%"
)

st.dataframe(
    high_value_customers[
        ["CustomerId", "Geography", "Balance",
         "NumOfProducts", "IsActiveMember", "Exited"]
    ].head(20)
)



st.subheader("Retention Strength Analysis")

tier_churn = (
    filtered_df.groupby("RelationshipTier")["Exited"]
    .mean()
    .mul(100)
    .reset_index()
)

st.bar_chart(
    tier_churn.set_index("RelationshipTier")["Exited"]
)

st.write("Churn rate across relationship strength tiers.")

