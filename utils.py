import pandas as pd
import json

with open("dictios/dic_entities.json", 'r') as de:
  dic_entities = json.load(de)

with open("dictios/dic_sector.json", 'r') as de:
  dic_sector = json.load(de)

with open("dictios/dic_sec_ents.json", 'r') as de:
  dic_sec_ents = json.load(de)

with open("dictios/dic_tipo_gasto.json", 'r') as de:
  dic_tipo_gasto = json.load(de)

def get_row_with_column_names(path, sheetname):
    renglon = 0
    df = pd.read_excel(path,
                          sheet_name=sheetname,
                          skiprows=renglon,
                          nrows=10)
    while "CONCEPTO" not in df.columns:

        renglon += 1
        df = pd.read_excel(path,
                          sheet_name=sheetname,
                          skiprows=renglon,
                          nrows=10)
    return renglon

def reverse_dictio(dictio):
  reversed_entities = {}
  for key, value in dic_entities.items():
    reversed_entities[value] = key

  return reversed_entities