# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 18:34:56 2021

@author: Julio Rubio Pons
"""


import pandas as pd


def invoices_to_df(csv_file):
    # csv_file format assumes sep=',' and decimal='.'
    # Example:
    #   day1,day2,energy_eur,p1_kWh,p2_kWh
    #   2020-11-23,2020-12-21,26.99,79,205

    df = pd.read_csv(csv_file)
    return df

def pvpc_to_df(csv_file):
    # csv_file format: original formrat from ree download page.
    # Source: https://www.esios.ree.es/es/pvpc
    # Intructions:
    # - Click on 'Analizar indicador' icon on the upper left of the graph
    # - Select desired dates 
    # - Click on "Exportación" in the bottom left corner of the page
    # - Select "CSV"
    # 
    # Detailed instructions: https://nergiza.com/foro/threads/historico-en-excel-o-csv-de-precios-pvpc.5119/#post-42982
    df = pd.read_csv(csv_file,sep=';',
                      usecols=[1,4,5])
    
    # Nombres más claros y concisos para los tres tipos de tarifa
    # A, DHA, DHS
    df['name']=df['name'].str.replace('.*peaje.*','A', regex=True)
    df['name']=df['name'].str.replace('.*DHA.*','DHA', regex=True)
    df['name']=df['name'].str.replace('.*vehículo.*','DHS', regex=True)
    
    
    # Hay que convertir los timestamps a UTC de lo contrario da este error (por no poder mezclar +0100 y +0200):
    #   ValueError: Tz-aware datetime.datetime cannot be converted to datetime64 unless utc=True
    # Luego se convertien de nuevo a la zona horaria 'Europe/Madrid' y ya funciona
    df['datetime'] = pd.to_datetime(df['datetime'],utc=True).dt.tz_convert('Europe/Madrid')
    
    # el precio de este CSV es en €/MWh, se pasa a €/kWh
    df['value']=df['value']/1000
    df.rename(columns={"value":"price_kWh"}, inplace=True)
    
    # Indexar todo el df usando la fecha/hora como nuevo índice
    df.set_index('datetime', inplace=True)
    
    
    # Tres df separadas, una por cada tipo de tarifa PVPC
    df_a   = df[df['name'] == 'A']
    df_dha = df[df['name'] == 'DHA']
    df_dhs = df[df['name'] == 'DHS']
    
    return  df_a,df_dha,df_dhs

def meter_to_df(csv_file):
    # csv_file format as downloaded from https://www.i-de.es
    df_meter = pd.read_csv(csv_file, sep=';',
                           usecols=[0,1,2,3], parse_dates=[1])
    
    
    df_meter = df_meter.rename(columns={"FECHA-HORA":"datetime", "INV / VER": "dst", "CONSUMO Wh": "meter_Wh"})
    
    # paso a kWh
    df_meter['meter_kWh'] = df_meter['meter_Wh'] / 1000
    df_meter.drop(columns=['meter_Wh','CUPS'], axis=1, inplace=True)
    
    
    # normaliza el formato de fecha para incluir la zona horaria.
    # de ese modo la columna datetime tiene el mismo fomato que la que se usa
    # en df_pvpc. Es calve el parametro _ambigous_ para resolver la ambigüedad
    # del cambio de hora en octubre, cuando el día tiene una hora repetida.
    df_meter['datetime'] = df_meter['datetime'].dt.tz_localize('Europe/Madrid', ambiguous=df_meter['dst'])
    
    df_meter.set_index('datetime', inplace=True) # el índice es la fecha
    
    return df_meter

def merge_data(df_meter, df_pvpc):
    # Adds to df_meter the prices from df_pvpc using the datetime column as key
    
    df_merged = pd.merge(df_meter, df_pvpc, how='left', on='datetime')
    # new column with the calculated price for each day hour
    df_merged['price'] =  df_merged['meter_kWh'] * df_merged['price_kWh']
    
    return df_merged
    
        