import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.HomePage import HomePage
from pages.CareerPage import CareerPage
from pages.QAPage import QAPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    global driver
    if request.param == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif request.param == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    driver.maximize_window()
    yield driver
    driver.quit()


def test_insider_career_page(driver):
    print("🚀 Open Insider website")
    home_page = HomePage(driver)
    home_page.open()
    assert home_page.is_accessible(), "❌ Error, page not found"

    print("✅ Cookies accepted")
    home_page.accept_cookies()

    print("✅ Redirect to the Career page")
    home_page.navigate_to_careers()
    careers_page = CareerPage(driver)
    assert careers_page.is_accessible(), "❌ Error: Career page not found"

    print("✅ Sayfa bölümleri kontrol ediliyor.")
    assert careers_page.verify_sections(), "❌ Error: Careers section not correct!"

    print("✅ Redirecting to the QA Careers page.")
    careers_page.go_to_qa_careers()
    qa_careers_page = QAPage(driver)

    print("🔍 Checking for the QA Careers page.")
    assert qa_careers_page.is_accessible(), "❌ Error: QA Careers page not found!"

    print("✅ 'See all QA jobs' button checked and click.")
    qa_careers_page.click_see_all_qa_jobs()

    print("✅ The Department is expected to be 'Quality Assurance' and the location is being selected.")
    qa_careers_page.select_location_if_department_is_qa()
    qa_careers_page.wait_for_job_cards_to_be_replaced()

    qa_careers_page.wait_for_job_cards_to_load()
    print("✅ Job postings are being verified.")
    assert qa_careers_page.verify_job_listings(), "❌Error: Job postings do not meet the criteria!"

    print("✅ View Role butonu kontrol ediliyor...")
    assert qa_careers_page.verify_view_role_redirects(), "❌Error: View Role button does not redirect!"

    print("🎉 All tests completed successfully!")
    print("🌐 Last URL:", driver.current_url)
