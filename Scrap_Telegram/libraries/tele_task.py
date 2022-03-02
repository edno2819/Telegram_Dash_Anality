from libraries.telegram import Telegram



class TelegramTask:
    def __init__(self, profiles=True, headless=True):
        self.tele = Telegram(profiles, headless=headless)
    
    def open_telegram(self):
        self.tele.open_telegram()
    
    def open_canal(self, canal):
        for c in range(5):
            if self.tele.open_canal_sinal(canal):
                break
            self.tele.driver.refresh()
        qtd = self.tele.msgs_unread()
        self.tele.scroll_dowm()
        return qtd

    def get_text(self, elens):
        if elens==[] or not elens:  
            return []
            return False
        lista = []
        for item in elens:
            try:
                lista.append(item.text)
            except: pass
        return lista

    def get_mensagens(self, qtd):
        msgs = list()
        count_repeat, elens_old = 0, 0
        while True:
            elens = self.tele.get_menssagens_elem()

            if elens==elens_old:
                count_repeat += 1
                self.tele.driver.move_element(elens[count_repeat])
            else:
                self.tele.driver.move_element(elens[0])
                count_repeat = 0

            msgs+=self.get_text(elens)
            msgs = list(set(msgs))
            
            if len(msgs) >= qtd or count_repeat>=6:
                break

            elens_old = elens

        return msgs



