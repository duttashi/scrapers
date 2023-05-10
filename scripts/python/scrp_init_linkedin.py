from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
# create object for chrome options
chrome_options = Options()
# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
chrome_options.add_argument('user-data-dir=C:\\Users\\Ashoo\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})
# invoke the webdriver
# filePath = r'C:\\Users\\Ashoo\\Documents\\playground_python\\chromedriver.exe'
# driver = webdriver.Chrome(filePath, options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install())
email = "sandyagostino@yahoo.com.ar"
password = "papa#456"
actions.login(driver, email, password)  # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/duttashish/", driver=driver)
