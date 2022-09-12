import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import csv
from operator import itemgetter

#S7-1500 version is 2.9.4
#S7-1500 Software Controller version is Software V21.9.4:

def parse_summary(text):
    if text.find("). ") == -1:
        return text
    else:
        index = text.index("). ") + 3
        return text[index:]

file = open("./specificproducts", "r")
lines = file.readlines()
header = ['vendor', 'product', 'associated cve', 'cvss', 'cve description', 'vulnerability type(s)']
cve_list = []
vendor = ""
product = ""
vulnerability_dict = {"denial of service" : ["dos", "denial of service", "denial-of-service"],
                      "code execution" : ["code execution" "arbitrary code"],
                      "overflow" : ["overflow", "overread", "over flow", "over read", "over-flow", "over-read"],
                      "memory corruption" : ["memory corruption"],
                      "injection" : ["injection", "inject"],
                      "xss" : ["xss", "cross site scripting"],
                      "directory traversal" : ["directory traversal"],
                      "http response splitting" : ["http response splitting"],
                      "bypass" : ["bypass"],
                      "gain privileges" : ["gain privileges", "elevation of privilege"],
                      "csrf" : ["csrf", "cross site request forgery", "cross-site-request-forgery"],
                      "cryptography" : ["cryptographic", "cryptography", "encrypt", "decyrpt", "encryption", "decryption"] ,
                      "phishing" : ["phishing", "phish"],
                      "information disclosure" : ["information disclosure", "disclosure of information", "information-disclosure"],
                      "man in the middle" : ["man in the middle", "man-in-the-middle", "manipulator in the middle", "manipulator-in-the-middle"]}
with open('specific_output.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(header)
    
    for line in lines:
        if line.isupper():
            vendor = line.strip().lower()
        else:
            product = line.strip()
            api_url = f"https://localhost/api/search/{vendor}/{product}"
            response = requests.get(api_url, verify=False).json()
            results = response["results"]
            names = ""
            if results:
                writer.writerow([vendor, product])
            product_vulnerabilities = []
            for vulnerability in results:
                id = vulnerability["id"]
                year = int(id[4:8])
                if year < 2019:
                    continue
                full_summary = vulnerability["summary"]
                score = vulnerability["cvss"]
                #useful_summary = parse_summary(full_summary)
                useful_summary = full_summary
                single_type = ""
                for type in vulnerability_dict:
                    for variation in vulnerability_dict[type]:
                        if variation in useful_summary.lower() and type not in single_type:
                            single_type += type + ", "
                if single_type:
                    single_type = single_type[:-2]
                else:
                    single_type = "N/A"
                product_vulnerabilities.append(['', '', id, score, useful_summary, single_type])
                
            product_vulnerabilities = sorted(product_vulnerabilities, key=itemgetter(3), reverse=True)
            for vulnerability in product_vulnerabilities:
                writer.writerow(vulnerability)



    