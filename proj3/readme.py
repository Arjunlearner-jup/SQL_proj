from pathlib import Path
import streamlit as st

def read_markdown_file(path):
    return Path(path).read_text(encoding="utf-8")

st.title("SQL_proj_2")

readme_text = read_markdown_file("README.md")
st.markdown(readme_text)