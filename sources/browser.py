from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from typing import List, Tuple
import chromedriver_autoinstaller
import time
import os
import shutil
from bs4 import BeautifulSoup
import markdownify
import logging
import sys
import re
from urllib.parse import urlparse

from sources.utility import pretty_print

class Browser:
    def __init__(self, headless=False, anticaptcha_install=False):
        """Initialize the browser with optional headless mode."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
        self.js_scripts_folder = "./sources/web_scripts/" if not __name__ == "__main__" else "./web_scripts/"
        self.anticaptcha = "https://chrome.google.com/webstore/detail/nopecha-captcha-solver/dknlfmjaanfblgfdfebhijalfmhmjjjo/related"
        try:
            chrome_options = Options()
            chrome_path = self.get_chrome_path()
            
            if not chrome_path:
                raise FileNotFoundError("Google Chrome not found. Please install it.")
            chrome_options.binary_location = chrome_path
            
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--autoplay-policy=user-gesture-required")
            chrome_options.add_argument("--mute-audio")
            chrome_options.add_argument("--disable-webgl")
            chrome_options.add_argument("--disable-notifications")
            security_prefs = {
                "profile.default_content_setting_values.media_stream": 2,  # Block webcam/mic
                "profile.default_content_setting_values.notifications": 2,  # Block notifications
                "profile.default_content_setting_values.popups": 2,  # Block pop-ups
                "profile.default_content_setting_values.geolocation": 2,  # Block geolocation
                "safebrowsing.enabled": True,  # Enable safe browsing
            }
            chrome_options.add_experimental_option("prefs", security_prefs)
            
            chromedriver_path = shutil.which("chromedriver") # system installed driver.
            
            #If not found, try auto-installing the correct version
            if not chromedriver_path:
                chromedriver_path = chromedriver_autoinstaller.install()
          
            if not chromedriver_path:
                raise FileNotFoundError("ChromeDriver not found. Please install it or add it to your PATH.")
                
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger = logging.getLogger(__name__)
            self.logger.info("Browser initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize browser: {str(e)}")
        self.load_anticatpcha()
            
    @staticmethod
    def get_chrome_path() -> str:
        if sys.platform.startswith("win"):
            paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google\\Chrome\\Application\\chrome.exe")  # User install
            ]
        elif sys.platform.startswith("darwin"):  # macOS
            paths = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                     "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"]
        else:  # Linux
            paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"]

        for path in paths:
            if os.path.exists(path) and os.access(path, os.X_OK):  # Check if executable
                return path
        return None
    
    def load_anticatpcha(self):
        print("You might want to install the AntiCaptcha extension for captchas.")
        self.driver.get(self.anticaptcha)

    def go_to(self, url:str) -> bool:
        """Navigate to a specified URL."""
        try:
            initial_handles = self.driver.window_handles
            self.driver.get(url)
            time.sleep(1)
            self.apply_web_safety()
            self.logger.info(f"Navigated to: {url}")
            return True
        except WebDriverException as e:
            self.logger.error(f"Error navigating to {url}: {str(e)}")
            return False

    def is_sentence(self, text:str) -> bool:
        """Check if the text qualifies as a meaningful sentence or contains important error codes."""
        text = text.strip()

        error_codes = ["404", "403", "500", "502", "503"]
        if any(code in text for code in error_codes):
            return True
        words = re.findall(r'\w+', text, re.UNICODE)
        word_count = len(words)
        has_punctuation = any(text.endswith(p) for p in ['.', '，', ',', '!', '?', '。', '！', '？', '।', '۔'])
        is_long_enough = word_count > 5
        return (word_count >= 5 and (has_punctuation or is_long_enough))

    def get_text(self) -> str | None:
        """Get page text and convert it to README (Markdown) format."""
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            for element in soup(['script', 'style']):
                element.decompose()
            
            text = soup.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk and self.is_sentence(chunk))
            #markdown_text = markdownify.markdownify(text, heading_style="ATX")
            return "[Start of page]\n" + text + "\n[End of page]"
        except Exception as e:
            self.logger.error(f"Error getting text: {str(e)}")
            return None
    
    def clean_url(self, url:str) -> str:
        """Clean URL to keep only the part needed for navigation to the page"""
        clean = url.split('#')[0]
        parts = clean.split('?', 1)
        base_url = parts[0]
        if len(parts) > 1:
            query = parts[1]
            essential_params = []
            for param in query.split('&'):
                if param.startswith('_skw=') or param.startswith('q=') or param.startswith('s='):
                    essential_params.append(param)
                elif param.startswith('_') or param.startswith('hash=') or param.startswith('itmmeta='):
                    break
            if essential_params:
                return f"{base_url}?{'&'.join(essential_params)}"
        return base_url
    
    def is_link_valid(self, url:str) -> bool:
        """Check if a URL is a valid link (page, not related to icon or metadata)."""
        if len(url) > 64:
            return False
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return False
        if re.search(r'/\d+$', parsed_url.path):
            return False
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        metadata_extensions = ['.ico', '.xml', '.json', '.rss', '.atom']
        for ext in image_extensions + metadata_extensions:
            if url.lower().endswith(ext):
                return False
        return True

    def get_navigable(self) -> [str]:
        """Get all navigable links on the current page."""
        try:
            links = []
            elements = self.driver.find_elements(By.TAG_NAME, "a")
            
            for element in elements:
                href = element.get_attribute("href")
                if href and href.startswith(("http", "https")):
                    links.append({
                        "url": href,
                        "text": element.text.strip(),
                        "is_displayed": element.is_displayed()
                    })
            
            self.logger.info(f"Found {len(links)} navigable links")
            return [self.clean_url(link['url']) for link in links if (link['is_displayed'] == True and self.is_link_valid(link['url']))]
        except Exception as e:
            self.logger.error(f"Error getting navigable links: {str(e)}")
            return []

    def click_element(self, xpath: str) -> bool:
        """Click an element specified by XPath."""
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            if not element.is_displayed():
                return False
            if not element.is_enabled():
                return False
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
                time.sleep(0.1)
                element.click()
                return True
            except ElementClickInterceptedException as e:
                return False
        except TimeoutException:
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error clicking element at {xpath}: {str(e)}")
            return False
        
    def load_js(self, file_name: str) -> str:
        path = os.path.join(self.js_scripts_folder, file_name)
        try:
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            raise Exception(f"Could not find: {path}") from e
        except Exception as e:
            raise e

    def find_all_inputs(self, timeout=4):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(0.5)
        script = self.load_js("find_inputs.js")
        input_elements = self.driver.execute_script(script)
        return input_elements

    def get_form_inputs(self) -> List[str]:
        """Extract all input from the page and return them."""
        try:
            #input_elements = self.driver.find_elements(By.TAG_NAME, "input")
            input_elements = self.find_all_inputs()
            if not input_elements:
                return ["No input forms found on the page."]

            form_strings = []
            for element in input_elements:
                input_type = element["type"] or "text"
                if input_type in ["hidden", "submit", "button", "image"] or not element["displayed"]:
                    continue
                input_name = element["text"] or element["id"] or input_type
                if input_type == "checkbox" or input_type == "radio":
                    checked_status = "checked" if element.is_selected() else "unchecked"
                    form_strings.append(f"[{input_name}]({checked_status})")
                else:
                    form_strings.append(f"[{input_name}]("")")
            return form_strings

        except Exception as e:
            self.logger.error(f"Error extracting form inputs: {str(e)}")
            return [f"Error extracting form inputs."]

    def get_buttons_xpath(self) -> List[str]:
        """
        Find buttons and return their type and xpath.
        """
        buttons = self.driver.find_elements(By.TAG_NAME, "button") + \
                  self.driver.find_elements(By.XPATH, "//input[@type='submit']")
        result = []
        for i, button in enumerate(buttons):
            if not button.is_displayed() or not button.is_enabled():
                continue
            text = (button.text or button.get_attribute("value") or "").lower().replace(' ', '')
            xpath = f"(//button | //input[@type='submit'])[{i + 1}]"
            if "login" in text or "sign" in text or "register":
                result.append((text, xpath))
        result.sort(key=lambda x: len(x[0]))
        return result

    def find_and_click_submit(self, btn_type:str = 'login') -> None:
        buttons = self.get_buttons_xpath()
        if len(buttons) == 0:
            self.logger.warning(f"No visible buttons found")
        for button in buttons:
            if button[0] == btn_type:
                self.click_element(button[1])
    
    def find_input_xpath_by_name(self, inputs, name: str) -> str | None:
        for field in inputs:
            if name in field["text"]:
                return field["xpath"]
        return None

    def fill_form_inputs(self, input_list:[str]) -> bool:
        """Fill form inputs based on a list of [name](value) strings."""
        inputs = self.find_all_inputs()
        try:
            for input_str in input_list:
                match = re.match(r'\[(.*?)\]\((.*?)\)', input_str)
                if not match:
                    self.logger.warning(f"Invalid format for input: {input_str}")
                    continue

                name, value = match.groups()
                name = name.strip()
                value = value.strip()
                xpath = self.find_input_xpath_by_name(inputs, name)
                if not xpath:
                    continue
                element = self.driver.find_element(By.XPATH, xpath)
                input_type = (element.get_attribute("type") or "text").lower()
                if input_type in ["checkbox", "radio"]:
                    is_checked = element.is_selected()
                    should_be_checked = value.lower() == "checked"

                    if is_checked != should_be_checked:
                        element.click()
                        self.logger.info(f"Set {name} to {value}")
                else:
                    element.send_keys(value)
                    self.logger.info(f"Filled {name} with {value}")
            return True
        except Exception as e:
            self.logger.error(f"Error filling form inputs: {str(e)}")
            return False

    def get_current_url(self) -> str:
        """Get the current URL of the page."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get the title of the current page."""
        return self.driver.title

    def scroll_bottom(self) -> bool:
        """Scroll to the bottom of the page."""
        try:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(1)  # Wait for scroll to complete
            return True
        except Exception as e:
            self.logger.error(f"Error scrolling: {str(e)}")
            return False

    def screenshot(self, filename:str) -> bool:
        """Take a screenshot of the current page."""
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved as {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return False

    def apply_web_safety(self):
        """
        Apply security measures to block any website malicious/annoying execution, privacy violation etc..
        """
        script = self.load_js("inject_safety_script.js")
        input_elements = self.driver.execute_script(script)

    def close(self):
        """Close the browser."""
        try:
            self.driver.quit()
            self.logger.info("Browser closed")
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")

    def __del__(self):
        """Destructor to ensure browser is closed."""
        self.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    browser = Browser(headless=False)
    time.sleep(8)
    
    try:
        print("AntiCaptcha Test")
        browser.go_to("https://www.google.com/recaptcha/api2/demo")
        time.sleep(5)
        print("Form Test:")
        browser.go_to("https://practicetestautomation.com/practice-test-login/")
        inputs = browser.get_form_inputs()
        inputs = ['[username](student)', f'[password](Password123)', '[appOtp]()', '[backupOtp]()']
        browser.fill_form_inputs(inputs)
        browser.find_and_click_submit()
        print("Stress test")
        browser.go_to("https://theannoyingsite.com/")
    finally:
        browser.close()
