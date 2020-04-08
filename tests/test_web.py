from pathlib import Path

import pytest

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys


SCRIPT_PATH = Path(__file__).resolve().parent
PROJECT_PATH = SCRIPT_PATH.parent
CHROMEDRIVER = PROJECT_PATH.joinpath('chromedriver')


@pytest.fixture
def browser():
    driver = Chrome(executable_path=CHROMEDRIVER)

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def test_duckduckgo_search(browser):
    URL = 'https://duckduckgo.com'
    PHRASE = 'panda'

    # Visit the search page
    browser.get(URL)

    # Search for the PHRASE
    search_input = browser.find_element_by_id('search_form_input_homepage')
    search_input.send_keys(PHRASE + Keys.RETURN)

    # Check if there are search results
    link_divs = browser.find_elements_by_css_selector('#links > div')
    assert len(link_divs) > 0, 'Search results not found!'

    # Check that at least 1 search result contains the PHRASE
    xpath = '//div[@id="links"]//*[contains(text(), "{}")]'.format(PHRASE)
    phrase_results = browser.find_elements_by_xpath(xpath)
    assert len(phrase_results) > 0, (
        'There are no results matching the search phrase'
    )

    # Verify that the search phrase is the same
    search_input = browser.find_element_by_id('search_form_input')
    assert search_input.get_attribute('value') == PHRASE, (
        'Search phrase does not match given PHRASE'
    )
