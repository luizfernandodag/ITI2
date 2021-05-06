#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 11:04:22 2021

@author: luiz
"""


import psycopg2
import pandas as pd
import json # ler arquivo de configuracao\
import requests

#******************** connect to database *****************
#installe o pacote psycopg2 copm pip ou pip3
#pip3 install xlrd
#pip install psycopg2
#pip3 install psycopg2
#pip3 install requests

def requestURL(url):
    r = requests.get(url)
    return r.status_code

def connectDataBase():

    hostname = 'localhost'
    username = 'postgres'
    password = 'postgres'
    database = 'postgres'

    conn = psycopg2.connect("dbname=" + database + " user=" + username + " host=" + hostname + " password=" + password)




def insert_pdf_certificado_link(AC, URL, pdfStatus):

    AC = "'" + AC + "'"
    URL = "'" + URL + "'"
    pdfStatus = "'" + pdfStatus + "'"

    try:
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'postgres'

        conn = psycopg2.connect("dbname=" + database + " user=" + username + " host=" + hostname + " password=" + password)

        queryInsert = "INSERT INTO public.certificado_link(ac_nome_id, url, status) select ac_nome_id, " + URL + ", " +  pdfStatus +  " from public.ac_nome where name = " + AC
        print(queryInsert)
        cur = conn.cursor()
        cur.execute(queryInsert)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_ac_name(acNAME):

    try:
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'postgres'

        conn = psycopg2.connect("dbname=" + database + " user=" + username + " host=" + hostname + " password=" + password)
        queryInsert = "INSERT Into public.ac_nome (name) Select " + acNAME + " AS name FROM ac_nome " + " WHERE NOT EXISTS ( SELECT ac_nome_id FROM ac_nome WHERE name=" + acNAME + " ) LIMIT 1"
        print(queryInsert)
        cur = conn.cursor()
        cur.execute(queryInsert)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()







# Rode esse comando no terminal para installar o pandas
#pip instal pandas
#sudo apt-get install python3-distutils



hostname = 'localhost'
username = 'postgres'
password = 'postgres'
database = 'postgres'

try:
    conn = psycopg2.connect("dbname=" + database +" user="+username +" host="+hostname + " password=" +password)

    cur = conn.cursor()
    cur.execute("Select * from ac_nome")


    rows = cur.fetchall()
    print(rows)

    # ************************ pega novas ACS do arquivo excel **********************************8
    localizacaoExcelACS = r"/home/luiz/Desktop/ITI/arquivos/acs_url.xls"
    # verificacoo localExcel
    print(localizacaoExcelACS)
    dataFrameACNAME = pd.read_excel(localizacaoExcelACS)
    print(dataFrameACNAME)
    df = pd.DataFrame(dataFrameACNAME)


    # get all acs  do dataframe

    ACS = dataFrameACNAME['AC']




    # get o set das acs do dataframe ( valores únicos no dataframe)

    ACSSET = set(ACS)
    for acNAME in ACSSET:
        if acNAME not in ACSSET:
            print(acNAME)
            insert_ac_name(acNAME)

    # verificar o status dos links dos pdfs no arquivo excel
    for ind in df.index:
        AC = df['AC'][ind]
        URL = df['URL'][ind]
        pdfStatus = requestURL(URL)
        print(pdfStatus)
        insert_pdf_certificado_link(AC, URL, pdfStatus)



except:
    print ("I am unable to connect to the database")
#*************************ler aquivo excel *********************************************
#colocar num arquivo txt.conf



