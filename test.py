import unittest
import pandas as pd
import json

df = pd.read_csv('data/gastos.csv')
vals = df.groupby('Año')['Apropiación a precios corrientes'].sum().to_dict()
print(vals)

with open('dictios/dic_vals_test.json', 'r') as ds:
    dic_vals = json.load(ds)

class TestPGNVals(unittest.TestCase):

    def test_length_vals_years(self):
        self.assertEqual(len(vals), len(dic_vals))

    def test_vals_years(self):
        for key, item in vals.items():
            self.assertEqual(vals[key], dic_vals[str(key)])

# tasks
# comparar valores en tipos de gasto para cada año
# comparar valores en cuentas                       
if __name__ == "__main__":
    unittest.main()