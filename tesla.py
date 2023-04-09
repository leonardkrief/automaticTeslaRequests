from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re

# Replace these with your own information
first_name = "Elon"
last_name = "MUSK"
email = "mistermusk@tesla.com"
phone = "123456789" #if your phone number is 06 12 34 56 78, type "612345678"
linkedin_url = "linkedin_profile_url"
resume_file_path = "/file/to/resume/resume.pdf"
#WARNING: YOU HAVE TO PROVIDE COHERENT PHONE NUMBER + EXISTING FILE FOR RESUME
#         OR THE DRIVER WON'T BE ABLE TO PROCESS, RESULTING IN FRUSTRATING QUITTING

#List of the urls of the internships you want to apply to
internships_urls=[
    "https://www.tesla.com/careers/search/job/apply/xxxxxx",
    "https://www.tesla.com/careers/search/job/apply/xxxxxx"]

firstConnection = True
headless = True

def init_driver():
    options = Options()
    if (headless):
        options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--start-maximized')
    options.add_argument("--incognito")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    chromedriver_path = 'chromedriver' # Replace with the path to your Chromedriver executable
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def quit_driver(driver):
    driver.close()
    driver.quit()
    print("driver exited gracefully")

def select_option(driver, element_XPATH, option_VALUE):
    element = driver.find_element(By.XPATH, element_XPATH)
    all_options = element.find_elements(By.TAG_NAME, "option")
    for option in all_options:
        if (option.get_attribute("value") == option_VALUE):
            option.click()
            print("    clicked on " + option_VALUE + " button")
            break

def clickNext(driver, element_XPATH):
    driver.execute_script("window.scrollBy(0, 500)")
    time.sleep(1)
    driver.find_element(By.XPATH, element_XPATH).click()
    print("    Next button got clicked")

def fill_date(driver, month_year, day, select_date_XPATH, select_month_XPATH):
    select_month_element = driver.find_element(By.XPATH, select_month_XPATH)
    driver.find_element(By.XPATH, select_date_XPATH).click()
    while (select_month_element.get_attribute("aria-label") != month_year):
        select_month_element.click()
    print("      selected " + month_year)

    pattern = r'div\[(\d+)\]\/button\[(\d+)\]'
    match = re.search(pattern, select_month_XPATH)
    div_index, button_index = match.groups()
    new_div_index = int(div_index) + 2
    new_button_index = int(button_index) + day
    select_day_XPATH = re.sub(pattern, f'div[{new_div_index}]/button[{new_button_index}]', select_month_XPATH)
    driver.find_element(By.XPATH, select_day_XPATH).click()
    print("    selected day " + str(day))

def fill_form_1(driver, url):
    driver.get(url)
    # Wait for the page to load
    time.sleep(3)

    #Quit the popup if first time
    global firstConnection
    global headless
    if (firstConnection and not(headless)):
        driver.find_element(By.XPATH, '//*[@id="tds-global-menu"]/dialog/div/button').click()
        firstConnection = False

    print("Auto-filling " + driver.find_element(By.XPATH, '//*[@id="app"]/div/div/span').text + " form... (n°" + url[47:] + ")")
    print("  Filling page 1/4...")

    driver.find_element(By.NAME, "personal.firstName").send_keys(first_name)
    print("    filled first name")
    driver.find_element(By.NAME, "personal.lastName").send_keys(last_name)
    print("    filled last name")
    driver.find_element(By.NAME, "personal.email").send_keys(email)
    print("    filled email")
    driver.find_element(By.XPATH, '//*[@id="country"]/button').click()
    driver.find_element(By.XPATH, '//*[@id="country-listbox-FR"]').click()
    print("    selected phone country id")
    select_option(driver, '//*[@name="personal.phoneType"]', "mobile")
    driver.find_element(By.NAME, "personal.phone").send_keys(phone)
    print("    selected phone type + added phone number")
    select_option(driver, '//*[@name="personal.country"]', "FR")
    print("    selected country")
    driver.find_element(By.XPATH, '//*[@accept=".pdf,.doc,.docx,.txt"]').send_keys(resume_file_path)
    print("    sent resume")
    driver.execute_script("window.scrollBy(0, 500)")
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[@class="tds-icon-trigger tds-icon-trigger--small style_Add__Kl8Wg"]').click()
    driver.find_element(By.NAME, "personal.profileLinks[0].link").send_keys(linkedin_url)
    select_option(driver, '//*[@name="personal.profileLinks[0].type"]', "linkedin")
    print("    Added LinkedIn profile")

    clickNext(driver, '//*[@id="app"]/div/div/form/div/div[2]/button')

def fill_form_2(driver):
    print("  Filling page 2/4...")
    driver.execute_script("window.scrollBy(0, 500)")
    fill_date(driver, "September 2023", 1, '//*[@id="step--job"]/fieldset/div[1]/div/div[1]/div[1]/button', '//*[@id="step--job"]/fieldset/div[1]/div/div[1]/div[2]/div/div[1]/button[2]')
    print("    Added internship start date")
    select_option(driver, '//*[@name="job.jobInternshipDuration"]', "6_months")
    print("    Added internship duration")
    select_option(driver, '//*[@name="job.jobInternshipType"]', "full_time")
    print("    Added full time internship")
    driver.find_element(By.XPATH, '//*[@name="job.jobInternshipThesis" and @value="yes"]').click()
    print("    Clicked yes for thesis")

    clickNext(driver, '//button[@name="next"]')

def fill_form_3(driver):
    print("  Filling page 3/4...")

    select_option(driver, '//*[@name="legal.legalNoticePeriod"]', "immediately")
    print("    Added legal notice period")
    driver.find_element(By.XPATH, '//*[@name="legal.legalConsiderOtherPositions" and @value="yes"]').click()
    print("    Clicked yes for consider other positions")
    driver.find_element(By.XPATH, '//*[@name="legal.legalImmigrationSponsorship" and @value="yes"]').click()
    print("    Clicked yes for legel immigration support from Tesla")
    driver.find_element(By.XPATH, '//*[@name="legal.legalFormerTeslaEmployee" and @value="no"]').click()
    print("    Clicked no for former Tesla employee")

    #First scroll
    driver.execute_script("window.scrollBy(0, 400)")
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@name="legal.legalFormerTeslaInternOrContractor" and @value="no"]').click()
    print("    Clicked no for already Tesla intern")
    driver.find_element(By.XPATH, '//*[@name="legal.legalUniversityStudent" and @value="yes"]').click()
    print("    Clicked yes for university student")
    driver.find_element(By.XPATH, '//*[@name="legal.legalReceiveNotifications" and @value="yes"]').click()
    print("    Clicked yes for receiving text messages notifications")
    fill_date(driver, "February 2024", 0, '//*[@id="step--legal"]/fieldset[1]/div[7]/div/div/div[1]/button', '//*[@id="step--legal"]/fieldset[1]/div[7]/div/div/div[2]/div/div[1]/button[2]')

    #Second scroll
    driver.execute_script("window.scrollBy(0, 2000)")
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@name="legal.legalAcknowledgment"]').click()
    print("    clicked OK on legal acknowledgement")
    driver.find_element(By.XPATH, '//*[@name="legal.legalAcknowledgmentName"]').send_keys(last_name + " " + first_name)
    print("    signed with first + last names")

    clickNext(driver, '//button[@name="next"]')

def fill_form_4(driver):
    print("  Filling page 4/4...")

    #Scroll everything to the bottom
    driver.execute_script("window.scrollBy(0, 1000)")
    element = driver.find_element(By.XPATH, '//div[@class="style_Disclaimer__toBo-"]')
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", element)
    time.sleep(1)

    select_option(driver, '//*[@name="eeo.eeoGender"]', "male")
    select_option(driver, '//*[@name="eeo.eeoVeteranStatus"]', "no")
    select_option(driver, '//*[@name="eeo.eeoRaceEthnicity"]', "2_races_or_more")
    select_option(driver, '//*[@name="eeo.eeoDisabilityStatus"]', "no")
    driver.find_element(By.XPATH, '//*[@name="eeo.eeoDisabilityStatusName"]').send_keys(last_name + " " + first_name)
    print("    signed with first + last names")
    driver.find_element(By.XPATH, '//*[@name="eeo.eeoAcknowledgment"]').click()
    print("    clicked on eeo acknowledgement")

    clickNext(driver, '//button[@type="submit"]')
    print("Form submitted")
    time.sleep(4)

def fill_form(driver, url):
    fill_form_1(driver, url)
    fill_form_2(driver)
    fill_form_3(driver)
    fill_form_4(driver)

def main():
    driver = init_driver()
    for url in internships_urls:
        fill_form(driver, url)
    quit_driver(driver)

if __name__ == '__main__':
    main()
