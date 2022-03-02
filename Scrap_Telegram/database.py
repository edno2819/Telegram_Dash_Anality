import mysql.connector

class MysqlClass:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conect()
    
    def conect(self):
        self.mydb  =  mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )

        self.cur = self.mydb.cursor(buffered=True)

    def create_database(self, name):
      self.cur.execute(f"CREATE DATABASE IF NOT EXISTS{name}")
        

    def create_table(self, table):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {table} (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                nome text (32),
                                                                data TEXT
                                                                )''')


    def show_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return self.cur.fetchall()
        

    def show_table(self, table):
        self.cur.execute(f'select * from {table}')
        return self.cur.fetchall()
      

    def insert_data(self, tabela:str,  new_data:str, columns:str=''):
        self.cur.execute(f'''INSERT INTO {tabela} {columns} VALUES {new_data}''')
        # self.commit()


    def get_data_by_colum_filter(self, tabela:str, colum:str, search:str, itens:str='*'):
        self.cur.execute(f'''select {itens} from {tabela} where {colum} like "%{search}%"''')
        return self.cur.fetchall()


    def get_all_data_from_table(self, tabela:str, coluns:str='*'):
        self.cur.execute(f'''select {coluns} from {tabela}''')
        return self.cur.fetchall()


    def get_data(self, codigo:str):
        self.cur.execute(codigo)
        return self.cur.fetchall()

    def close(self):
      self.mydb.close()

    def check_connected(self):
      self.mydb.is_connected()

    def commit(self):
      self.mydb.commit()


                        