import streamlit as st
import shutil

from src.utils import read_markdown_file, pattern_match
from src.test_tabula import read_pdf_lst_df


st.set_page_config(layout="wide")


if __name__ == "__main__":
    st.markdown(
        "<h1 style='text-align: center; color: green;'>Classification & Parsing</h1>",
        unsafe_allow_html=True,
    )
    intro_markdown = read_markdown_file("introduction.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a file (PDF / PNG)",
        type=["pdf"],
    )

    if uploaded_file:
        with open(uploaded_file.name, "wb") as buffer:
            shutil.copyfileobj(uploaded_file, buffer)
        
        dfs = read_pdf_lst_df(uploaded_file.name)
        len_dfs = [len(list(df.columns)) for df in dfs]
        i, j = 1, 0
        while j < 5:
            pattern = [i, i+1, i+2]
            st.info(pattern)
            st.info(pattern_match(pattern, len_dfs))

        for df in dfs:
            st.dataframe(df)