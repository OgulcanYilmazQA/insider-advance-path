import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class CareerPage(BasePage):
    # Locator definitions
    COOKIE_ACCEPT = "//*[@id='wt-cli-accept-all-btn']"
    LOCATIONS_XPATH = "//*[@id='career-our-location']/div/div/div/div[1]"
    TEAMS_PATH = "//*[@id='career-find-our-calling']/div/div/a"
    LIFE_AT_INSIDER = "//h2[contains(text(), 'Life at Insider')]"
    SEE_ALL_TEAMS = "//a[contains(text(), 'See all teams')]"
    QA_CAREER = "//h3[contains(text(), 'Quality Assurance')]"
    QA_OPEN_POSITIONS = "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(text(), 'Open Positions')]"

    def __init__(self, driver):
        """
        CareersPage constructor.

        :param driver: Selenium WebDriver instance
        """
        super().__init__(driver)
        self.check()

    def check(self):
        """
        Checks visibility of critical locators to confirm page integrity.

        :raises Exception: If any critical element is not visible
        """
        try:
            print("✅ Running initial checks for critical elements...")
            self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
            self.wait_for_element(By.XPATH, self.TEAMS_PATH)
            self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER)
            print("✅ All critical elements are visible.")
        except Exception as e:
            print(f"❌ Critical element not found during check: {e}")
            raise

    def is_accessible(self):
        """
        Verifies if the Careers page is accessible.

        :return: True if title or URL contains career-related keywords, else False
        """
        try:
            print("🔍 QA page title check")
            self.wait_for_page_to_load()
            title = self.driver.title.lower()
            url = self.driver.current_url.lower()
            print(f"📄 QA Page Title: {title}")
            print(f"🌐 QA Page URL: {url}")
            return "careers" in title or "quality assurance" in title or "/careers" in url
        except Exception as e:
            print(f"❌ QA page error: {e}")
            return False

    def verify_sections(self):
        """
        Verifies the presence of key sections: Locations, Teams, and Life at Insider.

        :return: True if all sections are found, else False
        """
        try:
            print("🔄 Waiting for Location part..")
            self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
            print("✅ Locations part found!")

            print("🔄 Waiting for Teams part..")
            self.wait_for_element(By.XPATH, self.TEAMS_PATH)
            print("✅ Teams part found!")

            self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER)
            print("✅ Life at Insider part found!")

            return True
        except Exception as e:
            print(f"❌ Error: Element could not be found: {e}")
            return False

    def go_to_qa_careers(self):
        """
        Navigates to the QA Careers page, using fallback methods if necessary.

        :raises Exception: If navigation fails
        """
        try:
            print("🔄 Waiting for 'See All Teams' button...")
            see_all_teams_button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_TEAMS)

            self.scroll_to_element(By.XPATH, self.SEE_ALL_TEAMS)
            time.sleep(1)
            self.scroll_to_element(By.XPATH, self.SEE_ALL_TEAMS)
            time.sleep(1)

            see_all_teams_button.click()
            print("✅ 'See All Teams' button clicked.")

            print("🔄 Waiting for page load...")
            self.wait_for_page_to_load()
            time.sleep(2)

            print("🔄 'QA Careers' button checked...")
            self.scroll_to_element(By.XPATH, self.QA_CAREER)
            time.sleep(1)

            qa_careers_section = self.wait_for_element(By.XPATH, self.QA_CAREER)

            qa_open_link = self.wait_for_element_to_be_clickable(By.XPATH, self.QA_OPEN_POSITIONS)

            if qa_open_link:
                print("🖱 Clicking on the 'Open Positions' button ")
                self.scroll_to_element(By.XPATH, self.QA_OPEN_POSITIONS)
                time.sleep(1)
                qa_open_link.click()
                print("✅ Changed to the 'QA Careers' page.")
            else:
                print("⚠️ Link not found, clicking with JavaScript")
                self.driver.execute_script("arguments[0].click();", qa_careers_section)
                print("✅ 'QA Careers' button clicked.")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
            )
        except Exception as e:
            print(f"❌ Error: 'QA Careers' page could not be found: {e}")
