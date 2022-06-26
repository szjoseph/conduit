from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from functions import login
from test_data import t_user, t_comment
import csv


class TestConduit(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        url = 'http://localhost:1667/'
        self.browser.get(url)
        self.browser.maximize_window()

    def teardown(self):
        self.browser.quit()

    # TC01 - Adatkezelési nyilatkozat használata - Sütik elfogadása
    def test_accept_cookies(self):
        cookie_accept_btn = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        cookie_accept_btn.click()
        time.sleep(2)
        cookie_panel = self.browser.find_elements_by_id('cookie-policy-panel')
        assert len(cookie_panel) == 0

    # TC02 - Regisztráció pozitív ágon, valid adatokkal.
    def test_registration(self):
        sign_up_btn = self.browser.find_element_by_xpath('//a[@href="#/register"]')
        sign_up_btn.click()
        user_name = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        email = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
        password = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
        sign_up_submit = self.browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')

        user_name.send_keys(t_user["username"])
        email.send_keys(t_user["email"])
        password.send_keys(t_user["pwd"])
        sign_up_submit.click()

        time.sleep(3)
        reg_msg = self.browser.find_element_by_xpath('//div[@class="swal-text"]')  # successful registration message
        assert reg_msg.text == "Your registration was successful!"

    # TC03 - Bejelentkezés
    def test_login(self):
        login(self.browser, t_user["email"], t_user["pwd"])
        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]
        assert user_profile.text == t_user["username"]

    # TC04 - Kijelentkezés
    def test_logout(self):
        login(self.browser, t_user["email"], t_user["pwd"])
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')
        logout_btn.click()
        assert self.browser.find_element_by_xpath('//a[@href="#/register"]').is_displayed()

    # TC05 - Adatok listázása - Lorem taggel rendelkező cikkek listázása
    def test_listing_data(self):
        login(self.browser, t_user["email"], t_user["pwd"])
        lorem_tag = self.browser.find_element_by_xpath('//a[@href="#/tag/lorem"]')
        lorem_tag.click()
        time.sleep(2)
        articles_found = len(self.browser.find_elements_by_xpath('//a[@class="preview-link"]/h1'))
        assert articles_found == 3

    # TC06 - Több oldalas lista bejárása - Navigálás a 2. oldalra
    def test_list_navigation(self):
        login(self.browser, t_user["email"], t_user["pwd"])
        page2_btn = self.browser.find_elements_by_xpath('//a[@class="page-link"]')[1]
        page2_btn.click()

        active_page = self.browser.find_element_by_xpath('//*[@class="page-item active"]')
        assert page2_btn.text == active_page.text

    # TC07 - Új adat bevitel - Kommentelés
    def test_add_comment(self):
        login(self.browser, t_user["email"], t_user["pwd"])
        first_article = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')[0]
        assert first_article.is_displayed()
        first_article.click()
        time.sleep(2)

        textarea = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
        post_comment_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
        textarea.send_keys(t_comment["comment"])
        post_comment_btn.click()
        time.sleep(2)
        latest_comment = self.browser.find_elements_by_xpath('//p[@class="card-text"]')[0]
        assert latest_comment.text == t_comment["comment"]

    # TC08 - Ismételt és sorozatos adatbevitel adatforrásból - Cikkek létrehozása
    def test_post_new_articles(self):
        login(self.browser, t_user["email"], t_user["pwd"])

        new_article_btn = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
        with open("test/article_data.csv", "r", encoding="UTF-8") as articles:
            a_table = csv.reader(articles, delimiter=";")
            for row in a_table:
                new_article_btn.click()
                time.sleep(2)
                title_input = self.browser.find_element_by_xpath('//*[@placeholder="Article Title"]')
                about_input = self.browser.find_element_by_xpath(
                    '//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
                text_input = self.browser.find_element_by_xpath('//*[@placeholder="Write your article (in markdown)"]')
                tag_input = self.browser.find_element_by_xpath('//*[@placeholder="Enter tags"]')
                publish_article_btn = self.browser.find_element_by_xpath('//button[@type="submit"]')

                title_input.clear()
                title_input.send_keys(row[0])
                about_input.clear()
                about_input.send_keys(row[1])
                text_input.clear()
                text_input.send_keys(row[2])
                tag_input.clear()
                tag_input.send_keys(row[3])
                time.sleep(1)
                publish_article_btn.click()
        profile_btn = self.browser.find_elements_by_xpath('//li/a[@class="nav-link"]')[2]
        profile_btn.click()
        time.sleep(2)
        self.browser.refresh()
        time.sleep(2)
        own_articles = self.browser.find_elements_by_xpath('//div[@class="article-preview"]')
        assert len(own_articles) == 5

    # TC09 - Meglévő adat módosítás - Felhasználónév megváltoztatása
    def test_change_data(self):
        login(self.browser, t_user["email"], t_user["pwd"])

        settings_btn = self.browser.find_element_by_xpath('//a[@href="#/settings"]')
        settings_btn.click()
        time.sleep(1)
        username_input = self.browser.find_element_by_xpath('//input[@placeholder="Your username"]')
        update_settings_btn = self.browser.find_element_by_xpath(
            '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
        username_input.clear()
        username_input.send_keys("NewUsername")
        update_settings_btn.click()
        time.sleep(2)
        update_successfull_msg = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        assert update_successfull_msg.text == "Update successful!"

    # TC10 - Adat vagy adatok törlése - Komment létrehozása, majd törlése
    def test_deleting_data(self):
        login(self.browser, t_user["email"], t_user["pwd"])

        first_article = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')[0]
        first_article.click()
        time.sleep(1)
        number_of_comments = len(self.browser.find_elements_by_xpath('//div[@class="card"]'))
        textarea = self.browser.find_element_by_xpath('//textarea[@placeholder="Write a comment..."]')
        post_comment_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-sm btn-primary"]')
        textarea.send_keys(t_comment["comment"])
        post_comment_btn.click()
        # time.sleep(1)  # nem működik nélküle
        delete_btn = WebDriverWait(self.browser, 5).until(ec.presence_of_element_located(
            (By.XPATH, '//i[@class="ion-trash-a"]')))
        delete_btn.click()
        time.sleep(1)
        number_of_comments2 = len(self.browser.find_elements_by_xpath('//div[@class="card"]'))
        assert number_of_comments == number_of_comments2

    # TC11 - Adatok lementése felületről - Saját cikkek címeinek lementése
    def test_saving_data(self):
        login(self.browser, t_user["email"], t_user["pwd"])
        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]
        user_profile.click()
        time.sleep(1)
        article_titles = self.browser.find_elements_by_xpath('//h1')
        with open('test/article_titles.txt', 'w', encoding='UTF-8') as collected_titles:
            for i in article_titles:
                collected_titles.write(i.text)
                collected_titles.write("\n")

        with open('test/article_titles.txt', 'r', encoding='UTF-8') as collected_titles2:
            saved_titles = collected_titles2.readlines()

        assert len(article_titles) == len(saved_titles)
