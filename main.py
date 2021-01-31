# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:40:44 2021

@author: Julio Rubio Pons
"""
import pandas as pd
import electricdata as ed

# Fichero CSV con importes de las factuas con la comercializadora actual
invoices_csv = 'invoices-data.csv'

# Fichero CSV con precios PVPC
pvpc_csv = 'pvpc_2020-01-01_2021-01-26.csv'

# Fichero CSV con medidas del contador (extríado de la web de i-DE)
meter_csv = 'consumo_periodo_24-01-2020_24-01-2021.csv'

# Todos esos datos en CSV convertidos a DataFrames para hacer cálculos
df_invoices = ed.invoices_to_df(invoices_csv)
df_a, df_dha, df_dhs = ed.pvpc_to_df(pvpc_csv)
df_meter = ed.meter_to_df(meter_csv)

# DataFrame con todos los datos
# Nota: como tengo tarifa DHA compararo con PVPC DHA 
df_merged = ed.merge_data(df_meter, df_dha)


# tmp = df_merged.loc[df_invoices.iloc[0,0]:df_invoices.iloc[0,1]]

# Slicing (troceo) de los datos por periodos de facturación para comparar
df_result = pd.DataFrame(columns=['day1','day2','simulated_price','invoice_price','metered_kWh','invoice_kWh'])
for idx, invoice_row in df_invoices.iterrows():
    
    day1 = invoice_row['day1']
    day2 = invoice_row['day2']
    
    print(f"\n--- {day1} --> {day2} ---:")
    
    # Extrae los datos de un intervalo concreto de una factura
    df_one_invoice  = df_merged.loc[day1:day2]
    
    # Cálculos
    simulated_price = df_one_invoice['price'].sum()
    metered_kWh     = df_one_invoice['meter_kWh'].sum()
    invoice_price   = invoice_row['energy_eur']
    invoice_kWh     = invoice_row['p1_kWh'] + invoice_row['p2_kWh'] 
    
    print(f"€: {simulated_price} --> {invoice_price}, kWh: {metered_kWh} = {invoice_kWh}")
    
    result_row = {'day1': day1,
                  'day2': day2,
                  'simulated_price': simulated_price,
                  'invoice_price': invoice_price,
                  'metered_kWh': metered_kWh,
                  'invoice_kWh': invoice_kWh}
    
    df_result = df_result.append(result_row, ignore_index=True)
    
df_result['increase_percent'] = (df_result['invoice_price'] / df_result['simulated_price'] - 1) * 100


# Imprimir resultados
print(df_result)
print(df_result.mean())

# Esportar resultados
df_result.to_excel('results.xlsx')
df_result.to_html('results.html', index=False)








# =============================================================================
# # Algunas comprobaciones:
# # Slicing: sacar un día concreto para ver qué es correcto comparandolo con la gráfica diaria
# # https://www.esios.ree.es/es/pvpc?date=26-01-2021
# #
# df_a.loc['20210126']
# 
# # ver qué pasa los días de cambio de hora.
# # marzo: el día oficial tiene 23 horas
# # octubre: el día oficial tiene 25 horas
# df_a.loc['20200329']
# df_a.loc['20200329'].count()
# df_a.loc['20201025']
# df_a.loc['20201025'].count()
# =============================================================================

