import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_fetch import fetch_vendor_data
from calculator import calculate_credit_score, calculate_risk_score, get_risk_level

# Google Sheet Key
SHEET_KEY = "1ccQAGRSCcJbJijorbBzSwU-wx60Ftf-2lzayKzCZQRw"

st.set_page_config(page_title="SmartSetu-AI", layout="wide")
st.title("SmartSetu-AI - Vendor Credit & Risk Scoring Dashboard")

# Fetch vendor data
df = fetch_vendor_data(SHEET_KEY)

if df.empty:
    st.warning("No vendor data found in the connected Google Sheet.")
    st.stop()

# Calculate scores for each vendor
scores = []
max_txn = df["Monthly Transactions"].max()

for index, row in df.iterrows():
    try:
        transactions = float(row['Monthly Transactions'])
        consistency = float(row['Consistency Score'])
        supplier_verified = row['Supplier Verified']
        testimonials = float(row['Customer Testimonial'])
        income1 = float(row['Monthly Income - Month 1'])
        income2 = float(row['Monthly Income - Month 2'])
        income3 = float(row['Monthly Income - Month 3'])
        avg_income = (income1 + income2 + income3) / 3
        expenses = [
            float(row['Spending Variance - Month 1']),
            float(row['Spending Variance - Month 2']),
            float(row['Spending Variance - Month 3']),
        ]

        credit_score = calculate_credit_score(transactions, consistency, supplier_verified, testimonials, max_txn)
        risk_score = calculate_risk_score(expenses, avg_income)
        risk_level = get_risk_level(risk_score)

        scores.append({
            "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
            "Credit Score": credit_score,
            "Risk Score": risk_score,
            "Risk Level": risk_level
        })

    except Exception as e:
        st.error(f"Error processing row {index + 1}: {e}")
        scores.append({
            "Vendor": row.get("Name of Vendor", f"Vendor {index+1}"),
            "Credit Score": "Error",
            "Risk Score": "Error",
            "Risk Level": f"{type(e).__name__}: {str(e)}"
        })

# Final DataFrame with scores
score_df = pd.DataFrame(scores)

# --- Sidebar: View Mode ---
device_mode = st.sidebar.radio("Select View Mode:", ["Desktop", "Mobile"])
fig_width, fig_height, rotation = (12, 6, 45) if device_mode == "Desktop" else (6, 4, 30)

# --- Sidebar: Vendor Selection ---
st.sidebar.title("Vendor Report Access")
search_query = st.sidebar.text_input("Search Vendor Name").strip().lower()
filtered_vendors = (
    [v for v in score_df["Vendor"] if search_query in v.lower()] if search_query else score_df["Vendor"].tolist()
)

if not filtered_vendors:
    st.sidebar.warning("No matching vendor found.")
    filtered_vendors = score_df["Vendor"].tolist()

selected_vendor = st.sidebar.selectbox("Choose a Vendor:", filtered_vendors)

# Display selected vendor details
selected_row = score_df[score_df["Vendor"] == selected_vendor].iloc[0]
st.sidebar.markdown("### Vendor Score Report")
st.sidebar.metric("Credit Score", selected_row["Credit Score"])
st.sidebar.metric("Risk Score", selected_row["Risk Score"])
st.sidebar.metric("Risk Level", selected_row["Risk Level"])

# Download CSV for selected vendor
vendor_row_df = pd.DataFrame([selected_row])
csv_data = vendor_row_df.to_csv(index=False).encode('utf-8')
file_name = f"{selected_vendor.replace(' ', '_')}_report.csv"
st.sidebar.download_button("Download My Report", data=csv_data, file_name=file_name, mime="text/csv")

# --- Main: All Vendor Scores Table ---
st.subheader("All Vendor Scores")
st.dataframe(score_df, use_container_width=True)

# --- Main: Chart Type Selection ---
st.subheader("Visualize Scores")
chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Scatter Plot"])

if chart_type == "Bar Chart":
    st.markdown("### Bar Chart: Credit vs Risk Score")
    top_n = st.slider("Select number of vendors to display", min_value=5, max_value=len(score_df), value=10, step=5)
    score_df_plot = score_df.sort_values("Credit Score", ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(max(10, top_n * 0.6), fig_height))
    x = range(len(score_df_plot))
    bar_width = 0.35

    credit_pos = [i - bar_width/2 for i in x]
    risk_pos = [i + bar_width/2 for i in x]

    ax.bar(credit_pos, score_df_plot["Credit Score"], width=bar_width, label="Credit Score", color="royalblue")
    ax.bar(risk_pos, score_df_plot["Risk Score"], width=bar_width, label="Risk Score", color="salmon")
    ax.set_xticks(x)
    ax.set_xticklabels(score_df_plot["Vendor"], rotation=rotation, ha="right")
    ax.set_ylabel("Score (0-100)")
    ax.set_title(f"Credit vs Risk Score for Top {top_n} Vendors")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)

elif chart_type == "Scatter Plot":
    st.markdown("### Scatter Plot: Credit vs Risk Score")
    fig2, ax2 = plt.subplots(figsize=(fig_width, fig_height))
    ax2.scatter(score_df["Credit Score"], score_df["Risk Score"], c="purple", s=100)

    for i, row in score_df.iterrows():
        ax2.text(row["Credit Score"] + 0.5, row["Risk Score"] + 0.5, row["Vendor"], fontsize=8)

    ax2.set_xlabel("Credit Score")
    ax2.set_ylabel("Risk Score")
    ax2.set_title("Credit Score vs Risk Score Scatter Plot")
    ax2.grid(True, linestyle="--", alpha=0.6)

    st.pyplot(fig2)

# --- Full CSV Download ---
st.subheader("Download All Vendor Data")
full_csv = score_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Full Vendor Scores as CSV", full_csv, "vendor_scores.csv", "text/csv")
