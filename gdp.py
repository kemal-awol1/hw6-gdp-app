import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Global GDP Dashboard")

st.title("Global GDP Dashboard")

st.write(
    "Interactive stacked GDP visualization by region."
)


url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

tables = pd.read_html(response.text)

df = tables[2]


df = df.iloc[1:21]

source = st.selectbox(
    "Select GDP Source",
    ["IMF (2026)[1]", "World Bank (2024)[6]", "United Nations (2024)[7]"]
)

df = df.iloc[:, [0, list(df.columns).index(source)]]

df.columns = ["Country", "GDP"]

df["GDP"] = (
    df["GDP"]
    .astype(str)
    .str.replace(",", "", regex=False)
)

df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")

region_map = {
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",

    "China": "Asia",
    "Japan": "Asia",
    "India": "Asia",
    "South Korea": "Asia",
    "Indonesia": "Asia",
    "Saudi Arabia": "Asia",
    "Turkey": "Asia",

    "Germany": "Europe",
    "United Kingdom": "Europe",
    "France": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Netherlands": "Europe",
    "Russia": "Europe",

    "Brazil": "South America",

    "Australia": "Oceania"
}

df["Region"] = df["Country"].map(region_map)

df = df.dropna()

fig = px.bar(
    df,
    x="Region",
    y="GDP",
    color="Country",
    title="GDP by Country and Region",
    labels={"GDP": "GDP (Million US$)"}
)

fig.update_layout(
    barmode="stack"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("GDP Data")

st.dataframe(df)

st.markdown("""
---
**Developed by:**  
Kemal Lemnuro Awol, MD, MPH Candidate  
Johns Hopkins Bloomberg School of Public Health
""")