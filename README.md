# SmartSetu-AI

SmartSetu-AI is a Streamlit-based dashboard for automated vendor credit and risk scoring. It enables organizations to objectively assess vendors using data-driven models, interactive analytics, and loan eligibility simulation, all powered by seamless Google Sheets integration.

## Features

- **Google Sheets Integration**: Fetches and updates vendor data directly from a connected Google Sheet.
- **Automated Scoring**: Calculates credit and risk scores using transaction history, consistency, supplier verification, testimonials, income, and expenses.
- **Loan Eligibility Simulator**: Determines loan eligibility and simulates EMI and repayment schedules for vendors.
- **Visual Analytics**: Interactive bar charts and scatter plots for comparing vendor credit and risk scores.
- **Downloadable Reports**: Export individual or all vendor reports in CSV format.
- **User-Friendly Web Interface**: Rapid deployment via Streamlit.

## How It Works

1. **Connects to Google Sheets** to fetch vendor data.
2. **Calculates Credit Score** using:
   - Monthly Transactions
   - Consistency Score
   - Supplier Verification Status
   - Customer Testimonials
3. **Calculates Risk Score** based on income and spending variance.
4. **Determines Risk Level** (Low, Medium, High).
5. **Loan Eligibility**: Offers tailored loan amounts and interest rates based on credit score.
6. **Visualization**: Presents all vendor scores and offers interactive data exploration.

## Getting Started

### Prerequisites

- Python 3.8+
- Google Cloud Service Account with Google Sheets API access
- Required columns in Google Sheet:
    - Name of Vendor
    - Monthly Transactions
    - Consistency Score
    - Supplier Verified
    - Customer Testimonial
    - Monthly Income - Month 1/2/3
    - Spending Variance - Month 1/2/3

### Installation

```bash
git clone https://github.com/xthxr/SmartSetu-AI.git
cd SmartSetu-AI
pip install -r requirements.txt
```

### Google Sheets Credentials

- Place your service account credentials as `credentials.json` in the root directory, **or**
- Set the environment variable `GOOGLE_CREDENTIALS_JSON` with your credentials JSON.

### Running the App

```bash
streamlit run app.py
```

By default, the Google Sheet key is set in `app.py` with the variable `SHEET_KEY`. Update it if your data source changes.

## File Structure

- `app.py` - Main Streamlit dashboard.
- `calculator.py` - Scoring logic (credit, risk, risk level).
- `data_fetch.py` - Google Sheets API integration.
- `requirements.txt` - Python dependencies.
- `assets/` - App logo and static assets.

## Example

![Dashboard Screenshot](https://raw.githubusercontent.com/mrashis06/SmartSetu-AI/main/assets/logo.png)

## Customization

- Adjust scoring logic in `calculator.py` to match your business criteria.
- Add new analytics or visualizations in `app.py` as required.

## License

[Specify your license here]

## Acknowledgements

- Inspired by original work from [mrashis06/SmartSetu-AI](https://github.com/mrashis06/SmartSetu-AI)
- [Streamlit](https://streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)

---

_This project helps automate and standardize vendor creditworthiness assessment using modern data analytics and is suitable for fintech, supply chain, and procurement scenarios._
