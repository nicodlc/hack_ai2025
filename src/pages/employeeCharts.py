import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title(":busts_in_silhouette: Employee Charts Dashboard")

data = None
with open('./json/employee_chart1.json', 'r') as file:
    data = json.load(file)

emp_df   = pd.json_normalize(data["employees"],         record_path=None)
diff_df  = pd.json_normalize(data["differently_abled_employees"])
women_df = pd.json_normalize(data["women_representation"])
turn_df  = pd.DataFrame(data["turnover_rate_permanent_employees"]).T.reset_index().rename(columns={"index":"FY"})


st.subheader("Employee Demographics")
fig1 = px.bar(
    emp_df,
    x="category",
    y=["male.pct","female.pct","others.pct"],
    title="Gender % by Employee Category",
    labels={"value":"%", "category":"Category"},
    barmode="stack",
    hover_data={"male.count":True, "female.count":True, "others.count":True}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Employees: Differently-Abled")
fig2 = px.bar(
    diff_df,
    x="category",
    y=["male.count","female.count","others.count"],
    title="Differently‑abled Employees by Category",
    barmode="group",
    hover_data={"male.pct":True, "female.pct":True, "others.pct":True}
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Women Representation")
fig3 = px.pie(
    women_df,
    names="role",
    values="female.pct",
    title="Women % in Key Roles",
    hole=0.4,
    hover_data=["female.count","total"]
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Employee Turnover line chart")
fig4 = px.line(
    turn_df,
    x="FY",
    y=["male","female","others","total"],
    markers=True,
    title="Turnover Rate (Permanent Employees)"
)
st.plotly_chart(fig4, use_container_width=True)