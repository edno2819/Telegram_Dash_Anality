from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


LOGGER.setLevel(logging.WARNING)

class Webdriver():
    def __init__(self, profiles=False, headless=False, kwargs={}):

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless") if headless==True else self.options.add_argument("--start-maximized")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])  
  
        self.kwargs=kwargs
        
        if profiles:
            dir_path = os.getcwd()
            profile = os.path.join(dir_path, "profile", "wpp")        
            self.options.add_argument(r"--user-data-dir={}".format(profile))  


        self.update_webdriver()
    
    def start(self):
        # service = Service('chromedriver.exe')
        # service.creationflags = CREATE_NO_WINDOW'service=service
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options, **self.kwargs)
        self.wait = WebDriverWait(self.driver, 10)
    
    def update_webdriver(self):
        try:
            if 'browserVersion' in self.driver.capabilities:
                version=self.driver.capabilities['browserVersion']
            else:
                version=self.driver.capabilities['version']

            gdd = ChromeDriverManager()
            gdd.download_and_install(version)
        except:
            pass 

    def open_page(self,url):
        self.driver.get(url)
    
    def find_element(self, locator, elem=None):
        by, locator = locator
        if elem:
            return elem.find_element(by, locator)
        else:
            return self.driver.find_element(by, locator)

    def find_elements(self, locator, elem=None):
        by, locator = locator
        if elem:
            return elem.find_elements(by, locator)
        else:
            return self.driver.find_elements(by, locator)

    def move_element(self, elem, y=-100):
        if type(elem)==tuple:
            elem = self.find_element(elem)

        loc=elem.location_once_scrolled_into_view
        self.driver.execute_script(f"window.scrollBy({loc['x']},{y})")

    def click(self, locator, hover_to=True):
        elem = locator
        if type(locator) is tuple:
            elem = EC.element_to_be_clickable(locator)
            elem = self.exist(locator, wait=3, retur= True)
        if hover_to:
            self.move_element(elem)
        elem.click()
        
    def exist(self, element, wait=10, retur = False):
        try:
            element = WebDriverWait(self.driver, wait).until(
                EC.presence_of_element_located(element)
                    )
            if retur: return element
            return True
        except:
            return False

    def fill(self, element, text):
        if type(element)==tuple:
            elem = EC.element_to_be_clickable(element)
            elem = self.wait.until(elem)

        self.move_element(elem)
        elem.click()
        elem.clear()
        elem.send_keys(text)

    def get_element_attribute(self, locator, attribute):
        elem = locator
        if type(locator) is tuple:
            elem = EC.presence_of_element_located(locator)
            elem = self.wait.until(elem)
        attribute = elem.get_attribute(attribute)
        return attribute

    def send_key(self, key, element=None):
        if element:
            return self.driver.find_element(element[0],element[1]).send_keys(key)
        else:
            return ActionChains(self.driver).send_keys(key).perform()

    def refresh(self):
        self.driver.refresh()

    def switch_to_frame(self, frame="root_frame"):
        if frame == 'root_frame':
            self.driver.switch_to_window(self.driver.window_handles[0])
        else:
            self.driver.switch_to.frame(frame)

    def wait_download(self):
        file = os.listdir(self.webdriver.downloads_path)[0]
        if '.tmp' not in file:
            if '.crdownload' not in file:
                time.sleep(1)
                return file
    def zoom(self,zoom):
        self.driver.execute_script(f"document.body.style.zoom='{zoom}'")

    def screenshot(self, file, zoom='100%'):
        self.zoom(zoom)
        self.driver.save_screenshot(file)
        self.zoom('100%')

    def close(self):
        self.driver.quit()


