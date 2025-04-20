import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title(":money_with_wings: Current Investments")

data = None 
with open("./json/currentInvestments.json") as file:
    data = json.load(file)

def show_amortized_cost_sunburst(ci):
    """
    Sunburst of Amortized Cost → Quoted vs Unquoted → Instruments (2024 values).
    """
    rows = []
    acc = ci["measured_at_amortized_cost"]
    for qual in ("quoted","unquoted"):
        for itm in acc.get(qual, []):
            rows.append({
                "Level 1": "Amortized Cost",
                "Level 2": qual.title(),
                "Instrument": itm["instrument"],
                "Value": itm["2024"]
            })
    df = pd.DataFrame(rows)
    fig = px.sunburst(
        df,
        path=["Level 1","Level 2","Instrument"],
        values="Value",
        title="Amortized Cost Investments (2024)",
        hover_data={"Value":":,d"}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_amortized_cost_comparison(ci):
    """
    Grouped bar comparing each Amortized Cost instrument: 2023 vs 2024.
    """
    rows = []
    acc = ci["measured_at_amortized_cost"]
    for qual in ("quoted","unquoted"):
        for itm in acc.get(qual, []):
            rows.append({
                "Instrument": itm["instrument"],
                "Category": qual.title(),
                "Year": "2023",
                "Amount": itm["2023"]
            })
            rows.append({
                "Instrument": itm["instrument"],
                "Category": qual.title(),
                "Year": "2024",
                "Amount": itm["2024"]
            })
    df = pd.DataFrame(rows)
    fig = px.bar(
        df,
        x="Instrument",
        y="Amount",
        color="Year",
        facet_col="Category",
        barmode="group",
        title="Amortized Cost: Quoted vs Unquoted (’23 vs ’24)"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_fvtpl_investments(ci):
    """
    Simple bar for FVTPL investments (only Mutual Funds here).
    """
    fvtpl = ci["measured_at_fvtpl"].get("quoted", [])
    df = pd.DataFrame([
        {"Instrument": itm["instrument"], "2023": itm["2023"], "2024": itm["2024"]}
        for itm in fvtpl
    ]).melt(id_vars="Instrument", value_name="Amount", var_name="Year")
    fig = px.bar(
        df,
        x="Instrument",
        y="Amount",
        color="Year",
        barmode="group",
        title="FVTPL Investments (’23 vs ’24)"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_totals(ci):
    """
    Single bar chart of Total Current Investments ’23 vs ’24.
    """
    tot = ci["totals"]["total_current_investments"]
    df = pd.DataFrame([
        {"Year": "2023", "Amount": tot["2023"]},
        {"Year": "2024", "Amount": tot["2024"]},
    ])
    fig = px.bar(
        df,
        x="Year",
        y="Amount",
        color="Year",
        text="Amount",
        title="Total Current Investments",
        labels={"Amount":"₹ Crores"}
    )
    fig.update_traces(textposition="outside", texttemplate="%{text:,}")
    st.plotly_chart(fig, use_container_width=True)

def show_other_disclosures(ci):
    """
    Grouped bar for the three “other_disclosures” metrics across years.
    """
    od = ci["other_disclosures"]
    rows = []
    for key, label in [
        ("aggregate_amount_quoted_investments", "Agg. Quoted"),
        ("market_value_quoted_investments",   "Market Value Quoted"),
        ("aggregate_amount_unquoted_investments","Agg. Unquoted"),
    ]:
        for year in ("2023","2024"):
            rows.append({
                "Metric": label,
                "Year": year,
                "Amount": od[key][year]
            })
    df = pd.DataFrame(rows)
    fig = px.bar(
        df,
        x="Metric",
        y="Amount",
        color="Year",
        barmode="group",
        title="Other Disclosures (₹ Crores)"
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.subheader("💼 Current Investments")
    show_amortized_cost_sunburst(data["current_investments"])
    st.divider()
    show_amortized_cost_comparison(data["current_investments"])
    st.divider()
    show_fvtpl_investments(data["current_investments"])
    st.divider()
    show_totals(data["current_investments"])
    st.divider()
    show_other_disclosures(data["current_investments"])

main()