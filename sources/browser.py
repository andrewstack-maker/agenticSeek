from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from bs4 import BeautifulSoup
import markdownify
import logging
import sys

class Browser:
    def __init__(self, headless=False, anticaptcha_install=False):
        """Initialize the browser with optional headless mode."""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
        self.anticaptcha = "https://chrome.google.com/webstore/detail/nopecha-captcha-solver/dknlfmjaanfblgfdfebhijalfmhmjjjo/related"
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            self.logger = logging.getLogger(__name__)
            self.logger.info("Browser initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize browser: {str(e)}")

    def goTo(self, url):
        """Navigate to a specified URL."""
        try:
            self.driver.get(url)
            time.sleep(2)  # Wait for page to load
            self.logger.info(f"Navigated to: {url}")
            return True
        except WebDriverException as e:
            self.logger.error(f"Error navigating to {url}: {str(e)}")
            return False
    
    def is_sentence(self, text):
        """Check if the text is a sentence."""
        if "404" in text:
            return True # we want the ai to see the error
        return len(text.split(" ")) > 5 and '.' in text

    def getText(self):
        """Get page text and convert it to README (Markdown) format."""
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            for element in soup(['script', 'style']):
                element.decompose()
            
            text = soup.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk and self.is_sentence(chunk))
            
            markdown_text = markdownify.markdownify(text, heading_style="ATX")
            
            return markdown_text
        except Exception as e:
            self.logger.error(f"Error getting text: {str(e)}")
            return None

    def getNavigable(self):
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
            return links
        except Exception as e:
            self.logger.error(f"Error getting navigable links: {str(e)}")
            return []

    def clickElement(self, xpath):
        """Click an element specified by xpath."""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            element.click()
            time.sleep(2)  # Wait for action to complete
            return True
        except TimeoutException:
            self.logger.error(f"Element not found or not clickable: {xpath}")
            return False

    def getCurrentUrl(self):
        """Get the current URL of the page."""
        return self.driver.current_url

    def getPageTitle(self):
        """Get the title of the current page."""
        return self.driver.title

    def scrollToBottom(self):
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

    def takeScreenshot(self, filename):
        """Take a screenshot of the current page."""
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved as {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return False

    def close(self):
        """Close the browser."""
        try:
            self.driver.quit()
            self.logger.info("Browser closed")
        except Exception as e:
            raise e

    def __del__(self):
        """Destructor to ensure browser is closed."""
        self.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    browser = Browser(headless=False)
    
    try:
        browser.goTo("https://karpathy.github.io/")
        text = browser.getText()
        print("Page Text in Markdown:")
        print(text)
        links = browser.getNavigable()
        print("\nNavigable Links:")
        for link in links[:50]:
            print(f"Text: {link['text']}, URL: {link['url']}")
        
        browser.takeScreenshot("example.png")
        
    finally:
        browser.close()