import streamlit as st

from src.utils import read_markdown_file


st.set_page_config(layout="wide")


if __name__ == "__main__":
    st.markdown(
        "<h1 style='text-align: center; color: green;'>Classification & Parsing</h1>",
        unsafe_allow_html=True,
    )
    intro_markdown = read_markdown_file("introduction.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)