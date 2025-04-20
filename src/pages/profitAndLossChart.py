import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title(":heavy_dollar_sign: Profit and Loss Charts")

data = None
with open('./json/profitAndLoss.json', 'r') as file:
    data = json.load(file)

def show_income_vs_expenses(pl_json):
    """Compare Total Income vs Total Expenses for Current & Prior years."""
    data = [
        {"Category": "Total Income",   "Year": "Current", "Amount": pl_json["total_income"]["current"]},
        {"Category": "Total Income",   "Year": "Prior",   "Amount": pl_json["total_income"]["prior"]},
        {"Category": "Total Expenses", "Year": "Current", "Amount": pl_json["total_expenses"]["current"]},
        {"Category": "Total Expenses", "Year": "Prior",   "Amount": pl_json["total_expenses"]["prior"]},
    ]
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x="Category",
        y="Amount",
        color="Year",
        barmode="group",
        title="Income vs Expenses"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_profit_trends(pl_json):
    """Side‑by‑side bars for Profit Before Tax & Net Profit After Tax."""
    rows = []
    for period, label in [( "current","Current"), ("prior","Prior")]:
        rows.append({
            "Period": label,
            "Profit Before Tax": pl_json["profit_before_tax"][period],
            "Net Profit After Tax": pl_json["net_profit_after_tax"][period]
        })
    df = pd.DataFrame(rows)
    fig = px.bar(
        df,
        x="Period",
        y=["Profit Before Tax", "Net Profit After Tax"],
        barmode="group",
        title="PBT & Net Profit Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_tax_breakdown(pl_json):
    """Grouped bars showing Current vs Deferred vs Total tax expense."""
    tax = pl_json["tax_expense"]
    data = []
    for period, label in [("current","Current"), ("prior","Prior")]:
        data += [
            {"Type": "Current Tax",  "Year": label, "Amount": tax["current_tax"][period]},
            {"Type": "Deferred Tax", "Year": label, "Amount": tax["deferred_tax"][period]},
            {"Type": "Total Tax",    "Year": label, "Amount": tax["total_tax"][period]},
        ]
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x="Type",
        y="Amount",
        color="Year",
        barmode="group",
        title="Tax Expense Breakdown"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_comprehensive_income(pl_json):
    """Stacked bars for components of Other Comprehensive Income and total OCI."""
    oci = pl_json["other_comprehensive_income"]
    data = []
    for period, label in [("current","Current"), ("prior","Prior")]:
        data += [
            {"Component": "Not Reclassified", "Year": label, "Amount": oci["not_reclassified"][period]},
            {"Component": "Reclassified",     "Year": label, "Amount": oci["reclassified"][period]},
            {"Component": "Total OCI",         "Year": label, "Amount": oci["total_oci"][period]},
        ]
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x="Component",
        y="Amount",
        color="Year",
        barmode="stack",
        title="Other Comprehensive Income"
    )
    st.plotly_chart(fig, use_container_width=True)


def show_eps(pl_json):
    """Grouped bars for Basic vs Diluted Earnings Per Share."""
    eps = pl_json["earnings_per_share"]
    data = [
        {"Type": "Basic EPS",   "Year": "Current", "Value": eps["basic"]["current"]},
        {"Type": "Basic EPS",   "Year": "Prior",   "Value": eps["basic"]["prior"]},
        {"Type": "Diluted EPS", "Year": "Current", "Value": eps["diluted"]["current"]},
        {"Type": "Diluted EPS", "Year": "Prior",   "Value": eps["diluted"]["prior"]},
    ]
    df = pd.DataFrame(data)
    fig = px.bar(
        df,
        x="Type",
        y="Value",
        color="Year",
        barmode="group",
        title="Earnings Per Share"
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.subheader("📈 Profit & Loss Statement")
    pls = data["profit_and_loss_statement"]
    st.caption(f'Periods ending {pls["period_ends"]["prior_year"]} vs {pls["period_ends"]["current_year"]}')
    show_income_vs_expenses(pls)
    show_profit_trends(pls)
    show_tax_breakdown(pls)
    show_comprehensive_income(pls)
    show_eps(pls)

main()