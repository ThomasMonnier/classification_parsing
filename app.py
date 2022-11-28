import streamlit as st


st.set_page_config(layout="wide")


if __name__ == "__main__":
    st.markdown(
        "<h1 style='text-align: center; color: green;'>Classification & Parsing</h1>",
        unsafe_allow_html=True,
    )
    st.markdown('introduction.md')