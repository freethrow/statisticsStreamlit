from deta import Deta  # Import Deta
from decouple import config

from io import BytesIO

import pandas as pd
import streamlit as st

import plotly.express as px

st.set_page_config(layout="wide")

# Initialize with a Project Key

deta_project_key = config("DETA_PROJECT_KEY_2", cast=str)
deta = Deta(deta_project_key)
drive = deta.Drive("statistics")
print(drive)




@st.cache
def load_world_data(filename):

    world_stats = drive.get(filename)
    content = world_stats.read()
    data_frame = pd.read_csv(BytesIO(content))
    world_stats.close()

    return data_frame


# get period
@st.cache
def load_data_period():

    deta_file = drive.get("Period.txt")
    period = deta_file.read()

    deta_file.close()
    return period.decode("utf8")


period = load_data_period()

st.header("Interscambio Commerciale della Serbia")

st.subheader(f"Periodo {period} / Valori in 1.000 EUR")

world_data = load_world_data("Serbia-Mondo.csv")

italy_data = load_world_data("Serbia-Italia.csv")

serbian_export_world = world_data[world_data["Paese"] == "TOTALE"][
    "Esportazioni"
].values[0]

serbian_export_world_var = world_data[world_data["Paese"] == "TOTALE"][
    "Var. Export"
].values[0]

serbian_import_world = world_data[world_data["Paese"] == "TOTALE"][
    "Importazioni"
].values[0]

serbian_import_world_var = world_data[world_data["Paese"] == "TOTALE"][
    "Var. Import"
].values[0]

serbian_int_world = world_data[world_data["Paese"] == "TOTALE"]["Interscambio"].values[
    0
]

serbian_int_world_var = world_data[world_data["Paese"] == "TOTALE"][
    "Var. Interscambio"
].values[0]


col1, col2, col3 = st.columns(3)
col1.metric(
    f"Esportazioni serbe nel mondo",
    f"{serbian_export_world:,}".replace(",", "."),
    f"{serbian_export_world_var}%",
)
col2.metric(
    "Importazioni serbe dal mondo",
    f"{serbian_import_world:,}".replace(",", "."),
    f"{serbian_import_world_var}%",
)
col3.metric(
    "Interscambio Serbia - mondo",
    f"{serbian_int_world:,}".replace(",", "."),
    f"{serbian_int_world_var}%",
)


with st.container():

    with st.sidebar:
        flux = st.selectbox(
            "Selezionare il flusso con il Mondo",
            ("Esportazioni", "Importazioni", "Interscambio"),
            key=1,
        )

        if flux == "Importazioni":
            var = "Var. Export"
        elif flux == "Esportazioni":
            var = "Var. Import"
        elif flux == "Interscambio":
            var = "Var. Interscambio"

        topN = st.selectbox("Quanti Paesi?", (10, 15, 20), key=2)

    fig = px.bar(
        world_data[world_data["Paese"] != "TOTALE"]
        .sort_values([flux], ascending=False)
        .head(topN),
        x="Paese",
        y=flux,
        title=f"{flux} della Serbia",
        color=var,
        color_continuous_scale="purpor",
    )
    st.plotly_chart(fig)


serbian_export_italy = world_data[world_data["Paese"] == "Italia"][
    "Esportazioni"
].values[0]

serbian_export_italy_var = world_data[world_data["Paese"] == "Italia"][
    "Var. Export"
].values[0]

serbian_import_italy = world_data[world_data["Paese"] == "Italia"][
    "Importazioni"
].values[0]

serbian_import_italy_var = world_data[world_data["Paese"] == "Italia"][
    "Var. Import"
].values[0]

serbian_int_italy = world_data[world_data["Paese"] == "Italia"]["Interscambio"].values[
    0
]

serbian_int_italy_var = world_data[world_data["Paese"] == "Italia"][
    "Var. Interscambio"
].values[0]


col1, col2, col3 = st.columns(3)
col1.metric(
    "Esportazioni serbe in Italia",
    f"{serbian_export_italy:,}".replace(",", "."),
    f"{serbian_export_italy_var}%",
)
col2.metric(
    "Importazioni serbe da Italia",
    f"{serbian_import_italy:,}".replace(",", "."),
    f"{serbian_import_italy_var}%",
)
col3.metric(
    "Interscambio Serbia - Italia",
    f"{serbian_int_italy:,}".replace(",", "."),
    f"{serbian_int_italy_var}%",
)


with st.container():

    st.header("Italia - Serbia")

    with st.expander("Dati completi"):
        st.dataframe(italy_data)

    with st.sidebar:
        flux = st.selectbox(
            "Selezionare il flusso con Italia",
            ("Esportazioni", "Importazioni", "Interscambio"),
            key=3,
        )

        if flux == "Importazioni":
            var = "Var. Export"
        elif flux == "Esportazioni":
            var = "Var. Import"
        elif flux == "Interscambio":
            var = "Var. Interscambio"

        topN = st.selectbox("Quante voci?", (10, 15, 20, 30), key=4)

    fig2 = px.bar(
        italy_data[italy_data["Voce"] != "TOTALE"]
        .sort_values([flux], ascending=False)
        .head(topN),
        x="Voce",
        y=flux,
        title=f"{flux} della Serbia - Italia",
        color=var,
        color_continuous_scale="Teal",
    )
    st.plotly_chart(fig2)
