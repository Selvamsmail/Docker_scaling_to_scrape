import pandas as pd
import json
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
from tqdm import tqdm
import pika 

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
url_channel = connection.channel()
url_channel.queue_declare(queue='url_queue', durable=True)
data_channel = connection.channel()
data_channel.queue_declare(queue='data_queue', durable=True)


# method_frame, header_frame, body = channel.basic_get(queue='url_queue', auto_ack=True)
# channel.basic_publish(
#                 exchange='',
#                 routing_key='url_queue',
#                 body=message,
#                 properties=pika.BasicProperties(
#                     delivery_mode=2  # Make message persistent
#                 )
#             )

driver = Driver(
    uc=True,  # undetected-chromedriver
    headless=False   
)

    
while True:
    method_frame, header_frame, body = url_channel.basic_get(queue='url_queue', auto_ack=True)
    if not method_frame:
        break
    else:
        driver.get(json.loads(body).get('url'))
        time.sleep(1.5)
        try:
            if driver.find_element(By.CSS_SELECTOR,'.styles_exp-alert-message__nUbfX.styles_error__IhAVp'):
                continue
        except:
            pass
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.styles_key-skill__GIPn_ > div > a, .getJobKeySkillsSection.key-skill a')))
        except:
            print("...")
            driver.quit()
            driver = Driver(
                uc=True,  # undetected-chromedriver
                headless=False   
            )
            driver.get(json.loads(body).get('url'))
            time.sleep(4)
        try:
            job_title = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            job_title = "N/A"
        try:
            company_name = driver.find_element(By.CSS_SELECTOR, '.styles_jd-header-comp-name__MvqAI > a').text
        except:
            company_name = "N/A"

        try:
            experience = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__exp__k_giM, .slide-meta.getExperience > span').text
        except:
            experience = "N/A"

        try:
            salary = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__salary__jdfEC, .job-meta.slide-meta-sal').text
        except:
            salary = "N/A"
        try:
            location = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__loc___Du2H, .row.nomb.getCityLinks').text
        except:
            location = "N/A"

        try:
            description = driver.find_element(By.CSS_SELECTOR, '.styles_job-desc-container__txpYf > div > div , .nConfig_textblock').text
        except:
            description = "N/A"

        try:
            li_elements = driver.find_elements(By.CSS_SELECTOR, '.styles_key-skill__GIPn_ > div > a, .getJobKeySkillsSection.key-skill a')
            l = [i.text for i in li_elements]
        except:
            l = []

        try:
            posted_on = driver.find_element(By.CSS_SELECTOR, '.styles_jhc__stat__PgY67 > span, .sumFoot > span').text
        except:
            posted_on = "N/A"

        current_date = datetime.datetime.now().date()
        data = {
            'job_title':job_title,
            'company_name':company_name,
            'experience':experience,
            'salary':salary,
            'location':location,
            'description':description,
            'posted_on':posted_on,
            'current_date':current_date,
            'link':json.loads(body).get('url'),
        }
        for i in range(len(l)):
            data['skill'+str(i+1)]=l[i]
        try:
            lable_span = driver.find_elements(By.CSS_SELECTOR, '.styles_job-desc-container__txpYf > div > div.styles_other-details__oEN4O > div')    
            for lable in lable_span:
                labl = lable.find_element(By.CSS_SELECTOR, 'label').text
                ans = lable.find_element(By.CSS_SELECTOR, 'span').text
                data[labl] = ans
        except:
            lable_span = driver.find_elements(By.CSS_SELECTOR, '.getJobDescriptionOtherDetails.JD.av_textblock_section.jDisc.mt25 p')
            for lable in lable_span:
                labl = lable.find_element(By.CSS_SELECTOR, 'em').text
                ans = lable.find_element(By.CSS_SELECTOR, 'span').text
                data[labl] = ans
        if data != {}:
            message = {k: str(v) for k, v in data.items()}
            data_channel.basic_publish(
                exchange='',
                routing_key='data_queue',
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Make message persistent
                )
            )
            # tempdf = pd.DataFrame(data, index=[0])
            # tempdf['current_date'] = tempdf['current_date'].astype(str)
            # tempfilename = 'Naukri_raw1.parquet'  
            # save_data_to_disk(tempdf, tempfilename)
            # tempdf = pd.DataFrame()
            # save_state(strng)
        # strng = inde + 1