from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from time import sleep, time, asctime, localtime
from json import loads, dumps
from tqdm import tqdm
import os, sys
import smtplib
import email
import email.encoders 
import email.mime.text 
import email.mime.base
from email.mime.multipart import MIMEMultipart
from getpass import getpass

EMAIL_ID = ''
PASSWORD = ''

SENDER_EMAIL = '' 
SENDER_PASSWORD = ''


SLEEP_TIME = 600

driver = ''
notify = ''
server = ''

def sleep_bar(sleep_time):
    for _ in tqdm(range(sleep_time), desc='Sleeping', ncols= 75, mininterval=1, maxinterval=1, leave = False):
        sleep(1)

def write_file(grades):
    with open(EMAIL_ID + '.json', 'w') as f:
        f.write(dumps(grades, indent=4))
    print('Data Written To File')

def sleeping():
    print()
    print(asctime(localtime(time())))
    print_line()
    sleep_bar(SLEEP_TIME)
    print(asctime(localtime(time())))
    print()

def grade_count(grades):
    total_grades = len(grades)
    received_grades = 0
    for course in grades:
        if gardes[course]["grade"]!='':
            received_grades+=1
    return total_grades==received_grades

def send_email(course, message):
    global server
    html = "<p> " + message.replace('\n','<br>') + " <br> <br>Regards,<br><b>QuadCore Systems</b><br>[A YVJ Initiative]</p>"
    emailMsg = email.mime.multipart.MIMEMultipart('mixed')
    emailMsg['Subject'] = course['name'][:course['name'].find('-')].strip() +' Grade'
    emailMsg['From'] = 'QuadCore Systems'
    emailMsg['To'] = EMAIL_ID
    emailMsg.attach(email.mime.text.MIMEText(html,'html'))
    try:
        server.sendmail(SENDER_EMAIL, EMAIL_ID, emailMsg.as_string())
    except:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, EMAIL_ID, emailMsg.as_string())

def format_message(course):
    message = f'Course: {course["name"]}\nCredits: {course["credit"]}\nGrade: {course["grade"]}\nGrade Points: {course["points"]}'
    return message

def send_grade(course):
    try:
        message = format_message(course)
        send_email(course, message)
        sleep(5)
        print(f'New Grade For {course["name"]}')
        print(message)
        print('Message Sent')
    except Exception as e:
            print('Message Send Error')
            print('Error:', str(e))

def match_grade(grades):
    new_grade = False
    with open(EMAIL_ID + '.json', 'r') as f:
        data = loads(f.read())
    for course in grades:
        try:
            if grades[course]["grade"]!='' and grades[course]["grade"]!=data[course]["grade"]:
                send_grade(grades[course])
                new_grade = True
            else:
                print(f'No New Grade For {course}')
        except Exception as e:
            print('Grade Check Error')
            print('Error:', str(e))
    return new_grade

def check_grade():
    driver.get('https://lms.ashoka.edu.in/Contents/Grades/ViewGrades.aspx')
    sleep(4)
    grades = dict()
    count = 2
    while True:
        try:
            course_element = driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[' + str(count) + ']')
            course_name = course_element.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[' + str(count) + ']/td[2]').text
            course_credit = course_element.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[' + str(count) + ']/td[3]').text
            course_grade = course_element.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[' + str(count) + ']/td[4]').text
            grade_points = course_element.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[' + str(count) + ']/td[5]').text
            grades[course_name] = {}
            grades[course_name]["name"] = course_name
            grades[course_name]["credit"] = course_credit
            grades[course_name]["grade"] = course_grade
            grades[course_name]["points"] = grade_points
            count+=1
        except:
            break
    return grades

def test_email():
    global server
    html = "<p> " + 'You Will Receive Ashoka Grade Updates Here' + " <br> <br>Regards,<br><b>QuadCore Systems</b><br>[A YVJ Initiative]</p>"
    emailMsg = email.mime.multipart.MIMEMultipart('mixed')
    emailMsg['Subject'] = 'Ashoka Grade Updates'
    emailMsg['From'] = 'QuadCore Systems'
    emailMsg['To'] = EMAIL_ID
    emailMsg.attach(email.mime.text.MIMEText(html,'html'))
    try:
        server.sendmail(SENDER_EMAIL, EMAIL_ID, emailMsg.as_string())
    except:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, EMAIL_ID, emailMsg.as_string())

def server_login():
    try:
        global server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
    except Exception as e:
        print('Error Logging In (E-Mail)')
        print('Error:', str(e))
        raise 'Exception'

def login():
    try:
        driver.get('https://lms.ashoka.edu.in/')
        sleep(4)
        driver.find_element_by_xpath('//*[@id="Email"]').send_keys(EMAIL_ID)
        driver.find_element_by_xpath('//*[@id="next"]').click()
        # driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(EMAIL_ID)
        # driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(4)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(PASSWORD)
        driver.find_element_by_xpath('//*[@id="trustDevice"]').click()
        driver.find_element_by_xpath('//*[@id="submit"]').click()
        # driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(PASSWORD)
        # driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        sleep(4)
        print('Logged In')
    except Exception as e:
        print('Error Logging In')
        print('Error:', str(e))
        raise 'Exception'

def start_driver():
    global driver
    try:
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')  
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--headless") 
        if getattr(sys, 'frozen', False):
            chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
            driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        print('Driver Started')
    except Exception as e:
        print('Error Starting Driver')
        print('Error:', str(e))
        raise 'Exception'

def create_directory(grades):
    if os.path.exists(EMAIL_ID + '.json')==False:
        with open(EMAIL_ID + '.json', 'w') as f:
            pass
        print('Data File Created')
        write_file(grades)

def take_input():
    global EMAIL_ID
    global PASSWORD
    global SENDER_EMAIL
    global SENDER_PASSWORD
    EMAIL_ID = input('Enter Ashoka Email-ID: ')
    PASSWORD = getpass(prompt='Enter Password: ')
    SENDER_EMAIL = EMAIL_ID
    SENDER_PASSWORD = PASSWORD
    print_line()

def print_line():
    print()
    print('-----------------------------------------------------------------------------')
    print()

def print_header():
    print()
    print_line()
    print('\tAshoka Grade Checker - By QuadCore Systems [A YVJ Initiative]')
    print_line()

def main():
    print_header()
    take_input()
    try:
        start_driver()
        login()
        server_login()
        test_email()
        received_all_grades = False
        while not received_all_grades:
            grades = check_grade()
            create_directory(grades)
            new_grade = match_grade(grades)
            if new_grade:
                write_file(grades)
                received_all_grades = grade_count(grades)
            if not received_all_grades:
                sleeping()
        print('All Grades Recevied')
    except:
        pass
    finally:
        driver.close()
        server.quit()
        input('Press Enter To Terminate...')

if __name__ == "__main__":
    main()