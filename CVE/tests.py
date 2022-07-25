import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

response = requests.get("https://localhost/api/search/siemens/simatic_s7-1500_firmware", verify=False).json()
print(len(response["results"]))
print(response["results"][0]['id'])
