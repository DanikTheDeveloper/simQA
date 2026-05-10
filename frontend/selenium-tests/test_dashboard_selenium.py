import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()

    # Headless mode for CI/testing
    options.add_argument("--headless=new")

    # Required for many Linux/WSL environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Explicitly use installed Chromium browser
    options.binary_location = "/usr/bin/chromium-browser"

    # Explicitly use system chromedriver
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    yield driver

    driver.quit()


def test_dashboard_loads(driver):
    driver.get("http://localhost:5173")

    assert "Device ID" in driver.page_source


def test_device_table_or_empty_state_visible(driver):
    driver.get("http://localhost:5173")

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert (
        "Device ID" in page_text
        or "No devices available" in page_text
    )


def test_refresh_button_if_present(driver):
    driver.get("http://localhost:5173")

    buttons = driver.find_elements(By.TAG_NAME, "button")

    for button in buttons:
        if "refresh" in button.text.lower():
            button.click()
            break

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert (
        "Device" in page_text
        or "No devices available" in page_text
    )