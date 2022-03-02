from libraries.tele_task import TelegramTask
import traceback
import function as func
from utils import *
from database import MysqlClass


CONFIGS = func.consult_csv()

class Main():
    def __init__(self):
        self.banco = MysqlClass(CONFIGS['host'][0], CONFIGS['user'][0], CONFIGS['password'][0], CONFIGS['database'][0])
        self.tele = TelegramTask(True, False)

    def start(self): 
        self.tele.open_telegram()
    
    def check_conection(self):
        if not self.tele.open_canal_sinal('InPlayScanner_BOT'):
            func.salve_csv(f'\nErro no Open Canal telegram!')
            return False

    def conect_new_telegram(self):
        self.tele_visi=TelegramTask(profiles=True, headless= False)
        self.tele_visi.open_telegram()
        input('Esperando conexão! Após conectar, Reinicie o programa!')
        self.tele_visi.tele.close()

    def get_msgs(self, grupo):
        qtd = self.tele.open_canal(grupo)
        print(f'Grupo {grupo} - {qtd} Mensagens')
        return self.tele.get_mensagens(qtd)
    
    def create_grup_in_db(self, grupo):
        self.check_connection_db()
        grupo_id = self.banco.get_data_by_colum_filter('Grupos', 'nome', grupo, 'id')
        if grupo_id == []:
           self.banco.insert_data('Grupos', f'''("{grupo}", "{time_now('%Y-%m-%d %H:%M:%S')}")''', '(nome, OrderDate)') 
           self.banco.commit()

    def save_msg_db(self, grupo, mensagens):
        self.check_connection_db()
        grupo_id = self.banco.get_data_by_colum_filter('Grupos', 'nome', grupo, 'id')[0][0]
        all_msg = ''
        for msg in mensagens:
            msg = msg.replace("'", '').replace('"', '')
            user = msg[:(msg.find('\n'))]
            all_msg += ','+ f'''("{user}", "{msg}", "{time_now('%Y-%m-%d %H:%M:%S')}", {grupo_id})'''
        self.banco.insert_data('Mensagens', all_msg[1:], '(user, mensagem, OrderDate, id_group)') 
        self.banco.commit()

    def close(self):
        self.tele.tele.close()
        self.banco.close()
    
    def check_connection_db(self):
        if not self.banco.check_connected():
            self.banco.conect()
 


bot = Main()

if not func.check_profile():
    bot.conect_new_telegram()

bot.start() 
print('Iniciando Bot')

try: 
    for grupo in CONFIGS['CANAIS']:
        print(f'\n{time_now("%H:%M:%S")} Iniciando buscas em {grupo}!')
        mensagens = bot.get_msgs(grupo)
        bot.create_grup_in_db(grupo)
        bot.save_msg_db(grupo, mensagens)
    print(f'\n{time_now("%H:%M:%S")} Busca finalizada!')
    bot.close()
except Exception:
    bot.close()
    print('\nError! Mostre para o desenvolvedor.\n')
    traceback.print_exc()    
    
input()