import redis
import json
import virustotal_python
from pprint import pprint
from base64 import urlsafe_b64encode
from collections import Counter
import logging
import datetime as dt
logging.basicConfig(filename=f'/tmp/vtotal_{dt.datetime.now().timestamp()}.log', level=logging.INFO)
def check_site_list(lst_of_results):
    if(('malicious' in  lst_of_results)| ('phishing' in  lst_of_results) | ('malware' in  lst_of_results)):
        return('risk')
    return('safe')

def list_to_dict(lst):
    count_dict = dict(Counter(lst))
    return count_dict

logging.basicConfig(filename='/tmp/myapp.log', level=logging.INFO)
logging.info('lklakslkas')

def get_vtotal(url):
    
    v_token="xxx"
    with virustotal_python.Virustotal(v_token) as vtotal:
        try:
            resp = vtotal.request("urls", data={"url": url}, method="POST")
            # Safe encode URL in base64 format
            # https://developers.virustotal.com/reference/url
            url_id = urlsafe_b64encode(url.encode()).decode().strip("=")
            report = vtotal.request(f"urls/{url_id}")
            logging.info(str(report.json()))
            return(report.json())
        except virustotal_python.VirustotalError as err:
            print(f"Failed to send URL: {url} for analysis and get the report: {err}")

def get_site_data(site):
    json_report=get_vtotal(site)
    
def get_site_data(site):
    report_json=get_vtotal(site)
    result_list=report_json['data']['attributes']['last_analysis_results'].values()
    lst_of_results= list(map(lambda x: x['result'], result_list))
    site_status=check_site_list(lst_of_results)
    categories_list = list(report_json['data']['attributes']['categories'].values())
    categories_dict = list_to_dict(categories_list)
    return({ 'state': site_status, 'tags': categories_dict})   

#the update happens only if the record alreay expired            
def update_database(site, expiration=1800):
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    result=redis_client.get(site)
    if (result==None):
        site_data=get_site_data(site)
        json_data = json.dumps(site_data)  # Convert the data to JSON string
        redis_client.set(site, json_data, ex=expiration )
        print(f"in update_database site: {site}. values {json_data} ")
    else:
        print(f"information for site: {site} already exist: {result}, skip site call")
    redis_client.close()
import pandas as pd
pd_sites=pd.read_csv('/tmp/sites/my_sites.csv', header=None)
pd_sites[0].apply(lambda x: update_database(x))
