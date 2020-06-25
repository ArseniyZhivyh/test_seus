# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:42:14 2020

@author: ars14
"""
import fitz
import pandas as pd
import os
from sqlalchemy import create_engine
import psycopg2
import numpy as np

#перечисление серверов и создание датафрейма
prox = ['88.198.24.108', '138.68.41.90', '191.96.42.80', '198.199.86.11']
df = pd.DataFrame(columns = ['IP', 'document_num', 'Period', 'Name', 'Address', 'Date_reestr', 'Num_reestr', 'INN', 'KPP', 'money', 'aim', 'face1', 'face2' ])
c = 0 #счётчик индексов датафрейма

#для каждого файла в папке для каждого сервера
for i in prox:
    directory = './отчёты/'+str(i)
    files = os.listdir(directory)
    for f in files:
        df.loc[c, 'IP'] = i
        df.loc[c, 'document_num'] = str(f)
        #открытие документа, соединение текста двух страниц, удаление номера страницы 2
        pdf_document = directory + '/' + f
        doc = fitz.open(pdf_document)
        page = doc.loadPage(0)
        page_text1 = page.getText("text")
        page = doc.loadPage(1)
        page_text2 = page.getText("text")
        page_text_to_del = page_text2[0:33]
        page_text2 = page_text2.replace(page_text_to_del, "")
        page_text = page_text1 + page_text2
        
        isp_index = page_text.find('использования')
        dot_index = page_text.find('г.')
        df.loc[c, 'Period'] = page_text[(isp_index+16):(dot_index+1)] #выделение отчётного периода
        
        full_name_index = page_text.find('(полное')
        df.loc[c, 'Name'] = page_text[(dot_index+3):full_name_index] #выделение название организации
        
        adress_index = page_text.find('(адрес') #выеделение адреса организации
        df.loc[c, 'Address'] = page_text[(full_name_index+len('полное наименование структурного подразделения')+2):adress_index]
        
        rees_index = page_text.find('Реестровый')
        rees_len = len('Реестровый номер структурного подразделения в реестре филиалов и представительств международных организаций и иностранных некоммерческих неправительственных организаций')
        df.loc[c, 'Date_reestr'] = page_text[(rees_index+rees_len+1):rees_index+rees_len+11] #выделение даты внесения в реестр
        INN_index = page_text.find('ИНН/КПП')
        df.loc[c, 'Num_reestr'] = page_text[(rees_index+rees_len+11):INN_index] #выеделение номера в реестре
        df.loc[c, 'INN'] = page_text[(INN_index+9):(INN_index+28):2] #выделение ИНН
        df.loc[c, 'KPP'] = page_text[(INN_index+31):(INN_index+51):2] #выделение КПП
        
        aim_index = page_text.find('Целевые средства, поступившие в отчетном периоде')
        prb_index = page_text.find('\n', (aim_index+49))
        df.loc[c, 'money'] = page_text[(aim_index+49):prb_index] #выделение суммы средств
        
        inoe_index = page_text.find('Иное')
        df.loc[c, 'aim'] = page_text[(prb_index+1):(inoe_index-3)] #выделение цели
        
        face1 ='руководитель филиала'
        face1_index = page_text.find(face1)
        dol ='(фамилия, имя, отчество, занимаемая должность)'
        dol1_index = page_text.find(dol)
        df.loc[c, 'face1'] = page_text[(face1_index+101):dol1_index] #выделение первого согласующего лица
        dol2_index = page_text.rfind(dol)
        df.loc[c, 'face2'] = page_text[(dol1_index+128):dol2_index] #выделение второго согласующего лица
        
        c += 1 #увеличение индекса

#удаление нулевых отчётов
df = df.loc[df['money'] != '0']
df = df.loc[df['money'] != '0,00']

#очистка отчётов с неопределёнными ИНН, КПП и датой внесения в реестр и номером
df.loc[df['INN'] == '/1Днжы рдт', 'KPP'] = 0
df.loc[df['INN'] == '/1Днжы рдт', 'INN'] = 0
df.loc[df['Num_reestr'] == '', 'Date_reestr'] = 0
df.loc[df['INN'] == '9909043738', 'Num_reestr'] = 170
df.loc[df['INN'] == '9909025552', 'Num_reestr'] = 0
df.loc[df['INN'] == '9909005997', 'Num_reestr'] = 0
df.loc[df['INN'] == '9909291096', 'Num_reestr'] = 0
df.loc[df['INN'] == '9909195307', 'Num_reestr'] = 0


#подготовка данных для выгрузки в БД
IP_to_db = pd.DataFrame(df['IP'].unique())
company_to_db = df[['Name', 'Address', 'Date_reestr', 'Num_reestr', 'INN', 'KPP']]
company_to_db = df[['Name', 'Address', 'Date_reestr', 'Num_reestr', 'INN', 'KPP']].drop_duplicates()
doc_to_db = df[['document_num', 'IP', 'Name', 'Period', 'money', 'aim', 'face1', 'face2']]
face_to_db = pd.unique(df['face1']).tolist()
face_to_db.extend(pd.unique(df['face2']).tolist())
face_to_db = pd.DataFrame(np.unique(np.array(face_to_db)).tolist())

#выгрузка в БД
engine = create_engine('postgresql://postgres:14011998@localhost:5433/DBparse')
company_to_db.to_sql('company', engine)
IP_to_db.to_sql('IP', engine)
doc_to_db.to_sql('document', engine)
face_to_db.to_sql('face', engine)