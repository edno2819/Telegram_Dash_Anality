from database import MysqlClass
import pandas as pd
import csv


def consult_csv(path='configs.txt'):
    configs={}
    gnore = [' ', '[', '#']
    with open(path, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        for row in spamreader:
            if row!=[]:
                if row[0][0] not in gnore:
                    dic = row[0].split('=')
                    value = dic[1].split(',')
                    value = [val.strip() for val in value]

                    configs[dic[0].strip()] = '' if len(dic)<2 else value
    return configs

CONFIGS = consult_csv()

class Processing_data:
    def __init__(self):
        self.banco = MysqlClass(CONFIGS['host'][0], CONFIGS['user'][0], CONFIGS['password'][0], CONFIGS['database'][0])
        self.CANAIS = {grupo:id for id,grupo in self.banco.get_all_data_from_table('Grupos', 'id, nome')}
    
    def all_msgs_from_canais(self, canais_id, date_range):
        data = list()
        for id in canais_id:
            data += self.banco.get_data_by_colum_filter('Mensagens', 'id_group', id, 'mensagem', date_range=date_range)
        return [msg[0] for msg in data]

    def frequencia_temas(self, canais, date_range:tuple):
        data = []
        for canal in canais:
            x = self.banco.get_data_by_colum_filter('Mensagens', 'id_group', self.CANAIS[canal], 'OrderDate', date_range=date_range)
            x = [dados[0] for dados in x]
            data += x
        data = list(set(data))
        data.sort()
        return  data

    def all_msgs_dict_from_canais(self, canais, date_range,  coluns='mensagem'):
        data = {}
        for canal in canais:
            data[canal] = self.banco.get_data_by_colum_filter('Mensagens', 'id_group', self.CANAIS[canal], coluns, date_range=date_range)
            data[canal] = list(set([msg[0] for msg in data[canal]]))
        return data

    def all_msgs_dict_from_canais_temas(self, canais, date_range, coluns='mensagem'):
        data = {}
        for canal in canais:
            data[canal] = self.banco.get_data_by_colum_filter('Mensagens', 'id_group', self.CANAIS[canal], coluns, date_range=date_range)
        return data

    def all_msgs_from_all_canais(self):
        data = list()
        df = pd.DataFrame({'Grupo':[], 'Mensagens':[]})
        limit_before = self.banco.limite
        self.banco.limite = int((80000/len(self.CANAIS.keys())))

        for id in self.CANAIS.keys():
            data = self.banco.get_data_by_colum_filter('Mensagens', 'id_group', self.CANAIS[id], 'mensagem')
            df = df.append([{'Grupo':id, 'Mensagens':msg[0]} for msg in data])
            
        self.banco.limite = limit_before
        return df


    def filter_list_strings(self, lista, strings):
        if strings==False:
            return lista

        new_list = list()

        for item in lista:
            inpu = True
            for string_filter in strings:
                if string_filter.upper().strip() not in item.upper().split(' '):
                    inpu = False
            if inpu:
                new_list.append(item)
        return new_list


    def filter_list_strings_temas(self, lista, strings):
        if strings==False:
            return lista

        new_list = list()

        for item in lista:
            if strings.upper().strip() in item[0].upper():
                new_list.append(item)
        return new_list

    def super_uses(self, canais, date_range):
        if canais not in [[],None]:
            canais_ids = '(' + ','.join([str(self.CANAIS[canal]) for canal in canais]) + ')'
            self.banco.cur.execute(
                f'''select user, COUNT(user) AS SUPER_USER
                from Mensagens 
                WHERE id_group in {canais_ids} AND
                (OrderDate >= "{date_range[0]}") AND 
                (OrderDate <= "{date_range[1]}")
                GROUP BY user
                ORDER BY COUNT(user) DESC''')
        else:
            self.banco.cur.execute(
                '''select user, COUNT(user) AS SUPER_USER
                from Mensagens
                GROUP BY user
                ORDER BY COUNT(user) DESC''')

        result = self.banco.cur.fetchall()

        return result


Analy = Processing_data()
