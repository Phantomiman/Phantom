import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
def importer():
    while True:
        print("""\   WELCOME TO SAMS'S SCRIPT  / 
        =====================================================================
        1) Check logs of file that resides in your computer
        2) Send requests and scan for vulnerabilities
        3) Scan for robots.txt file
        4) Scan for Google Dorks On Target
        5) Exit""")
        try:
            typer = int(input("[+] Please choose option :"))
            if typer == 1:
                filename = input(" [+] Please give us a file name >>  ")
                with open(filename,"r+") as f:
                    f = (f.read())
                    file = input(" [+] Type the syntax you want to check in the file : ")
                    check = (file in f)
                if check == True:
                    result = input(" [+] The file contains the syntax you have choosen, type 'again' to scan again >> ")
                    if result == "again":
                        pass
                    else:
                        break

                else:
                    print(" [-] ERROR : The file doesn't contain the syntax ")
                    break
            if typer == 2:
                print("[+] The script scans sensetive information for a manipulation ")
                urlcheck = input("[+] Please choose url to check >> ")









                websites = urlcheck

                df = pd.DataFrame(columns=["Website", "Vulnerability", "Status"])

                for website in websites:

                    response = requests.get(website)


                    soup = BeautifulSoup(response.text, "html.parser")

                    xss = False
                    for tag in soup.find_all():
                        if "onmouseover" in tag.attrs:
                            xss = True
                            break

                    csrf = False
                    for tag in soup.find_all("form"):
                        if "csrf" not in tag.attrs.get("action", ""):
                            csrf = True
                            break

                    injection = False
                    injection_payload = "' OR '1'='1"
                    login_url = f"{website}/login"
                    response = requests.post(login_url, data={"username": injection_payload, "password": "password"})
                    if re.search(r"error|invalid|incorrect|failed", response.text, re.I):
                        injection = True

                    auth = False
                    weak_password = "password"
                    response = requests.post(login_url, data={"username": "user", "password": weak_password})
                    if "logged in" in response.text:
                        auth = True

                    direct_object_ref = False
                    resource_url = f"{website}/users/user1"
                    response = requests.get(resource_url)
                    if "Access denied" not in response.text:
                        direct_object_ref = True

                    misconfig = False
                    if soup.find("a", text="admin"):
                        misconfig = True
                    if soup.find("a", text="Powered by WordPress"):
                        misconfig = True
                    if "X-Frame-Options" not in response.headers:
                        misconfig = True
                    if "X-Content-Type-Options" not in response.headers:
                        misconfig = True
                    if "X-XSS-Protection" not in response.headers:
                        misconfig = True
                    if "Content-Security-Policy" not in response.headers:
                        misconfig = True

                    data_exposure = False

            if typer == 3:
                url = input("[+] Send URL to scan >>> ")
                if url.endswith('/'):
                    path = url
                else:
                    path = url + '/'
                req = requests.get(path + 'robots.txt')
                if req.status_code == 200:
                    found = req.text
                    print("[+] The results are : {0}".format(found))
                    logsaver = input("[+] Would You Like To Save The Robots.txt content ? [Y]es [N]O ")
                    if logsaver == "Y" or "y":
                        with open("logofrobots.txt", 'w+') as f:
                            f.write(req.text)
                            print("File saved as logoofrobots.txt")
                    else:
                        break
                else:
                    print("[-] Seemingly the file we are searching doesn't exist")
                    break
            if typer == 4:
                    print("[+] This section generates several links with Google Dorks capabilities.")
                    domain = input("[+] Please type the exact domain >> [E.X : target.com ] >>  ")
                    googleSearch('Site:{0} -site:www.{0}'.format(domain))
                    googleSearch("intitle:index of / Parent Directory site: {0}".format(domain))
                    googleSearch("intitle:Index of /admin site: {0}".format(domain))
                    googleSearch("Intitle: login admin site: {0}".format(domain))
                    googleSearch("inurl /cpanel/login.php site: {0}".format(domain))
                    googleSearch("inurl:login site: {0}".format(domain))

            if typer == 5:
                break
        except Exception as e:
            print("[-] An Error occured: {0}".format(e))


def googleSearch(query):
    with requests.session() as c:
        url = 'https://www.google.com'
        query = {'q': query}
        urllink = requests.get(url, params=query)
        print(urllink.url)

