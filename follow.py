from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
driver.get("https://medium.com/m/signin?operation=login&redirect=https%3A%2F%2Fmedium.com%2F&source=upgrade_membership---landing_home_nav-----------------------landing_home_nav-")
sleep(1.5)


#Sets up program by signing into medium w password and email
def setup(driver):
    login_button = driver.find_element_by_xpath("//button[@data-action-value='login']")
    login_button.click()
    sleep(2)

    e_box = driver.find_element_by_xpath("//input[@type='email']")
    email = input("Email?")
    e_box.send_keys(email)
    nextButton = driver.find_element_by_xpath("//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc']")
    nextButton.click()
    sleep(2)

    driver.save_screenshot("input.png")

    p_box = driver.find_element_by_xpath("//input[@type='password']")
    password = input("Password?")
    p_box.send_keys(password)
    signInButton = driver.find_element_by_xpath("//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc']")
    signInButton.click()
    sleep(2)

    driver.get("https://medium.com/@21mvandervelden/followers")


#Recursive function - Scrolls down the follower/following pages clicks user profile if possible
def scroll(driver, count, tries):
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        sleep(0.5)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True
    try:
        sleep(1)
        driver.find_element_by_xpath(
            "//a[@data-action-source='user_profile---------%d-----------------------']" % count).click()
        driver.get(driver.current_url + "/followers")
    except:
        if tries == 20:
            return
        tries += 1
        scroll(driver, count, tries)


#Converts follower/following details into actual integers
def conversion(driver, f):
    for k in range(10):
        try:
            locator_str = "//a[@data-action-value='" + f + "']"
            num = driver.find_element_by_xpath(locator_str).text[:-10]
            if "K" in num:
                return int(float(num[:-1]) * 1000)
            else:
                return int(num)
        except:
            sleep(0.5)
            if k == 9:
                return 0


if __name__ == "__main__":
    setup(driver)
    my_follows = int(driver.find_element_by_xpath("//a[@data-action-value='followers']").text[:-10])
    my_following = int(driver.find_element_by_xpath("//a[@data-action-value='following']").text[:-10])
    print("I am followed by " + str(my_follows) + " and follow " + str(my_following) + " people.")

    for j in range(15, 225):
        print("\n")
        num_cases = 0
        x = 0
        follow_list = []

        scroll(driver, j, 0)

        base_name = driver.find_element_by_tag_name("h1").text
        base_url = driver.current_url
        base_following = conversion(driver, "followers")
        print("Beginning on " + base_name + "...")

        for i in range(1, min(base_following+1, 225)):
            scroll(driver, i, 0)
            x = i
            try:
                cycle_name = driver.find_element_by_tag_name("h1").text
                cycle_url = driver.current_url

                their_following = conversion(driver, "following")
                their_followers = conversion(driver, "followers")

                driver.save_screenshot("page.png")

                if their_following > their_followers:
                    try:
                        follow_button = driver.find_element_by_xpath(
                            "//button[@class='button button--primary u-noUserSelect button--withChrome u-accentColor--buttonNormal button--follow js-followButton']")
                        follow_button.click()
                        num_cases += 1
                        follow_list.append(cycle_url)
                        print(str(num_cases) + " - following " + cycle_name + " (" + str(their_following) + ", " + str(
                            their_followers) + "), case number " + str(i))
                        driver.save_screenshot("confirmation.png")
                    except:
                        pass
            except:
                pass
            driver.get(base_url)
            sleep(2)
        print(num_cases, x, round(float(num_cases)/x, 4))
        print("Follow list for " + base_name + ":")
        print(follow_list)
        driver.get("https://medium.com/@21mvandervelden/followers")
