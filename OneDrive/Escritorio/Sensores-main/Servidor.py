# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 20:03:20 2024

@author: Ivan Camilo Leiton Murcia
"""
from sqlalchemy import create_engine
import socket
import time
#from matplotlib import pyplot as plt
#import matplotlib.animation as animation
import json
import threading
import pandas as pd
import numpy as np
import json

PORT=8889
IP="192.168.0.180"

def handler(client_soc):
    client_soc.send(b"a")
    print("Peticion enviada")
    time.sleep(20)
    global df

    try:
        data=client_soc.recv(65536).decode()
        print(data,"\n")
        if len(data)>4:
            j=json.loads(data)
            print("datos recibidos")
            j["time"]=time.strftime('%X')
            
            #df = pd.DataFrame.from_dict([j], orient='columns')
            #df=pd.concat([df, pd.DataFrame([j])], ignore_index=True)
    	    

            # print(df,"\n")
            #print(json,"\n")
            df=pd.concat([df, pd.DataFrame([j])], ignore_index=True)
            df2=pd.DataFrame([j])
            df2 = df2.rename(columns={
            'Device': 'device',
            'IP': 'ip',
            'LUX': 'lux',
            'NH3': 'nh3',
            'HS': 'hs',
            'H': 'h',
            'T': 't',
            'time': 'time'
            })	    
            #df2['time'] = pd.to_datetime(df2['time'], format='%H:%M:%S').dt.time
            df2['time'] = pd.to_datetime(df2['time'])
            condicion = df2['time'].apply(lambda x: x.minute % 5 == 0 and 0 <= x.second <= 10)

            # Filtrar el DataFrame usando la condicional
            df2_filtrado = df2[condicion]

            # Enviar datos a la base de datos
            send_to_db(df2)

            #print(df)
            df.to_excel("data_test_15.xlsx",sheet_name='sheet1', index=False)
            df_test = pd.DataFrame({
            'device': ['ESP#'],
            'ip': ['192.168.20.56'],
            'lux': [0],
            'nh3': [0],
            'hs': [0],
            'h': [0],
            't': [0],
            'time': ['00:00:00']
        })
            
      

        
    except Exception as e:
        print (e)
        # c.close()
        # break          
    
    client_soc.close()

def send_to_db(df):
    # Conexión a la base de datos PostgreSQL
    engine = create_engine('postgresql+psycopg2://alex:123@localhost:5432/granja')
    
    # Insertar datos en la tabla 'nombre_tabla'
    df.to_sql('sensors3', engine, if_exists='append', index=False)


def main ():
    
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    global df
    df=pd.DataFrame()
    
    with s:
        s.bind((IP,PORT))
        s.listen(True)
        while 1:
        
            client_soc, client_address = s.accept()
            client_soc.settimeout(25)
            # Send each "client_soc" connection as a parameter to a thread.
            threading.Thread(target=handler,args=(client_soc,), daemon=True).start() 
 

    
if __name__ == "__main__": 
    print("Servidor ON")
    main()
