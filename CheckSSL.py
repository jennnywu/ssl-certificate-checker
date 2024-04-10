# checks SSL certificate
# 3 lists are generates in result
#
# take input from websites.txt
# result is written into result.txt

import datetime
import requests
import socket
import ssl

file_object = open('result.txt', mode='w')

expired = []
expiring = []
dne = []

now = datetime.datetime.today()

print()
print('SSL CERTIFICATE VALIDITY CHECKER test', file=file_object)
print("*********************************", file=file_object)
print()

old_urls = open('websites.txt', 'r')

my_urls = []

for element in old_urls:
    element = element.strip()
    my_urls.append(element)


# check validity
def check_ssl(url):
    if "https://" not in url:
        url = "https://" + url

    try:
        req = requests.get(url, verify=True)
        return True

    except requests.exceptions.SSLError:
        print(url + " is expired :(", file=file_object)
        expired.append(url)
        return False

    except requests.exceptions.ConnectionError:
        print(url + " does not exist :(", file=file_object)
        dne.append(url)
        return False


# check expiry date
def checking(url):
    dateformat = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket \
            (
            socket.socket(socket.AF_INET),
            server_hostname=url,
        )

    conn.connect((url, 443))
    ssl_info = conn.getpeercert()
    date = datetime.datetime.strptime(ssl_info['notAfter'], dateformat)

    diff = date - now

    if diff.days <= 31:

        if "https://" not in url:
            url = "https://" + url

        print(url + " expires in ", end="", file=file_object)
        print(diff.days, end="", file=file_object)
        print(" days.", file=file_object)
        expiring.append(url)

    else:
        pass


for url in my_urls:
    if check_ssl(url):
        checking(url)

print(file=file_object)
print("Expired URLs: ", end="", file=file_object)
print(*expired, sep=", ", file=file_object)
print("Expiring URLs: ", end="", file=file_object)
print(*expiring, sep=", ", file=file_object)
print("Nonexistent URLs: ", end="", file=file_object)
print(*dne, sep=", ", file=file_object)

input("Press any key to exit: ")
