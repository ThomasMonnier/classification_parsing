from . import tabula


def read_pdf_lst_df(file):
    'Read pdf into list of DataFrame'
    dfs = tabula.read_pdf(file, pages='all')
    return dfs


def read_url_lst_df(url):
    'Read remote pdf into list of DataFrame'
    dfs2 = tabula.read_pdf(url)
    return dfs2


def convert_pdf_csv(file, output="output.csv"):
    'convert PDF into CSV file'
    tabula.convert_into(file, output, output_format="csv", pages='all')


def convert_all_pdf_csv(dir):
    'convert all PDFs in a directory'
    tabula.convert_into_by_batch(dir, output_format='csv', pages='all')