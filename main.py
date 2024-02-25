import json
import pandas as pd
import logging
from utils import get_row_with_column_names, reverse_dictio


with open("dictios/dic_entities.json", 'r') as de:
  dic_entities = json.load(de)

with open("dictios/dic_sector.json", 'r') as de:
  dic_sector = json.load(de)

with open("dictios/dic_sec_ents.json", 'r') as de:
  dic_sec_ents = json.load(de)

with open("dictios/dic_tipo_gasto.json", 'r') as de:
  dic_tipo_gasto = json.load(de)

dfs = {}
for i in range(2013, 2023):
  renglon = get_row_with_column_names('data/Decreto_de_liquidacion.xlsx',
                                      f"Gastos PGN {i}")
  
  df = pd.read_excel('Decreto_de_liquidacion.xlsx',
                     sheet_name=f"Gastos PGN {i}", skiprows=renglon)
  
  df.columns = [s.strip() for s in df.columns]
  df = df[~(df['CTA\nPROG'].isna()) | ~(df['CONCEPTO'].isna())]
  df['CONCEPTO'] = df['CONCEPTO'].str.capitalize().str.strip()
  df.loc[df['CONCEPTO'] == 'Ministerio de cultura', 'CONCEPTO'] = "Ministerio de las culturas, las artes y los saberes"

  rev_entities = reverse_dictio(dic_entities)

  df['CONCEPTO'] = df['CONCEPTO'].fillna(method='ffill')
  
  df['Código de entidad'] = df['CONCEPTO'].map(rev_entities)
  df['CTA\nPROG'] = df['CTA\nPROG'].str.strip().map(dic_tipo_gasto)

  df = df.filter(['CTA\nPROG', 'CONCEPTO', 'TOTAL', 'Código de entidad'])
  df = df[~(df['CONCEPTO'].str.contains('Seccion:'))].reset_index(drop=True)


  df['Código del sector'] = df['Código de entidad'].astype(str).map(dic_sec_ents)
  df['Sector'] = df['Código del sector'].astype('Int64').astype(str).map(dic_sector)

  df.rename(columns={'CTA\nPROG': 'Tipo de gasto',
                     'CONCEPTO': 'Entidad',
                     'TOTAL': 'Apropiación a precios corrientes'}, inplace=True)
  
  df = df.dropna(subset='Tipo de gasto').reset_index(drop=True)

  dfs[i] = df
  logging.warning(f"Decreto año {i}: cleaned!!")


data = (pd
 .concat(dfs.values(), keys=dfs.keys())
 .reset_index()
 .drop(columns='level_1')
 .rename(columns={'level_0':'Año'}))

data.to_csv('data/gastos.csv', index=False)


