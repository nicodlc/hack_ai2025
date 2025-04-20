import streamlit as st

st.set_page_config(
    page_title="LTI Intelligence Platform",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

pg = st.navigation([
    st.Page(page="./pages/agent.py", title="LTI Agent"), 
    st.Page(page="./pages/employeeCharts.py", title="Employee Charts"),
    st.Page(page="./pages/balanceSheetChart.py", title="Balance Sheets Charts"),
    st.Page(page="./pages/profitAndLossChart.py", title="Profit And Loss Charts"),
    st.Page(page="./pages/currentInvestments.py", title="Current Investments")
])
pg.run()
