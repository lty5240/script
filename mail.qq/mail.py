from selenium import webdriver
import sys
import argparse

try:
    parser = argparse.ArgumentParser(description='脚本手册')
    parser.add_argument("-S", "--session", help="session", required='true')
    parser.add_argument("-U", "--url", help="ip:port", required='true')

    parser.add_argument("-T", "--target", help="目标邮箱", required='true')
    parser.add_argument("--title", help="邮件主题", required='true')
    parser.add_argument("-C", "--content",  help="发送内容", required='true')

    args = parser.parse_args()
    session = args.session
    url = args.url
    target = args.target
    content = args.content
    title = args.title
except:
    print('args error')
    sys.exit()


def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
    RemoteWebDriver.execute = new_command_execute
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    new_driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities={}, options=options)
    new_driver.session_id = session_id
    RemoteWebDriver.execute = org_command_execute
    return new_driver


try:
    browser = create_driver_session(session, url)
    browser.switch_to.default_content()
    browser.find_element_by_xpath('//*[@id="composebtn"]').click()
    browser.switch_to.frame("mainFrame")
    browser.find_element_by_xpath(
        '//*[@id="toAreaCtrl"]/div[2]/input').send_keys(target)
    browser.find_element_by_xpath('//*[@id="subject"]').send_keys(title)
    # Body_frame=driver.find_element_by_xpath('//iframe[@scrolling="auto"]')
    Body_frame = browser.find_element_by_class_name("qmEditorIfrmEditArea")
    browser.switch_to.frame(Body_frame)
    # 添加正文
    browser.find_element_by_xpath('/html/body').send_keys(content)
    # 退回大Frame再点击发送
    browser.switch_to.parent_frame()
    browser.find_element_by_xpath('//*[@id="toolbar"]/div/a[1]').click()
    browser.switch_to.default_content()
    browser.switch_to.frame("mainFrame")
    res = browser.find_element_by_xpath('//*[@id="sendinfomsg"]').text
    if res == '您的邮件已发送':
        print('success')
    else:
        print('send  error')
except Exception as a:
    print('browser error')
