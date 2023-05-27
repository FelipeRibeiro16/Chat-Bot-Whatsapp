# %%
from datetime import datetime, time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
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
    """WhatsApp bot class that initializes the bot and closes it

    Args:
        object (object): The object class

        Attributes:
            driver (webdriver): The webdriver
    """

    def __init__(self) -> None:
        return None

    def start(self) -> bool:
        """Starts the bot

        Returns:
            bool: True if the bot started successfully
        """
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('window-size=1920x2160')
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
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
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                                    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get("https://web.whatsapp.com/")

        return self.__autentication()

    def __autentication(self) -> bool:
        """Authenticates the bot

        Returns:
            bool: True if the bot authenticated successfully
        """
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
        """Closes the bot

        Returns:
            None
        """
        self.driver.close()


class Chat:
    """Chat class that contains the chats informations and methods to interact with them

    Args:
        object (object): The object class
        driver (webdriver): The webdriver

    Attributes:
        driver (webdriver): The webdriver
    """

    def __init__(self, driver: webdriver) -> None:
        self.driver: webdriver = driver
        self._chats: list = []
        self.main_chat: dict = None
        return None

    def is_main_chat(self, chat: dict) -> bool:
        """Checks if the chat is the main chat

        Args:
            chat (dict): The chat dictionary

        Returns:
            bool: True if the chat is the main chat, False otherwise
        """
        if chat['title'] == self.main_chat['title']:
            return True
        return False

    def __main_chat_is_set(self) -> bool:
        """Checks if the main chat is set

        Returns:
            bool: True if the main chat is set, False otherwise
        """
        if self.main_chat:
            return True
        return False

    def __if_muted(self, element: WebElement) -> bool:
        """Checks if the chat is muted
        Args:
            element (WebElement): The chat element
        Returns:
            bool: True if the chat is muted, False otherwise
        """
        if element.find_elements(By.XPATH, """
        *//span[@data-testid="muted"]
        """):
            return True
        return False

    def __is_group(self, text: list[str]) -> bool:
        """Checks if the chat is a group
        Args:
            text (list): The chat text
        Returns:
            bool: True if the chat is a group, False otherwise
        """
        if len(text) > 4:
            return True
        return False

    def __unread_messages(self, text: list[str]) -> int:
        """Gets the number of unread messages
        Args:
            text (list): The chat text
        Returns:
            int: The number of unread messages
        """
        try:
            return int(text[-1])
        except ValueError:
            return 0

    def __chat_last_message(self, text: list[str]) -> str:
        """Gets the last message
        Args:
            text (list): The chat text
        Returns:
            str: The last message
        """
        if self.__is_group(text):
            return text[4].lower()
        return text[2].lower()

    def __chat_last_message_time(self, text: str) -> datetime.time:
        """Gets the last message time
        Args:
            text (str): The chat message time text
        Returns:
            datetime.time: The last message time
        """
        seconds = datetime.now().time().second
        if self.verify_last_message(text):
            return time(int(text.split(":")[0]), int(
                text.split(":")[1]), seconds)
        return text

    def update(self) -> bool:
        """Updates the chat list

        Returns:
            bool: True if the chat list updated successfully, False otherwise
        """
        try:
            for chat in self._chats:
                raw_text = chat['id'].text
                chats_text = raw_text.split("\n")
                chat['raw_text'] = raw_text
                chat['silenced'] = self.__if_muted(chat['id'])
                chat['unread_messages'] = self.__unread_messages(chats_text)
                chat['last_message'] = self.__chat_last_message(chats_text)
                chat['date_last_message'] = self.__chat_last_message_time(
                    chats_text[1])
            return True
        except:
            if self.is_main_chat(chat):
                self.remove_chat(chat)
                self.main_chat_is_present()
            else:
                self.remove_chat(chat)
            return self.update()

    def new_chat(self, chat_title: str, main: bool = False) -> bool:
        """Creates a new chat

        Args:
            chat_title (str): The chat title

            main (bool, optional): If the chat is the main chat. Defaults to False

        Returns:
            bool: True if the chat was created successfully, False otherwise
        """
        chats_open = self.driver.find_elements(By.XPATH,
                                               """
                                                //div[@data-testid="cell-frame-container"]
                                                """)
        for chat_open in chats_open:
            chat_active_title = chat_open.find_element(By.XPATH,
                                                       f"""
                                                             .//div[@data-testid="cell-frame-title"]/span[1]
                                                             """).get_attribute("title")
            if chat_title in chat_active_title:
                break
        else:
            return False
        raw_text = chat_open.text
        chats_text = raw_text.split("\n")
        if not main:
            new = {
                'id': chat_open,
                'raw_text': raw_text,
                'title': chat_active_title,
                'is_group': self.__is_group(chats_text),
                'silenced': self.__if_muted(chat_open),
                'unread_messages': self.__unread_messages(chats_text),
                'last_message': self.__chat_last_message(chats_text),
                'date_last_message': self.__chat_last_message_time(chats_text[1]),
                'messages': []
            }
            if self.add(new):
                return True
        else:
            new = {
                'id': chat_open,
                'raw_text': raw_text,
                'title': chat_active_title,
                'is_group': self.__is_group(chats_text),
                'silenced': self.__if_muted(chat_open),
                'unread_messages': self.__unread_messages(chats_text),
                'last_message': self.__chat_last_message(chats_text),
                'date_last_message': self.__chat_last_message_time(chats_text[1]),
                'messages': []
            }
            self.main_chat = new
            return True
        return False

    def return_messages(self, id_chat: WebElement) -> list[str]:
        """Returns the messages of a chat

        Args:
            id_chat (WebElement): The chat element

        Returns:
            list: The messages of the chat
        """
        for chats in self._chats:
            if chats['id'] == id_chat:
                return chats['messages']
        return []

    def add(self, chat: dict) -> bool:
        """Adds a chat to the chat list

        Args:
            chat (dict): The chat to be added

        Returns:
            None
        """
        if not self.if_exists(chat['title']):
            self._chats.append(chat)
            return True
        return False

    def if_exists(self, chat_title: str) -> bool:
        """Checks if a chat exists in the chat list

        Args:
            chat_title (str): The chat title

        Returns:
            bool: True if the chat exists, False otherwise
        """
        for chat in self._chats:
            if chat['title'] == chat_title:
                return True
        return False

    def remove_chat(self, chat: dict) -> None:
        """Removes a chat from the chat list

        Args:
            chat (dict): The chat to be removed

        Returns:
            None
        """
        if self.if_exists(chat['title']):
            self._chats.remove(chat)
        return None

    def reset(self) -> None:
        """Resets the chat list

        Returns:
            None
        """
        self._chats = []
        return None

    def display(self, by: str = None) -> None:
        """Displays the chat list

        Args:
            by (str, optional): The way to display the chat list. Defaults to None.

        Returns:
            None
        """
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
        """Verifies if the last message is a time

        Args:
            last_message (str): The last message

        Returns:
            bool: True if the last message is a time, False otherwise
        """
        pattern = r"\d{2}:\d{2}"
        if re.fullmatch(pattern, last_message):
            return True
        return False

    def main_chat_is_present(self, warning: str = "Maintain the main chat unarchived") -> bool:
        """Checks if the main chat is present

        Args:
            warning (str): The warning message
        Returns:
            bool: True if the main chat is present, False otherwise
        """
        try:
            self.main_chat['id'].is_enabled()
            return True
        except:
            try:
                chat_search = self.driver.find_element(By.XPATH,
                                                       """
                                            //div[@data-testid="chat-list-search"]
                                            """)
                chat_search.click()
                chat_search.send_keys(self.main_chat['title'])
                chat_search.send_keys(Keys.ENTER)
                sleep(0.5)
                message_box = self.driver.find_element(By.XPATH,
                                                       """
                                         //div[@data-testid='conversation-compose-box-input']
                                         """
                                                       )
                message_box.send_keys(warning)
                message_box.send_keys(Keys.ENTER)
                sleep(1)
                self.new_chat(self.main_chat['title'], main=True)
                self.new_chat(self.main_chat['title'])
            except NoSuchElementException:
                return False

    def listen_chats(self, corresponded: str) -> dict:
        """Listens to specifics chats until a chat with the corresponded message appears

        Args:
            corresponded (str): The message to be listened
            Warning (str, optional): The warning message. Defaults to "Maintain the main chat unarchived".
            timeout (float, optional): The time between each listen. Defaults to 0.5.

            Returns:
                dict: The chat with the corresponded message
        """
        self.update()
        while True:
            try:
                for chats_listening in self._chats:
                    if corresponded in chats_listening['id'].text:
                        self.update()
                        return chats_listening
            except:
                self.update()

    def listen_set_main_chat(self, corresponded: str, timeout: int = 43200) -> bool:
        """Listens to all chats until a chat with the corresponded message appears and set it as the main chat

        Args:
            corresponded (str): The message to be listened
            timeout (int, optional): The time between each listen. Defaults to 12h.

        Returns:
            bool: True if the chat with the corresponded message appears, False otherwise
        """

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((By.XPATH,
                                                  """
                        //div[@data-testid="chat-list"]
                        """), corresponded))
        except TimeoutException:
            WhatsApp.close()
            return False
        else:
            chats_open = self.driver.find_elements(By.XPATH,
                                                   """
                                                //div[@data-testid="chat-list"]/div/div
                                                """)
            for chat_open in chats_open:
                if corresponded in chat_open.text:
                    chat_open_title = chat_open.find_element(By.XPATH,
                                                             f"""
                                                             .//div[@data-testid="cell-frame-title"]/span[1]
                                                             """).get_attribute("title")
                    break
            else:
                return self.listen_chats(corresponded, timeout)
            if self.new_chat(chat_open_title, main=True) and self.new_chat(chat_open_title):
                if self.__main_chat_is_set():
                    return True
            return False

    def last_message(self, chat: dict) -> dict:
        """Returns the last message of a chat

        Args:
            chat (dict): The chat to get the last message

        Returns:
            dict: The last message of the chat
        """
        self.update_messages(chat)
        while True:
            if chat['messages'] is None:
                return {}
            for message in chat['messages']:
                if not message['replied']:
                    return message
            else:
                return {}

    def reply_message(self, chat: dict, reply: str) -> bool:
        """Replies a message in a chat

        Args:
            chat (dict): The chat to reply the message
            reply (str): The message to be replied

        Returns:
            bool: True if the message was replied, False otherwise
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", chat['id'])
        actionChains = ActionChains(self.driver)
        chat['id'].click()
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                """
                                                                                //div[@data-testid='conversation-compose-box-input']
                                                                                """)))
        except TimeoutException:
            return False
        else:
            message_box = self.driver.find_element(By.XPATH,
                                                   """
                                     //div[@data-testid='conversation-compose-box-input']
                                     """
                                                   )
            message_box.send_keys(reply)
            message_box.send_keys(Keys.ENTER)
        return True

    def update_messages(self, chat: dict) -> bool:
        """Updates the messages of a chat

        Args:
            chat (dict): The chat to update the messages

        Returns:
            bool: True if the messages were updated, False otherwise
        """
        if chat is None:
            return False

        def is_audio(text: str) -> bool:
            pattern1 = r"\d{2}:\d{2}"
            pattern2 = r"\d{1}:\d{2}"
            if re.fullmatch(pattern1, text) or re.fullmatch(pattern2, text):
                return True
            return False

        def message_time(text: str) -> any:
            seconds = datetime.now().time().second
            return time(int(text.split(":")[0]), int(text.split(":")[1]), seconds)

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
            message_boxes = self.driver.find_elements(By.XPATH,
                                                      """
                                     //div[@data-testid='msg-container']
                                     """
                                                      )
            message_box = message_boxes[-1]
            messages = {}
            text = message_box.text.split("\n")
            messages['time'] = message_time(text[1])
            messages['id'] = message_box.text
            messages['message'] = 'audio' if is_audio(
                text[0]) else text[0].lower()
            messages['replied'] = False
            self.add_message(chat, messages)
            return True

    def mark_as_replied(self, chat: dict, message: dict) -> bool:
        """Marks a message as replied

        Args:
            chat (dict): The chat that have the message to be marked as replied
            message (dict): The message to be marked as replied
        Returns:
            bool: True if the message was marked as replied, False otherwise
        """
        if_exists = self.if_exists_message(chat, message['id'])
        if if_exists:
            chat['messages'][chat['messages'].index(
                message)]['replied'] = True
            return True
        return False

    def if_exists_message(self, chat: dict, message_id: WebElement) -> bool:
        """Verifies if a message exists in a chat

        Args:
            chat (dict): The chat to verify if the message exists
            message_id (WebElement): The message to be verified
        Returns:
            bool: True if the message exists, False otherwise
        """
        ids_chat = [elements['id'] for elements in chat['messages']]
        if message_id in ids_chat:
            return True
        return False

    def add_message(self, chat: dict, message: dict) -> None:
        """Adds a message in a chat

        Args:
            chat (dict): The chat to add the message
            message (dict): The message to be added

        Returns:
            None
        """
        if not self.if_exists_message(chat, message['id']):
            chat['messages'].append(message)
        return None

    def create_sticker(self) -> bool:
        """Creates a sticker from the last image in the chat

        Returns:
            bool: True if the sticker was created, False otherwise
        """
        def delete_images() -> None:
            """Deletes the images in the downloads folder

            Returns:
                None
            """
            images = glob.glob(f"{os.getcwd()}\\data\\downloads\\*.jpeg")
            for image in images:
                os.remove(image)
            return None
        elements = self.driver.find_elements(By.XPATH,
                                             """
                                                //div[@data-testid="media-url-provider"]
                                                """)
        try:
            element = elements[-1]
        except IndexError:
            return False
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", element)
        element.click()
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
        """Archives the chats

        Args:
            by (str, optional): The way to archive the chats. Defaults to None.

        Returns:
            None
        """
        def __to_archive(chat: dict) -> None:
            rigth_click = chat['id']
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", rigth_click)
            actionChains = ActionChains(self.driver)
            actionChains.context_click(rigth_click).perform()
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH,
                        """
                        //li[@data-testid='mi-archive']
                        """
                     )))
            except TimeoutException:
                return None
            else:
                self.driver.find_element(By.XPATH,
                                         """
                                         //li[@data-testid='mi-archive']
                                         """
                                         ).click()
            self.remove_chat(chat)
            return None

        def __archive_groups() -> None:
            """Archives the groups

            Returns:
                None
            """
            for chat in self._chats:
                if chat['is_group'] and not self.is_main_chat(chat):
                    __to_archive(chat)
                    sleep(1)
            return None

        def __archive_chats() -> None:
            """Archives the chats

            Returns:
                None
            """
            for chat in self._chats:
                if not chat['is_group'] and not self.is_main_chat(chat):
                    __to_archive(chat)
                    sleep(1)
            return None

        def __archive_all() -> None:
            """Archives all the chats

            Returns:
                None
            """
            for chat in self._chats:
                if chat:
                    __to_archive(chat)
                    sleep(1)
            return None
        if by == "groups":
            return __archive_groups()
        if by == "chats":
            return __archive_chats()
        if by is None:
            return __archive_all()
        return None
# %%
