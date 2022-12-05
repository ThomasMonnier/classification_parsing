import streamlit as st
from dateutil.parser import parse
import shutil

from src.utils import read_markdown_file, pattern_match
from src.test_tabula import read_pdf_lst_df


st.set_page_config(layout="wide")


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


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

        for df in dfs:
            columns = list(df.columns)
            if columns[0] == "Unnamed: 0":
                new_header = df.iloc[0] #grab the first row for the header
                df = df[1:] #take the data less the header row
                df.columns = new_header #set the header row as the df header

        for df in dfs:
            columns = list(df.columns)
            dates = []
            if is_date(columns[0]):
                dates.append(columns[0])
                st.dataframe(df)
            st.info('Dates are {}'.format(list(set(dates))))