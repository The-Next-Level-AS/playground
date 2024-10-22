import streamlit as st
import pandas as pd
from streamlit_extras.button_selector import button_selector
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit.components.v1 as components
import json


with open("./default.html", "r", encoding="utf-8") as file:
    default = file.read()

with open("./boilerplates/outland.json", "r", encoding="utf-8") as outland:
    outland_boilerplate = json.load(outland)

df = pd.DataFrame(
    {
        "Name": ["", "", ""],
        "Type": [
            "",
            "",
            "",
        ],
        "Size": [
            "",
            "",
            "",
        ],
    }
)

title = "✨ Playground"
st.set_page_config(
    page_title=title, layout="wide", initial_sidebar_state="expanded", menu_items={}
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
  </style>
""",
    unsafe_allow_html=True,
)
st.sidebar.header(title)

boilerplate = st.sidebar.selectbox("Boilerplate:", ("", "Outland"), index=1)

col1, col2 = st.columns(2)

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
    st.dataframe(
        df,
        column_config={
            "name": "App name",
            "stars": st.column_config.NumberColumn(
                "Github Stars",
                help="Number of stars on GitHub",
                format="%d ⭐",
            ),
            "url": st.column_config.LinkColumn("App URL"),
            "views_history": st.column_config.LineChartColumn(
                "Views (vvpast 30 fsdays)", y_min=0, y_max=5000
            ),
        },
        use_container_width=True,
        hide_index=True,
    )
    st.html("<strong>Current retrieved data:</strong>")
    container3 = st.container(border=True)
    container3.json(
        {},
        expanded=1,
    )
# container.write(f"Selected month: {month_list[selected_index]}")
st.html("<strong>Matrices:</strong>")
container2 = st.container(border=True)
with container2:
    selected_matrix = button_selector(
        [
            item.split("/")[1].split(".")[0]
            for item in user_journeys[selected_user_journey]["matrices"]
        ],
        index=0,
        spec=4,
    )
# st.html("<strong>Matrix:</strong>")
# st.code(default, language="html")
with st.sidebar:
    add_vertical_space()
st.sidebar.selectbox(
    label="Large Language Model:",
    # index=category_indices[parameters.category.value],
    options=[""],
    # key=parameters.category.key,
    # on_change=functools.partial(
    #     parameters.update_parameter_from_session_state,
    #     key=parameters.category.key
    # )
)
st.sidebar.selectbox(
    label="Embedding Model:",
    # index=category_indices[parameters.category.value],
    options=[""],
    # options=["NoInstruct small Embedding v0"],
    # key=parameters.category.key,
    # on_change=functools.partial(
    #     parameters.update_parameter_from_session_state,
    #     key=parameters.category.key
    # )
)
with st.sidebar:
    add_vertical_space()
st.sidebar.html("<strong>Signal:</strong>")
txt = st.sidebar.text_area(
    "Accumulated user signals:",
    # "It was the best of times, it was the worst of times, it was the age of "
    # "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    # "was the epoch of incredulity, it was the season of Light, it was the "
    # "season of Darkness, it was the spring of hope, it was the winter of "
    # "despair, (...)",
    height=256,
)
txt = st.sidebar.text_area(
    "Current sentiment:",
    # "It was the best of times, it was the worst of times, it was the age of "
    # "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    # "was the epoch of incredulity, it was the season of Light, it was the "
    # "season of Darkness, it was the spring of hope, it was the winter of "
    # "despair, (...)",
    height=128,
    disabled=True,
)

# st.write(f"You wrote {len(txt)} characters.")
st.html("<strong>Artifact:</strong>")
components.iframe(
    "https://platform.nxtl.ai/"
    + user_journeys[selected_user_journey]["matrices"][selected_matrix],
    height=500,
)
