from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


class Utils:
    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    def wait_and_find(self, by: str, value) -> WebElement:
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def get_inner_text(self, by: str, value) -> str | None:
        try:
            return self.driver.find_element(by, value).text.strip()
        except:
            return None
