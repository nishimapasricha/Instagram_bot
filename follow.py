from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(8)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(10)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(300)
        #verification_elem = driver.find_element_by_xpath("//input[@name='verificationCode']")
        #verification_elem.clear()
        #verification_elem.send_keys("verification key")
        #verification_elem.send_keys(Keys.RETURN)
        #time.sleep(7)

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            #time.sleep(12)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(7, 15))
                name = driver.find_element_by_css_selector("body:nth-child(2) div._2dDPU.vCf6V:nth-child(18) div.zZYga > div.PdwC2._6oveC")
                print(name)
                follow_button = lambda: driver.find_element_by_xpath(
                    "//div[contains(@class,'bY2yH')]//button[contains(@type,'button')][contains(text(),'Follow')]").click()
                follow_button().click()

                print("div[contains(@class,'bY2yH')]//button[contains(@type,'button')][contains(text(),'Follow')]".value)
                time.sleep(10)

                for second in reversed(range(0, random.randint(2, 7))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(30)
            except Exception as e:
                time.sleep(12)
            unique_photos -= 1

if __name__ == "__main__":

    username = "yourusername"
    password = "yourpassword"

    ig = InstagramBot(username, password)
    ig.login()

    hashtags = ['Your Hashtags here' ]
    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
        except Exception:
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()
