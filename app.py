import streamlit as st
from dateutil.parser import parse
from datetime import datetime
from dateutil import relativedelta
import shutil
import base64

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


def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="600" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


if __name__ == "__main__":
    st.markdown(
        "<h1 style='text-align: center; color: green;'>Classification & Parsing</h1>",
        unsafe_allow_html=True,
    )
    intro_markdown = read_markdown_file("introduction.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choose a file (PDF / PNG)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        col_1, col_2 = st.columns(2)

        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as buffer:
                shutil.copyfileobj(uploaded_file, buffer)
            
            with col_1:
                displayPDF(uploaded_file.name)

            with col_2:
                st.info(uploaded_file.name)
            
            dfs = read_pdf_lst_df(uploaded_file.name)
            for df in dfs:
                columns = list(df.columns)
                if columns[0] == "Unnamed: 0":
                    try:
                        new_header = df.iloc[0] #grab the first row for the header
                        df = df[1:] #take the data less the header row
                        df.columns = new_header #set the header row as the df header
                    except:
                        pass

            dates, display_dates = [], []
            for df in dfs:
                columns = list(df.columns)
                if is_date(columns[0]):
                    dates.append(datetime.strptime(columns[0], "%d.%m.%Y"))
                    display_dates.append(columns[0])
                with col_2:
                    st.dataframe(df)
            dates = list(set(dates))
            display_dates = list(set(display_dates))

            with col_2:
                if len(dates) > 0:
                    st.info('Dates are {}'.format(display_dates))
                    st.info('Months: {}'.format(relativedelta.relativedelta(max(dates), min(dates)).months))
