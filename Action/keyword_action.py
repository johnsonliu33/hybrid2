import time
from selenium import webdriver
from ProjVar.var import *
from Util.find import *
from Util.calendar import *
driver = ""
def open(browser):
    global driver
    try:
        if browser.find("ie")>=0:
            driver = webdriver.Ie()
        elif browser.find("chrome")>=0:
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
    except Exception as e:
        raise e

def visit(url):
    global driver
    driver.get(url)

def sleep(times):
    try:
        time.sleep(int(times))
    except Exception as e:
        raise e


def input(locator_method,locator_exp,content):
    global driver
    try:
        element =  getElement(driver,locator_method,locator_exp)
        element.send_keys(content)
    except Exception as e:
        raise  e

def click(locator_method,locator_exp):
    global driver
    try:
        element =  getElement(driver,locator_method,locator_exp)
        element.click()
    except Exception as e:
        raise  e

def assert_word(content):
    global driver
    try:
        assert content in driver.page_source
    except AssertionError as e:
        raise e

def quit():
    try:
        driver.quit()
    except Exception as e:
        raise e

def capture(file_path):
    try:
        driver.save_screenshot(file_path)
    except Exception as e:
        raise e

if __name__ == "__main__":
    open("chrome")
    visit("http://www.sogou.com")
    sleep(3)
    input("id","query","光荣之路自动化测试")
    click("id","stb")
    sleep(3)
    assert_word("安全测试")
    capture(ProjDirPath+"\\ScreenCapture\\"+get_current_time()+".png")
    quit()