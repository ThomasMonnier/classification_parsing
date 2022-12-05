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


def action():
    st.session_state.index += 1


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

        if "index" not in st.session_state:
            st.session_state.index = 0
        
        uploaded_file = uploaded_files[st.session_state.index]
        
        with open(uploaded_file.name, "wb") as buffer:
            shutil.copyfileobj(uploaded_file, buffer)
        
        with col_1:
            provider = st.selectbox('Provider: ', ('A2A', 'ACEA', 'IREN'))
            displayPDF(uploaded_file.name)

        with col_2:
            st.info(uploaded_file.name)
        
        dfs = read_pdf_lst_df(uploaded_file.name)

        if provider == 'A2A':
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
            dates = list(set(dates))
            display_dates = list(set(display_dates))

            with col_2:
                if len(dates) > 0:
                    st.info('Dates are {}'.format(display_dates))
                    diff_months = 1 + relativedelta.relativedelta(max(dates), min(dates)).months
                    st.info('Months: {}'.format(len(dates)))
                    st.info('Validation: {}'.format((len(dates) == diff_months)))
        
        elif provider == 'ACEA':
            dates, display_dates = [], []
            for df in dfs:
                columns = list(df.columns)
                if columns in [
                    ['DAL', 'AL', 'Unnamed: 0', "UNITA' DI MISURA", 'PREZZO UNITARIO', "QUANTITA'", 'euro'],
                    ['DETTAGLIO CONSUMO FATTURATO NEL PERIODO', 'Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3'],
                    ['DETTAGLIO CONSUMO FATTURATO NEL PERIODO ED EVENTUALI RICALCOLI DA CONGUAGLI', 'Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3']
                ]:
                    for iter, row in df.iterrows():
                        for i in range(3):
                            try:
                                dates.append(datetime.strptime(row[i], "%d/%m/%Y"))
                                dates.append(datetime.strptime(row[i+1], "%d/%m/%Y"))
                                display_dates.append(row[i])
                                display_dates.append(row[i+1])
                            except:
                                pass
                    dates = list(set(dates))
                    display_dates = list(set(display_dates))
                    break
            
            with col_2:
                if len(dates) > 0:
                    st.info('Dates are {}'.format(display_dates))
                    diff_tot = relativedelta.relativedelta(max(dates), min(dates))
                    diff_months = diff_tot.months + 1*(diff_tot.days > 15)
                    st.info('Months: {}'.format(diff_months))
        
        with col_2:
            if st.session_state.index + 1 < len(uploaded_files):
                next = st.button('Next', on_click=action)
        
            else:
                st.info('All invoices have been processed ({} invoice{})'.format(len(uploaded_files), 's'*(len(uploaded_files)>1)))
                st.session_state.index = 0
            
            display = st.selectbox('Display dataframes', ('False', 'True'))
            if display == "True":
                for df in dfs:
                    with col_2:
                        st.dataframe(df)
            