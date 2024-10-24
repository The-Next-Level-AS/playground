from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.button_selector import button_selector
import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="✨ Playground",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)
st.markdown(
    """
    <style>
        [data-testid="stSidebarHeader"], [data-testid="stHeader"] {
            display: none;
        }
        [data-testid="stMainBlockContainer"] {
            padding-top: 0.75rem;
        }
        [data-testid="stSidebar"] {
            top: 0;
        }
        textarea {
            resize: none !important;
        }
        [data-testid="stIFrame"] {
            border: dashed 1px #80808080;
            border-radius: 8px;
            background: #fff;
            box-shadow: hsl(220deg 12.5% 50% / 25%) 0px 0px 0px 10000px;
            mix-blend-mode: multiply;
        }
        [data-testid="stHtml"] strong {
            margin-bottom: -0.75rem;
            display: block;
        }
        [data-testid="stSidebarCollapsedControl"] {
            top: 0;
            left: 0.25rem;
            transform: scale(0.75);
        }
        textarea {
            font-family: monospace !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_boilerplate():
    with open("./boilerplates/outland.json", "r", encoding="utf-8") as outland:
        return json.load(outland)


outland_boilerplate = load_boilerplate()
df = pd.DataFrame(outland_boilerplate["data_sources"])
st.sidebar.header("✨ Playground")
boilerplate = st.sidebar.selectbox("Boilerplate:", ("", "Outland"), index=1)
col1, col2 = st.columns([1, 3], gap="medium")
with col1:
    st.html("<strong>User journeys:</strong>")
    container = st.container(border=True)
    with container:
        user_journeys = (
            outland_boilerplate["user_journeys"] if boilerplate == "Outland" else []
        )
        selected_user_journey = button_selector(
            [item["name"] for item in user_journeys], index=0, spec=1
        )
with col2:
    st.html("<strong>Data sources:</strong>")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.html("<strong>Current retrieved data:</strong>")
    container3 = st.container(border=True)
    container3.json([], expanded=1)
st.html("<strong>Matrices:</strong>")
container2 = st.container(border=True)
with container2:
    selected_matrix = button_selector(
        [
            item2.split("/")[1].split(".")[0]
            for item2 in user_journeys[selected_user_journey]["matrices"]
        ],
        index=0,
        spec=3,
    )
with st.sidebar:
    add_vertical_space()
selected_tgm = st.sidebar.selectbox(
    "Text Generation Model:",
    ("Mistral-Nemo-Instruct-2407", "Phi-3-mini-4k-instruct"),
    index=0,
)
if selected_tgm == "Mistral-Nemo-Instruct-2407":
    tgm = "mistral"
elif selected_tgm == "Phi-3-mini-4k-instruct":
    tgm = "phi"
else:
    tgm = "mistral"
selected_tem = st.sidebar.selectbox(
    "Text Embedding Model:", ("NoInstruct small Embedding v0"), index=0
)
if selected_tem == "NoInstruct small Embedding v0":
    tem = "noinstruct"
else:
    tem = "noinstruct"
with st.sidebar:
    add_vertical_space()
st.sidebar.html("<strong>Signal:</strong>")
st.html("<strong>Artifact:</strong>")
components.iframe(
    "https://platform.nxtl.ai/"
    + (
        "outland/blank.html?log="
        + str(st.query_params.log)
        + "&tgm="
        + tgm
        + "&tem="
        + tem
        + "&matrix="
        if boilerplate == "Outland"
        else ""
    )
    + user_journeys[selected_user_journey]["matrices"][selected_matrix]
    .split("/")[1]
    .split(".")[0],
    height=500,
)
st.sidebar.text_area("Accumulated user signals:", str(st.query_params.log), height=256)
st.sidebar.text_area("Current sentiment:", "", height=128, disabled=True)
js = """
        <script>
            window.parent.postMessage("streamlit_ready", '*');
        </script>
    """
st.components.v1.html(js, height=0)
