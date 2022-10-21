import pandas as pd

ALLOWED_EXTENSIONS = {'csv', 'tsv', 'xlsx'}


def read_data(file):
    """
    Converts input files into pandas dataframe.
    """
    extension = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower()

    if extension in ALLOWED_EXTENSIONS:
        if extension == 'csv':
            data = pd.read_csv(file, header=0, encoding='utf-8')
        elif extension == 'tsv':
            data = pd.read_csv(file, header=0, delimiter='\t', encoding='utf-8')
        else:
            data = pd.read_excel(file, header=0, engine='openpyxl')

        return data

    raise FileNotFoundError('Unable to read data. The file extension may not be supported.')
