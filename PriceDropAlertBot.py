from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import smtplib
import time

headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'})

PRODUCT_NAME = 'iPad Pro M1' #for example
AMAZON_URL = 'https://www.amazon.in/Apple-iPad-Pro-11-inch-27-96-Cellular/dp/B0932R3PMQ/ref=sr_1_1?crid=JD2BW59GT5SR&dchild=1&keywords=ipad+pro+m1&qid=1635764167&sprefix=ipad+pro+m%2Caps%2C326&sr=8-1'
FLIPKART_URL = 'https://www.flipkart.com/apple-ipad-pro-2021-3rd-generation-8-gb-ram-256-rom-11-inches-wi-fi-5g-space-grey/p/itm4f5d1315fdfe7?pid=TABG3YZNBDADBN7T&lid=LSTTABG3YZNBDADBN7T63PY5J&marketplace=FLIPKART&q=ipad+pro+m1&store=tyy%2Fhry&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=64a3682d-cf5c-4069-a742-dd4e12406ffb.TABG3YZNBDADBN7T.SEARCH&ppt=sp&ppn=sp&ssid=ank3tfrn8w0000001635764180888&qH=581be6ed13a94224'
WISH_PRICE = 90000
EMAIL_ID = 'you@gmail.com' #same mail will be used for sending & receving the alerts here
PASSWORD = 'yourpassword'


def amazon_price(url):
    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        html = response.read()
        html_soup = BeautifulSoup(html, 'html.parser')
        price = html_soup.find('span', id='priceblock_ourprice').text
        price = float(re.sub(r'[,₹]', '', price))
    except Exception as e:
        print("Can't load Amazon.in")
    return int(price)


def flipkart_price(url):
    try:
        request = Request(url=FLIPKART_URL, headers=headers)
        response = urlopen(request)
        html = response.read()
        html_soup = BeautifulSoup(html, 'html.parser')
        price = html_soup.find('div', class_='_30jeq3 _16Jk6d').text
        price = int(re.sub(r'[,₹]', '', price))
    except Exception as e:
        print("Can't load Flipkart.in")
        return price


def send_email(website, URL, price):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_ID, PASSWORD)
    subject = f"Price dropped for {PRODUCT_NAME} on {website}"
    body = f'''The price of {PRODUCT_NAME} you are tracking dropped to {price} (less than or equal to your wish price).\n\n Order it by visiting {URL}'''
    msg = f"Subject:{subject}\n\n\n\n{body}"
    server.sendmail(EMAIL_ID, EMAIL_ID, msg)
    print("email sent\n")
    print("Email Content:\n")
    print(msg)
    server.quit()


amazon_price = amazon_price(AMAZON_URL)
flipkart_price = flipkart_price(FLIPKART_URL)

print(f"Amazon Price: {amazon_price}")
print(f"Flipkart Price: {flipkart_price}")

count = 0
i=1
while count == 0:
    print(f"No. of Price Enquiries: {i}")

    if amazon_price <= WISH_PRICE and flipkart_price > WISH_PRICE:
        send_email('Amazon', AMAZON_URL, amazon_price)
        count = count + 1
        break

    if flipkart_price <= WISH_PRICE and amazon_price > WISH_PRICE:
        send_email('Flipkart', FLIPKART_URL, flipkart_price)
        count = count + 1
        break

    if amazon_price <= WISH_PRICE and flipkart_price <= WISH_PRICE:
        if amazon_price <= flipkart_price:
            send_email('Amazon', AMAZON_URL, amazon_price)
            count = count + 1
            break
        else:
            send_email('Flipkart', FLIPKART_URL, flipkart_price)
            count = count + 1
            break
    i=i+1
    time.sleep(21600) #price enquiry will be made every 6 hours (can be customised)
