import streamlit as st
import plotly.express as px
import pandas as pd


st.title("Top CO₂ Emitters per Capita")

# Charger les données
df = pd.read_csv("input/CO2_per_capita.csv", sep=";")

def top_n_emitters(df, start_year, end_year, nb_displayed):
    
    #years filter
    yearsok = (df['Year'] >= start_year) & (df['Year'] <= end_year)
    #do the mean for each country
    df_filtered = df.loc[yearsok]
    #sort the values and keep nb_displayed
    df_grouped2 = (
        df_filtered
        .groupby("Country Code")["CO2 Per Capita (metric tons)"]
        .mean()
    )
    # Tri décroissant et sélection des top N
    df_sorted = df_grouped2.sort_values(
         ascending=False
    ).head(nb_displayed)

                                                                          
    #create the fig
    df_plot = df_sorted.reset_index()

    fig = px.bar(
    df_plot,
    x="Country Code",
    y="CO2 Per Capita (metric tons)",
    title=f"Top {nb_displayed} CO₂ Emitters per Capita ({start_year}-{end_year})",
    labels={
        "CO2 Per Capita (metric tons)": "CO₂ per capita (t)",
        "Country Code": "Country"
    }
    )
    return fig

# Widgets Streamlit
start_year = st.slider("Start year", int(df["Year"].min()), int(df["Year"].max()), 2008)
end_year = st.slider("End year", int(df["Year"].min()), int(df["Year"].max()), 2011)
nb_displayed = st.slider("Number of countries", 5, 20, 10)

# Graphique
fig = top_n_emitters(df, start_year, end_year, nb_displayed)
st.plotly_chart(fig)
