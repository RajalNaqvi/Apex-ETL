import extra_streamlit_components as stx
import streamlit as st

val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])
st.write(val)