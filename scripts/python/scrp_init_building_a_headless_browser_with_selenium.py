# install selenium if not already installed
# pip install selenium

# start the webdriver
from selenium import webdriver

path_to_chromedriver = '/Users/Ashoo/Miniconda3/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# Now, lets open the page we want
url = 'https://www.lexisnexis.com/hottopics/lnacademic/?verb=sf&amp;sfi=AC00NBGenSrch'
browser.get(url)

# switch frame
browser.switch_to_frame('mainFrame')

browser.find_element_by_id('terms')
browser.find_element_by_id('terms').clear()

browser.find_element_by_id('terms').send_keys('balloon')

browser.find_element_by_xpath('//*[@id="txtFrmDate"]')

browser.find_element_by_xpath('//*[@id="txtFrmDate"]"]/option[contains(text(), "Today")]').click()
