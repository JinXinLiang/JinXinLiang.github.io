# coding: utf-8
import os
import csv
import json
from unicodedata import decimal

import pandas as pd
# from tools.Config import BASE_PATH


def csv_to_json(csv_path, json_path, date_name):
    csv_file = open(csv_path, 'r',encoding='utf-8')  # encoding="gbk",errors='ignore'
    json_file = open(json_path, 'w')
    first_name = pd.read_csv(csv_path)
    fieldnames1 = first_name.columns
    reader = csv.DictReader(csv_file, tuple(fieldnames1))
    json_file.write("var %s = [\n" % date_name)
    mark = 1
    for row in reader:
        if mark == 1:
            mark = 0
            continue
        try:
            row.update({'lng': float(row['lng']), 'lat': float(row['lat']), 'value': float(row['value'])})
        except:
            pass
        json.dump(row, json_file)
        json_file.write(',')
        json_file.write('\n')
    json_file.write(']')
    json_file.close()
    csv_file.close()

def csv_to_strjson(csv_path, json_path, date_name):
    csv_file = open(csv_path, 'r',encoding='utf-8')  # encoding="gbk",errors='ignore'
    json_file = open(json_path, 'w')
    first_name = pd.read_csv(csv_path,dtype={'value':str})
    fieldnames1 = first_name.columns
    reader = csv.DictReader(csv_file, tuple(fieldnames1))
    json_file.write("var %s = [\n" % date_name)
    mark = 1
    for row in reader:
        if mark == 1:
            mark = 0
            continue
        try:
            row.update({'lng': float(row['lng']), 'lat': float(row['lat']), 'value': str(row['value'])})
        except:
            pass
        json.dump(row, json_file)
        json_file.write(',')
        json_file.write('\n')
    json_file.write(']')
    json_file.close()
    csv_file.close()



def csv_to_networkjson(csv_path, json_path, date_name):
    csv_file = open(csv_path, 'r',encoding='utf-8')  # encoding="gbk",errors='ignore'
    json_file = open(json_path, 'w')
    first_name = pd.read_csv(csv_path)
    fieldnames1 = first_name.columns
    reader = csv.DictReader(csv_file, tuple(fieldnames1))
    json_file.write("var %s = [\n" % date_name)
    mark = 1
    for row in reader:
        if mark == 1:
            mark = 0
            continue
        try:
            row.update({'lgt': float(row['lng']), 'name': str(row['name']), 'ID4': int(row['ID4']),'ID6': int(row['ID6']),
                        'eletric':float(row['eletric'])})
        except:
            pass
        json.dump(row, json_file)
        json_file.write(',')
        json_file.write('\n')
    json_file.write(']')
    json_file.close()
    csv_file.close()

if __name__ == '__main__':
    # csv_name = 'address_demo'
    # js_name = 'success_cancel_point'

    csv_name = '停车场经纬度(未去重)'
    js_name = '停车场经纬度(未去重)'
    # csv_to_json(csv_name, js_name)
