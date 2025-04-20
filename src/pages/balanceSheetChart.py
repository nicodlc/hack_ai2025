import json
import streamlit as st
import plotly.express as px
import pandas as pd

data = None
with open('./json/balanceSheet.json', 'r') as file:
    data = json.load(file)

def show_non_current_assets(bs_json):
    # normalize items + subitems
    nc = bs_json["financial_position"]["assets"]["non_current"]
    rows = []
    for item in nc["items"]:
        if "subitems" in item:
            for sub in item["subitems"]:
                rows.append({
                    "parent": item["name"],
                    "name":   sub["name"],
                    "value":  sub["2024"]
                })
        else:
            rows.append({
                "parent": "Non-current Assets",
                "name":   item["name"],
                "value":  item["2024"]
            })
    rows.append({
        "parent": "",
        "name": "Non-current Assets",
        "value": nc["total_non_current_assets"]["2024"]
    })
    df = pd.DataFrame(rows)
    fig = px.sunburst(
        df,
        path=["parent","name"],
        values="value",
        title="Non‑Current Assets (2024)",
        hover_data={"value":True}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_current_assets(bs_json):
    cur = bs_json["financial_position"]["assets"]["current"]
    rows = []
    for item in cur["items"]:
        if "subitems" in item:
            for sub in item["subitems"]:
                rows.append({
                    "parent": item["name"],
                    "name":   sub["name"],
                    "value":  sub["2024"]
                })
        else:
            rows.append({
                "parent": "Current Assets",
                "name":   item["name"],
                "value":  item["2024"] or 0
            })
    rows.append({
        "parent": "",
        "name": "Current Assets",
        "value": cur["total_current_assets"]["2024"]
    })
    df = pd.DataFrame(rows)
    fig = px.treemap(
        df,
        path=["parent","name"],
        values="value",
        title="Current Assets (2024)",
        hover_data={"value":True}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_assets_totals(bs_json):
    nc_tot = bs_json["financial_position"]["assets"]["non_current"]["total_non_current_assets"]
    c_tot  = bs_json["financial_position"]["assets"]["current"]["total_current_assets"]
    df = pd.DataFrame({
        "Category": ["Non-current","Non-current","Current","Current"],
        "Year":     ["2023","2024","2023","2024"],
        "Value":    [nc_tot["2023"], nc_tot["2024"], c_tot["2023"], c_tot["2024"]]
    })
    fig = px.bar(
        df,
        x="Category",
        y="Value",
        color="Year",
        barmode="group",
        title="Non-current vs Current Assets"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_equity(bs_json):
    eq = bs_json["financial_position"]["equity_and_liabilities"]["equity"]
    rows = []
    for item in eq["items"]:
        if "subitems" in item:
            for sub in item["subitems"]:
                rows.append({
                    "parent": item["name"],
                    "name":   sub["name"],
                    "value":  sub["2024"]
                })
        else:
            rows.append({
                "parent": "",
                "name":   item["name"],
                "value":  item["2024"]
            })
    rows.append({
        "parent": "",
        "name": "Total Equity",
        "value": eq["total_equity"]["2024"]
    })
    df = pd.DataFrame(rows)
    fig = px.treemap(
        df,
        path=["parent","name"],
        values="value",
        title="Equity Breakdown (2024)"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_liabilities(bs_json):
    liab = bs_json["financial_position"]["equity_and_liabilities"]["liabilities"]

    def extract(section, label):
        rows = []
        sec = liab[section]
        for item in sec["items"]:
            if "subitems" in item:
                for sub in item["subitems"]:
                    rows.append({
                        "parent": label,
                        "name":   sub["name"],
                        "value":  sub["2024"]
                    })
            else:
                rows.append({
                    "parent": label,
                    "name":   item["name"],
                    "value":  item["2024"]
                })
        rows.append({
            "parent": "",
            "name": f"Total {label}",
            "value": sec[f"total_{section}_liabilities"]["2024"]
        })
        return rows

    df = pd.DataFrame(extract("non_current","Non-current Liabilities")
                      + extract("current","Current Liabilities"))
    fig = px.sunburst(
        df,
        path=["parent","name"],
        values="value",
        title="Liabilities (2024)",
        hover_data={"value":True}
    )
    st.plotly_chart(fig, use_container_width=True)

def show_balance_composition(bs_json):
    # grab the 2024 figures
    assets = bs_json["financial_position"]["assets"]["total_assets"]["2024"]
    equity  = bs_json["financial_position"]["equity_and_liabilities"]["equity"]["total_equity"]["2024"]
    liabilities = bs_json["financial_position"]["equity_and_liabilities"]["liabilities"]["total_liabilities"]["2024"]

    # build a small DataFrame
    df = pd.DataFrame({
        "Component": ["Total Assets", "Total Equity", "Total Liabilities"],
        "Amount":    [assets, equity, liabilities]
    })

    # Plotly‑Express bar chart
    fig = px.bar(
        df,
        x="Component",
        y="Amount",
        text="Amount",
        title="Balance Sheet Composition (2024)",
        labels={"Amount":"₹ Crores","Component":""}
    )
    # show the raw values on bars
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("📑 Balance Sheet Charts")
    show_non_current_assets(data)
    show_current_assets(data)
    show_assets_totals(data)
    st.divider()
    show_equity(data)
    show_liabilities(data)
    st.divider()
    show_balance_composition(data)

main()