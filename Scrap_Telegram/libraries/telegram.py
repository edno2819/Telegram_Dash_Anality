from libraries.web_base import Webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class Telegram:
    URL='https://web.telegram.org/z/'
    BARRA_DE_BUSCA= (By.XPATH, '//*[@id="telegram-search-input"]')
    FIST_ITEM_CHAT_SEARCH = (By.XPATH,'(//*[@class="ListItem chat-item-clickable search-result no-selection"])[1]')

    MSG = (By.XPATH,'//*[@class="text-content with-meta"]')
    MSG_AND_PEOPLE = (By.XPATH,'//*[@class="message-content-wrapper can-select-text"]')
    DESCER_MSG = (By.XPATH,'//*[@class="ScrollDownButton-inner"]')
    EXIST_SCROLL_DOWM=(By.XPATH,'//*[@class="unread-count"]')

    SEARCH_IN_CHAT = (By.XPATH, '//*[@class="Button smaller translucent round"]')
    SEARCH_IN_CHAT_CLOSE = (By.XPATH, '//*[@class="Button close-button smaller translucent round"]')
    JUMP_TO_DATE = (By.XPATH, '//*[@class="Button default primary"]')

    MSGS_UNREAD = (By.XPATH, "//*[@class='unread-count']")

    TODAY = (By.XPATH, "//span[text()='Today']")

    def __init__(self, profiles=False, headless=False):
        self.driver = Webdriver(profiles, headless)
    
    def open_telegram(self):
        self.driver.start()
        self.driver.open_page(self.URL)
    
    def open_canal_sinal(self, nome):
        try:
            self.driver.click(self.BARRA_DE_BUSCA)
            self.driver.fill(self.BARRA_DE_BUSCA, nome)
            elem = self.driver.exist(self.FIST_ITEM_CHAT_SEARCH, wait=10, retur=True)
            self.driver.click(elem)
            return True
        except:
            self.driver.screenshot(f'screen/ERRO OPEN CANAL.png')
            return False

    def scroll_dowm(self):
        try:
            while self.driver.exist(self.EXIST_SCROLL_DOWM, wait=3):
                self.driver.click(self.DESCER_MSG)
            return True
        except:
            return False

    def check_conected(self):
        return self.driver.exist(self.BARRA_DE_BUSCA)

    def open_chat(self, name):
        self.driver.click(self.BARRA_DE_BUSCA)
        self.driver.fill(self.BARRA_DE_BUSCA, name)
        if self.driver.exist(self.FIST_ITEM_CHAT_SEARCH, wait=3):
            self.driver.send_key(Keys.ENTER,self.BARRA_DE_BUSCA)
        return False

    def send_menssege(self,text):
        self.driver.send_key(text)
        self.driver.send_key(Keys.ENTER)
    
    def get_menssagens_elem(self):
        elens=self.driver.find_elements(self.MSG_AND_PEOPLE)
        if elens==[]:  
            return False
        return elens

    def get_menssagens(self):
        elens=self.get_menssagens_elem()
        if elens==[] or not elens:  
            return False
        lista = []
        for item in elens:
            try:
                lista.append(item.text)
            except: pass
        return lista


    def atualizar(self):
        self.driver.refresh()

    def click_jump_to_date(self):
        self.driver.click(self.JUMP_TO_DATE)

    def click_search_in_chat(self):
        self.driver.click(self.SEARCH_IN_CHAT)

    def msgs_unread(self):
        def qtd_msg_to_int(string):
            a = string.split('K')
            if len(a)>1:
                return float(a[0].replace(',','.')) * 1000
            else:
                return float(a[0].replace(',','.'))

        qtd = self.driver.exist(self.MSGS_UNREAD, wait=2, retur=True)
        
        return qtd_msg_to_int(qtd.text) if qtd!=False else qtd

    def click_search_in_chat_close(self):
        self.driver.click(self.SEARCH_IN_CHAT_CLOSE)

    def close(self):
        self.driver.close()



