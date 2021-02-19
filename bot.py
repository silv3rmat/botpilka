import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from time import sleep, time

options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

LOGIN = ''
PASSWORD = ''
GROUP_ID = '1077873292657481'
WANTED_OWNER = ""
WANTED_TITLE = "Zapisy"
MESSAGE = "Gram, pizdeczki\n"

time_start = time()
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
driver.get('https://facebook.com')

login_locator = (By.ID, 'email')
password_locator = (By.ID, 'pass')
login_button_locator = (By.CSS_SELECTOR, 'button[name="login"]')

wait = WebDriverWait(driver, 20)

accept_cookies_locator = (By.CSS_SELECTOR, 'button[title="Accept All"]')

wait.until(EC.element_to_be_clickable(accept_cookies_locator))
driver.find_element(*accept_cookies_locator).click()

wait.until(EC.element_to_be_clickable(login_button_locator))
driver.find_element(*login_locator).send_keys(LOGIN)
driver.find_element(*password_locator).send_keys(PASSWORD)
driver.find_element(*login_button_locator).click()

sleep(10)

while True:
    driver.get(f'https://facebook.com/groups/{GROUP_ID}')

    group_feed_locator = (By.CSS_SELECTOR, 'div[role="feed"]')
    post_locator = (By.XPATH, '*')
    sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    sleep(5)
    wait.until(EC.presence_of_element_located(group_feed_locator))

    feed = driver.find_element(*group_feed_locator)

    last_post = feed.find_elements(*post_locator)[1]

    post_text_locator = (By.CSS_SELECTOR, 'div[dir="auto"]')
    post_owner_locator = (By.CSS_SELECTOR, 'a[aria-label]')
    comment_locator = (By.CSS_SELECTOR, 'div[aria-label="Napisz komentarz"]')
    # time_locator = (By.XPATH, './/a/span[contains(text()," min")|contains(text()," godz.")|contains(text(),"Przed chwilą")]')
    title = last_post.find_element(*post_text_locator)
    author = last_post.find_element(*post_owner_locator)
    # try:
    #     post_time = post.find_element(*time_locator).get_attribute('innerHTML')
    # except NoSuchElementException:
    #     continue
    # minutes, dimension = post_time.split(' ')
    # if dimension =='min':
    #     post_time = time() - (int(minutes)-1) *60
    # elif dimension =='godz.':
    #     post_time = time() - int(minutes) *3600
    # elif dimension=='chwilą':
    #     post_time = time()
    if WANTED_TITLE in title.get_attribute('innerHTML') and WANTED_OWNER == author.get_attribute('aria-label'):
        comment = last_post.find_element(*comment_locator)
        comment.click()
        comment.send_keys(MESSAGE)
        sys.exit()
    sleep(60)
