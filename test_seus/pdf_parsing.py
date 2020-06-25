# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 09:32:54 2020

@author: ars14
"""
import fitz

pdf_document = "./отчёты/88.198.24.108/18177901.pdf"
doc = fitz.open(pdf_document)
page = doc.loadPage(0)
page_text1 = page.getText("text")

page = doc.loadPage(1)
page_text2 = page.getText("text")
page_text_to_del = page_text2[0:33]
page_text2 = page_text2.replace(page_text_to_del, "")
page_text = page_text1 + page_text2

isp_index = page_text.find('использования')
dot_index = page_text.find('.')
date_otch = page_text[(isp_index+16):dot_index]

full_name_index = page_text.find('(полное')
full_name = page_text[(dot_index+2):full_name_index]

adress_index = page_text.find('(адрес')
adress = page_text[(full_name_index+len('полное наименование структурного подразделения')+2):adress_index]

rees_index = page_text.find('Реестровый')
rees_len = len('Реестровый номер структурного подразделения в реестре филиалов и представительств международных организаций и иностранных некоммерческих неправительственных организаций')
rees_date = page_text[(rees_index+rees_len+1):rees_index+rees_len+11]
INN_index = page_text.find('ИНН/КПП')
rees_num = page_text[(rees_index+rees_len+11):INN_index]
INN_num = page_text[(INN_index+9):(INN_index+28):2]
KPP_num = page_text[(INN_index+31):(INN_index+51):2]

aim_index = page_text.find('Целевые средства, поступившие в отчетном периоде')
prb_index = page_text.find('\n', (aim_index+49))
den_summ = page_text[(aim_index+49):prb_index]

inoe_index = page_text.find('Иное')
aim = page_text[(prb_index+1):(inoe_index-3)]

face1 ='руководитель филиала'
face1_index = page_text.find(face1)
dol ='(фамилия, имя, отчество, занимаемая должность)'
dol1_index = page_text.find(dol)
face1_dol = page_text[(face1_index+101):dol1_index]
dol2_index = page_text.rfind(dol)
face2_dol = page_text[(dol1_index+128):dol2_index]

stroka = [date_otch, full_name, adress, rees_date, rees_num, INN_num, KPP_num, den_summ, aim, face1_dol, face2_dol]