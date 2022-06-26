import time

def login(browser, email, password):
    login_btn_nav = browser.find_element_by_xpath('//a[@href="#/login"]')
    login_btn_nav.click()

    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    login_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')

    email_input.send_keys(email)
    password_input.send_keys(password)
    login_btn.click()

    time.sleep(2)
#def new_article(browser, title, about, text, tag):
#     new_article_btn = browser.find_element_by_xpath('//a[@href="#/editor"]')
#     new_article_btn.click()
#
#     time.sleep(2)
#     title_input = browser.find_element_by_xpath('//*[@placeholder="Article Title"]')
#     about_input = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
#     text_input = browser.find_element_by_xpath('//*[@placeholder="Write your article (in markdown)"]')
#     tag_input = browser.find_element_by_xpath('//*[@placeholder="Enter tags"]')
#
#     title_input.send_keys(title)
#     about_input.send_keys(about)
#     text_input.send_keys(text)
#     tag_input.send_keys(tag)
#
#     publish_article_btn = browser.find_element_by_xpath('//button[@type="submit"]')
#     publish_article_btn.click()
#

# def commenting(browser, comment):
#     first_article = browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')[0]
#     assert first_article.is_visible
#     first_article.click()
