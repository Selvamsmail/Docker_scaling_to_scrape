import requests
import pandas as pd
import json
import pika

##################################################################################################################

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Ensure the queue exists
channel.queue_declare(queue='url_queue', durable=True)

##################################################################################################################

def job_extract(url):    
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.7',
        'appid': '109',
        'clientid': 'd3skt0p',
        'content-type': 'application/json',
        'gid': 'LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE',
        'nkparam': 'ccALYVnCX0UW3/kXgze2dLkgIVEJCGmJPekTqX0UUyXEONwJ4xwZqqTe1Zv+o12FzYsXsIJCG+q8T1obHf4Rjw==',
        'priority': 'u=1, i',
        'referer': 'https://www.naukri.com/smart-metering-jobs-2',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'systemid': 'Naukri',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        # 'cookie': 'test=naukri.com; _t_ds=dad84d11725966280-20dad84d1-0dad84d1; J=0; MYNAUKRI[UNID]=82833c6c37294cbf94eada51038e8707; _ff_ds=0689945001727669852-C4D9453A951E-0B2CA997C18E; PS=cad81a7e1e2920a6fe087bd22d46d5c695be1fe02d4bd9d1f71baa5026cee48c92d2d6ac5f21f68f; _did=066b83d803; _odur=3019dcd5a3; kycEligibleCookie124608632=true; ACCESS=1738295610544; UNID=vlsKmECw544ge9Y7roUAAAFMkN3FcVomgSWGFlaj; UNPC=124608632; UNCC=124814168; loginPreference=null_null; lastLoggedInUser=9442054516h5TGllSt1o_mobUser; promobnr=FASTJOB20; bm_mi=0B76F1060D08E28FF8A7208692908D3F~YAAQ0UvSF9JUB9mUAQAAH4zNIxpc/s9rapGgbLiTmrhnUNcsVZa8NmL3fN+t4jXX3l6oDdA6KMtHQNW5Q7ULGrWF6B3YomZvqLNTRmdMutDPR0iBheT2K1lf5J8igzORRihm5Wa/4JAicCrqzJ0FLnuMb03/6y8JwhzClYYZgKQI/INN9tOxEnYDHtWoeh5sWF6+qoy1/2e5M5h3wuVPC3iHa18JSBXlpGtLK19pk2Te1JVVrls5aogBpiTXQHOhB/FmyRCHgBvIHGbTJ8aHxTespE8K6NWWHrnjW1dRJdI/TVVmwmRHT56ZshuCgv32yakFgLQR1t/tbjbEDFE=~1; ak_bmsc=892B819C3DC00ABA02B5C8D4ABDA0A0B~000000000000000000000000000000~YAAQ0UvSF/RUB9mUAQAAjJPNIxrp4C3a6BAeP81Q9F9yaCLRotQVw9mAnX55luYV4lPcjcMCyAUZdv93uTHXVACJdJMN64MzY2QqaFWy2iwt/RaOwJyrbSwgRs7u3eD44qxlCM6nBUusDx63cw3PR0A1ab/LY6RcZ8j2DzwwvzJWfZZlK0UKL7MWhmmZjRpckVbzeaRMqhcf/5un9oXMVws/UnrVTqSnLMQnDP9F+S/TZynQS0h0T4evoLp5OVPwUAYpOLmukYFKco+jXK+4fn25EM05hyc1wZkXAa1ed/yXU9nOnSrESKUQu4M0h/mcEFA0sYWLTms40bic3pbOPP58+RnJdoyruUwPyzvEnB3Rfve+YuuG6sDZ8AdqLE7H+JUF6U4W0VmOVj1gxFGDEkmMoAF796xs5/wJtp+cNUvpxx4octxcTvRu9eES1S7cCK25N7MKI0enfpZSazJ054AsnDNSY6WxWJsb0drj9Dn5Acl7CRo/11uRliNuuEDV; ACTIVE=1740062457; PHPSESSID=dfc10tm1cpe0klmkm8adi4lhlj; _t_us=67B74816; _t_s=direct; _t_r=1030%2F%2F; persona=default; bm_sv=D750334A884D97D83A63F32C40A2DA7B~YAAQ0UvSF8uECNmUAQAAQS4DJBrB5sap85i0eZnjz4TChN6v36lt6P5pkpq8zaP8kRYKoAS6pSLY6rv4bZ9Bh4PzGo/ws+StN+DgP94MRwvJaFcVJtxsqwd2a0AT6ZWKVG56N/OOK2HVGa+4VFqwPO2zFfwt6WTeWim0eb/Bs0fu1NnsFUyU3nXqry40qZxVf/9tdSASxB1VuAXARYkh7oxlCSa0d/k0vAIx4WQJlvbRnmpd2oBwbtYd43J1UALYBQ==~1',
    }

    params = {
        'noOfResults': '20',
        'urlType': 'search_by_keyword',
        'searchType': 'adv',
        'keyword': 'smart metering',
        'pageNo': '2',
        'sort': 'r',
        'seoKey': 'smart-metering-jobs-2',
        'src': 'seo_srp',
        'latLong': '',
        'sid': '17400659409967805',
    }

    response = requests.get(url,params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")


##################################################################################################################


dontwantlis = {'vacancy', 'consultant', 'hideClientName',
            'clientHeadline', 'jobType', 'date', 'brandingTags', 'exclusive',
            'duration', 'hiringFor', 'clientLogo', 'clientCareersUrl',
            'clientGroupId', 'smbJobFields', 'internshipTags',
            'groupId','isTopGroup','createdDate','mode','board',
            'showMultipleApply','logoPath','logoPathV3', 'companyId',
            'isSaved','footerPlaceholderColor','currency','jobId'}

url = f'https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_location&searchType=adv&location=india&sort=r&pageNo=1&clusters=functionalAreaGid&seoKey=jobs-in-india'
ran = job_extract(url)['noOfJobs']
ran = ran//20
for i in range(ran):
    print(f'\r processing {i} out of {ran}',end= '')
    url = f'https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_location&searchType=adv&location=india&sort=r&pageNo={str(i)}&clusters=functionalAreaGid&seoKey=jobs-in-india'
    
    try: a = job_extract(url)['jobDetails']
    except: continue
    cleaned_data = []
    for c in a:
        c = {donts:c[donts] for donts in c.keys() if donts not in dontwantlis}
        contflag = 0
        for dic in c['placeholders']:
            if (dic['type'] == 'salary') and (dic['label'].lower() == 'not disclosed'):
                contflag = 1
        if contflag == 1:
            continue
        for dic in c['placeholders']:
            c[dic['type']] = dic['label']
        try:
            for dic in c['ambitionBoxData']:
                c['Ambi_'+str(dic)] = c['ambitionBoxData'][dic]
        except:None
        try: del c['placeholders']
        except:None
        try: del c['ambitionBoxData']
        except:None
        cleaned_data.append(c)
    tempdf = pd.DataFrame(cleaned_data)
    if not tempdf.empty:
        tempdf = tempdf.rename(columns={'footerPlaceholderLabel':'posted_on','title':'job_title','companyName':'company_name','jdURL':'link'})
        tempdf['link'] = 'https://www.naukri.com'+tempdf['link']
        tempfilename = 'links.parquet'  # Change the file extension to '.parquet'
        tempdf.to_csv(tempfilename,index=False)
        
        for url in tempdf['link']:
            message = json.dumps({'url': url})
            channel.basic_publish(
                exchange='',
                routing_key='url_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Make message persistent
                )
            )
        
        tempdf = pd.DataFrame()