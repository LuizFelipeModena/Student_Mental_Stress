import pandas as pd
import re

def load_data(filepath, sep=',', encoding='utf-8', drop_duplicates=True, fill_na=None):
    """
    Carrega um arquivo CSV e realiza pré-processamento básico.

    Parâmetros:
    - filepath: Caminho do arquivo CSV.
    - sep: Separador do CSV (padrão: vírgula).
    - encoding: Tipo de codificação (padrão: utf-8).
    - drop_duplicates: Se True, remove duplicatas (padrão: True).
    - fill_na: Valor para preencher nulos (se None, os nulos permanecem).
    
    Retorna:
    - DataFrame tratado.
    """
    try:
        df = pd.read_csv(filepath, sep=sep, encoding=encoding)

        if drop_duplicates:
            df.drop_duplicates(inplace=True)
        
        if fill_na is not None:
            df.fillna(fill_na, inplace=True)
        else:
            df.dropna(inplace=True)

        return df

    except Exception as e:
        print(f'Erro ao carregar {filepath}: {e}')
        return None
    

def normalize_dataframe_columns(df):
    """
    Normaliza os nomes das colunas:
    - Remove observações entre parênteses
    - Converte para minúsculas
    - Converte CamelCase/PascalCase para snake_case (ex: 'CustomerID' -> 'customer_id')
    - Substitui espaços por '_'
    - Remove múltiplos '_' seguidos
    - Remove '_' no início e no fim
    """
    def to_snake_case(column_name):
        column_name = re.sub(r"\s*\(.*?\)", "", column_name)
        column_name = re.sub("(?<!^)(?=[A-Z])", "_", column_name)
        column_name = column_name.replace(" ", "_")
        column_name = column_name.lower()
        column_name = re.sub(r"_+", "_", column_name)
        column_name = column_name.strip("_")
        return column_name 
    
    df.columns = [to_snake_case(col) for col in df.columns]

    return df

def convert_to_binary(df, columns):

    for col in columns:
        df[col] = df[col].map({'Yes': 1, 'No': 0})

    return df
