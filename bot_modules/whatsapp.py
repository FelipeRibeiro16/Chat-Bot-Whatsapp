# %%
from datetime import datetime, time
import glob
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotVisibleException, ElementNotSelectableException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
import io
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import re
os.environ['WDM_LOCAL'] = '1'


class WhatsApp:
    def __init__(self) -> None:
        return None

    def start(self) -> bool:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument('window-size=1920x2160')
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            f"--user-data-dir={os.getcwd()}\\data\\bot-data")
        prefs = {"profile.default_content_settings.popups": 0,
                 "download.default_directory": f"{os.getcwd()}\\data\\downloads",
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True}
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager(path=f"{os.getcwd()}\\data\\Drivers", cache_valid_range=365).install()), options=chrome_options)

        self.driver.get("https://web.whatsapp.com/")

        return self.__autentication()

    def __autentication(self) -> bool:
        try:
            WebDriverWait(self.driver, 60).until(
                EC.any_of(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#app > div > div > div._2Ts6i._3RGKj")),
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#app > div > div > div.landing-window > div.landing-main > div > div > div._2I5ox > div > canvas"))
                ))
        except TimeoutException:
            pass
        else:
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div > div.landing-window > div.landing-main > div > div > div._2I5ox > div > canvas")))
            except TimeoutException:
                return True
            try:
                qr_code_element = self.driver.find_element(By.
                                                           CSS_SELECTOR,
                                                           """
                                #app > div > div > div.landing-window > div.landing-main > div > div > div._2I5ox > div > canvas
                                """)
            except NoSuchElementException:
                pass
            else:
                screenshot = qr_code_element.screenshot_as_png
                image = Image.open(io.BytesIO(screenshot))
                qr_code_data = decode(image)
                qr_code_text = qr_code_data[0].data.decode("utf-8")
                qr_code = qrcode.QRCode()
                qr_code.add_data(qr_code_text)
                f = io.StringIO()
                qr_code.print_ascii(out=f)
                f.seek(0)
                os.system('cls')
                print(f.read())
            try:
                WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#app > div > div > div._2Ts6i._3RGKj")))
            except TimeoutException:
                self.__autentication()
            else:
                return True

    def close(self) -> None:
        self.driver.close()


class Chat:
    def __init__(self, driver):
        self.driver = driver
        self._chats = []

    def update(self) -> bool:
        def if_muted(element) -> bool:
            if element.find_elements(By.XPATH, """
            *//span[@data-testid="muted"]
            """):
                return True
            return False

        def is_group(text: list) -> bool:
            if len(text) > 4:
                return True
            return False

        def unread_messages(text: list) -> int:
            try:
                return int(text[-1])
            except ValueError:
                return 0

        def last_message(text: list) -> str:
            if is_group(text):
                return text[4]
            return text[2]

        def last_message_time(text: list) -> str:
            seconds = datetime.now().time().second
            if self.verify_last_message(text):
                return time(int(text.split(":")[0]), int(
                    text.split(":")[1]), seconds)
            return text
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 """
                 #pane-side > div:nth-child(1) > div > div > div:nth-child(1)
                 """
                 )))
        except TimeoutException:
            return False
        else:
            first_chat = self.driver.find_element(By.CSS_SELECTOR,
                                                  """
                                                  #pane-side > div:nth-child(1) > div > div > div:nth-child(1)
                                                  """
                                                  )
            first_chat_class = first_chat.get_attribute("class")
            active_chats = self.driver.find_elements(By.XPATH,
                                                     f"""
                                                                 //div[@class="{first_chat_class}"]
                                                    
                                                                 """)
            try:
                for chats in active_chats:
                    if (not self.if_exists(chats)) or len(active_chats) != len(self._chats):
                        break
                else:
                    for chat in self._chats:
                        if chat['id'].text == chat['raw_text']:
                            continue
                        chats_text = chat['id'].text.split("\n")
                        chat['raw_text'] = chat['id'].text
                        chat['title'] = chats_text[0]
                        chat['is_group'] = is_group(chats_text)
                        chat['silenced'] = if_muted(chat['id'])
                        chat['unread_messages'] = unread_messages(chats_text)
                        chat['last_message'] = last_message(chats_text)
                        chat['date_last_message'] = last_message_time(
                            chats_text[1])
                    return True
                new_chats = []
                for chats in active_chats:
                    chats_text = chats.text.split("\n")
                    chat = {}
                    chat['id'] = chats
                    chat['raw_text'] = chats.text
                    chat['title'] = chats_text[0]
                    chat['is_group'] = is_group(chats_text)
                    chat['silenced'] = if_muted(chats)
                    chat['unread_messages'] = unread_messages(chats_text)
                    chat['last_message'] = last_message(chats_text)
                    chat['date_last_message'] = last_message_time(
                        chats_text[1])
                    chat['messages'] = self.return_messages(chats)
                    new_chats.append(chat)
                self.reset()
                for chat in new_chats:
                    self.add(chat)
                return True
            except StaleElementReferenceException:
                return self.update()

    def return_messages(self, id_chat: any) -> list:
        for chats in self._chats:
            if chats['id'] == id_chat:
                return chats['messages']
        return []

    def add(self, chat: dict) -> None:
        if not self.if_exists(chat['id']):
            self._chats.append(chat)
        return None

    def if_exists(self, chat_id: any) -> bool:
        for chat in self._chats:
            if chat['id'] == chat_id:
                return True
        return False

    def remove(self, chat: dict) -> None:
        if self.if_exists(chat):
            self.hold = chat
            self._chats.remove(chat)
            try:
                WebDriverWait(self.driver, 1).until(
                    EC.staleness_of(self.hold['id']))
            except WebDriverException:
                self.add(self.hold)
            else:
                self.update()
        return None

    def reset(self) -> None:
        self._chats = []
        return None

    def display(self, by: str = None) -> None:
        def __display_groups() -> None:
            for chat in self._chats:
                if chat['is_group']:
                    windows = f"{chat['title']}{' Silenciado' if chat['silenced'] else ''}\nUltima mensagem: {chat['last_message']}, {chat['date_last_message']}\n"
                    print(windows)
            return None

        def __display_chats() -> None:
            for chat in self._chats:
                if not chat['is_group']:
                    windows = f"{chat['title']}{' Silenciado' if chat['silenced'] else ''}\nUltima mensagem: {chat['last_message']}, {chat['date_last_message']}\n"
                    print(windows)
            return None

        def __display_all() -> None:
            for chat in self._chats:
                windows = f"{chat['title']}{' Silenciado' if chat['silenced'] else ''}\nUltima mensagem: {chat['last_message']}, {chat['date_last_message']}\n"
                print(windows)
            return None
        if by == "groups":
            return __display_groups()
        if by == "chats":
            return __display_chats()
        return __display_all()

    def verify_last_message(self, last_message: str) -> bool:
        pattern = r"\d{2}:\d{2}"
        if re.fullmatch(pattern, last_message):
            return True
        return False

    def listen_chats(self, corresponded: str, timeout: int = 43200) -> dict:
        self.update()
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((By.XPATH,
                                                  """
                        //div[@data-testid="chat-list"]
                        """), corresponded))
        except TimeoutException:
            WhatsApp.close()
            return False
        finally:
            self.update()
            for chats_listening in self._chats:
                if corresponded in chats_listening['last_message']:
                    return chats_listening
            else:
                return self.listen_chats(corresponded, timeout)

    def listen_messages(self, chat: dict, correspond: str, timeout: int = 0) -> dict:
        self.update_messages(chat)
        while True:
            if chat['messages'] is None:
                return False
            for message in chat['messages']:
                if message['replied']:
                    continue
                if correspond in message['message']:
                    return message
            else:
                sleep(timeout)
                self.update_messages(chat)

    def reply_message(self, chat: dict, reply: str) -> bool:
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", chat['id'])
        actionChains = ActionChains(self.driver)
        actionChains.double_click(chat['id']).perform()
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                """
                                                                                //div[@title='Mensagem']
                                                                                """)))
        except TimeoutException:
            return False
        else:
            message_box = self.driver.find_element(By.XPATH,
                                                   """
                                     .//div[@title='Mensagem']
                                     """
                                                   )
            message_box.send_keys(reply)
            message_box.send_keys(Keys.ENTER)
        return True

    def update_messages(self, chat: dict) -> bool:
        def is_audio(text: str) -> bool:
            pattern1 = r"\d{2}:\d{2}"
            pattern2 = r"\d{1}:\d{2}"
            if re.fullmatch(pattern1, text) or re.fullmatch(pattern2, text):
                return True
            return False

        def message_time(text: str) -> any:
            seconds = datetime.now().time().second
            return time(int(text.split(":")[0]), int(text.split(":")[1]), seconds)

        def verify_time(time: datetime) -> bool:
            time_chat = datetime.combine(
                datetime.today(), chat['date_last_message'])
            time_message = datetime.combine(datetime.today(), time)
            seconds_difference = (time_chat - time_message)
            if seconds_difference.seconds > 120:
                return True
            return False

        self.driver.execute_script(
            "arguments[0].scrollIntoView();", chat['id'])
        actionChains = ActionChains(self.driver)
        actionChains.double_click(chat['id']).perform()
        try:
            WebDriverWait(self.driver, 5).until(EC.text_to_be_present_in_element((By.XPATH,
                                                                                  """
                                                                                //span[@data-testid='conversation-info-header-chat-title']
                                                                                """), chat['title']))
        except TimeoutException:
            return False
        finally:
            aplication = self.driver.find_element(By.XPATH,
                                                  """
                                     //div[@role='application']
                                     """
                                                  )
            message_boxes = aplication.find_elements(By.XPATH,
                                                     """
                                     .//div[@role='row']
                                     """
                                                     )
            for message_box in message_boxes:
                messages = {}
                try:
                    element = message_box.find_element(By.XPATH,
                                                       """
                                            .//div[@data-testid='msg-container']
                                            """)
                except NoSuchElementException:
                    continue
                if self.if_exists_message(chat, element):
                    continue
                text = message_box.text.split("\n")
                if len(text) != 2:
                    continue
                messages['time'] = message_time(text[1])
                if verify_time(messages['time']):
                    continue
                messages['id'] = element
                messages['message'] = 'audio' if is_audio(
                    text[0]) else text[0].lower()
                messages['replied'] = False
                self.add_message(chat, messages)
            self.update()
            return True

    def mark_as_replied(self, chat: dict, message: dict) -> bool:
        if_exists_message = self.if_exists_message(chat, message['id'])
        if if_exists_message:
            self._chats[self._chats.index(chat)]['messages'][chat['messages'].index(
                message)]['replied'] = True
            return True
        return False

    def if_exists_message(self, chat: dict, message_id: any) -> bool:
        ids_chat = [elements['id'] for elements in chat['messages']]
        if message_id in ids_chat:
            return True
        return False

    def add_message(self, chat: dict, message: dict) -> None:
        if not self.if_exists_message(chat, message['id']):
            chat['messages'].append(message)
        return None

    def create_sticker(self, message: dict) -> bool:
        def delete_images() -> None:
            images = glob.glob(f"{os.getcwd()}\\data\\downloads\\*.jpeg")
            for image in images:
                os.remove(image)
            return None
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", message['id'])
        message['id'].click()
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                            """
                                                                                //span[@data-testid='download']
                                                                                """)))
        except TimeoutException:
            return False
        else:
            self.driver.find_element(By.XPATH,
                                     """
                                     //span[@data-testid='download']
                                     """
                                     ).click()
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                            """
                                                                                //span[@data-testid='x-viewer']
                                                                                """)))
        except TimeoutException:
            delete_images()
            return False
        else:
            self.driver.find_element(By.XPATH,
                                     """
                                     //span[@data-testid='x-viewer']
                                     """
                                     ).click()
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                            """
                                                                                //span[@data-testid='clip']
                                                                                """)))
        except TimeoutException:
            delete_images()
            return False
        else:
            self.driver.find_element(By.XPATH,
                                     """
                                     //span[@data-testid='clip']
                                     """
                                     ).click()
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                """
                                                                                //input[@accept='image/*']
                                                                                """)))
        except TimeoutException:
            delete_images()
            return False
        else:
            self.driver.find_element(By.XPATH,
                                     """
                                     //input[@accept='image/*']
                                     """
                                     ).send_keys(glob.glob(f"{os.getcwd()}\\data\\downloads\\*.jpeg")[0])
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                            """
                                                                                //span[@data-testid='send']
                                                                                """)))
        except TimeoutException:
            delete_images()
            return False
        else:
            self.driver.find_element(By.XPATH,
                                     """
                                     //span[@data-testid='send']
                                     """
                                     ).click()
        sleep(1)
        delete_images()
        return True

    def archive(self, by: str = None) -> None:
        self.update()

        def __to_archive(chat: dict) -> None:
            rigth_click = chat['id']
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", rigth_click)
            actionChains = ActionChains(self.driver)
            actionChains.context_click(rigth_click).perform()
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH,
                        """
                        //div[@aria-label='Arquivar conversa']
                        """
                     )))
            except TimeoutException:
                return None
            else:
                self.driver.find_element(By.XPATH,
                                         """
                                         //div[@aria-label='Arquivar conversa']
                                         """
                                         ).click()
            self.remove(chat)
            return None

        def __archive_groups() -> None:
            for chat in self._chats:
                if chat['is_group']:
                    __to_archive(chat)
                    break
            else:
                return None
            return __archive_groups()

        def __archive_chats() -> None:
            for chat in self._chats:
                if not chat['is_group']:
                    __to_archive(chat)
                    break
            else:
                return None
            return __archive_chats()

        def __archive_all() -> None:
            for chat in self._chats:
                if chat:
                    __to_archive(chat)
                    break
            else:
                return None
            return __archive_all()
        if by == "groups":
            return __archive_groups()
        if by == "chats":
            return __archive_chats()
        if by is None:
            return __archive_all()
        return None


# %%
