from datetime import datetime
import csv
import shutil, os




def time_now(formato):
    return datetime.now().strftime(formato)


def consult_csv():
    configs={}
    gnore = [' ', '[', '#']
    with open('configs.txt', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        for row in spamreader:
            if row!=[]:
                if row[0][0] not in gnore:
                    dic = row[0].split('=')
                    value = dic[1].strip().split(',')

                    configs[dic[0].strip()] = '' if len(dic)<2 else value
    return configs


def set_folder(folder_path, rewrite=False):
    if os.path.exists(folder_path) and rewrite:
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

def qtd_msg_to_int(string):
    a = string.split('K')
    if len(a)>1:
        return float(a[0].replace(',','.')) * 1000
    else:
        return float(a[0].replace(',','.'))

