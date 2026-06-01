import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Kiln Firing Log Viewer")

uploaded_file = st.file_uploader("Upload Skutt CSV Log", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, skipinitialspace=True)
    df = df.dropna(subset=['t30s']).copy()

    df["Time"] = pd.to_datetime(df["t30s"] * 30, unit='s', errors='coerce')

    st.subheader("Firing Profile Analyis")

    fig = px.line(
        df,
        x="Time",
        y=["sp", "temp2"],
        color_discrete_map={
            "sp": "#FF4B4B",
            "temp2": "#0068C9"
        },
        hover_data=["out2"],
        title="Kiln Temperature & Relay Output",
    )

fig.update_layout(hovermode="x unified")

fig.update_xaxes(
    tickformat="%H:%M:%S",
    hoverformat="<b><span style='font-size: 22px;'>%H:%M:%S</span></b>",
    title_text="Elapsed Time (HH:MM:SS)"
)

fig.update_yaxes(
    ticksuffix=" °F",
    title_text="Temperature"
)

fig.update_layout(
    yaxis_title="Temperature (°F)",
    legend=dict(
        title=None,
        font=dict(size=14)
    )
)

for trace in fig.data:
    if trace.name == "sp":
        trace.name = "Target Temp"
        trace.hovertemplate = "%{y}<br>Relay Output: %{customdata[0]}%"
    
    elif trace.name == "temp2":
        trace.name = "Actual Temp"
        trace.hovertemplate = "%{y}<br>Relay Output: %{customdata[0]}%"

st.plotly_chart(fig, use_container_width=True)