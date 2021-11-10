import pricedropalert.constants as const
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import smtplib
import time
from datetime import datetime


headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'})


class Alert:

    i = 0
    mail_sent = False

    def __init__(self):
        pass

    def amazon_price(self, url):
        request = Request(url, headers=headers)
        response = urlopen(request)

        html = response.read()
        html_soup = BeautifulSoup(html, 'html.parser')

        price = html_soup.find('span', id='priceblock_ourprice').text
        price = float(re.sub(r'[,₹]', '', price))

        return int(price)

    def flipkart_price(self, url):
        request = Request(url=const.FLIPKART_URL, headers=headers)
        response = urlopen(request)

        html = response.read()
        html_soup = BeautifulSoup(html, 'html.parser')

        price = html_soup.find('div', class_='_30jeq3 _16Jk6d').text
        price = int(re.sub(r'[,₹]', '', price))

        return price

    def send_email(self, website, URL, price):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(const.EMAIL_ID, const.PASSWORD)

        subject = f"Price dropped for {const.PRODUCT_NAME} on {website}"
        body = f'''The price of {const.PRODUCT_NAME} you are tracking dropped to {price} (less than or equal to your wish price).\n\n Order it by visiting {URL}'''

        msg = f"Subject:{subject}\n{body}"

        server.sendmail(const.EMAIL_ID, const.EMAIL_ID, msg)
        print("Email Sent!\n")
        print("--------------------------------------")
        print("Email Content:\n")
        print(msg)
        print("--------------------------------------")
        server.quit()


    def execute(self):
        Alert.i = Alert.i + 1

        print(f"No. of Price Enquiries: {Alert.i}\n")

        now = datetime.now()
        time_now = now.strftime("%B %d, %Y %H:%M:%S")

        amazon_price = self.amazon_price(const.AMAZON_URL)
        flipkart_price = self.flipkart_price(const.FLIPKART_URL)

        print(f"Amazon Price: {amazon_price}")
        print(f"Flipkart Price: {flipkart_price}")
        print(f"Your Wish Price: {const.WISH_PRICE}\n")

        while True:

            if amazon_price <= const.WISH_PRICE and flipkart_price > const.WISH_PRICE:
                self.send_email('Amazon', const.AMAZON_URL, amazon_price)
                Alert.mail_sent = True
                break

            if flipkart_price <= const.WISH_PRICE and amazon_price > const.WISH_PRICE:
                self.send_email('Flipkart', const.FLIPKART_URL, flipkart_price)
                Alert.mail_sent = True
                break

            if amazon_price <= const.WISH_PRICE and flipkart_price <= const.WISH_PRICE:
                if amazon_price <= flipkart_price:
                    self.send_email('Amazon', const.AMAZON_URL, amazon_price)
                    Alert.mail_sent = True
                    break
                else:
                    self.send_email('Flipkart', const.FLIPKART_URL, flipkart_price)
                    Alert.mail_sent = True
                    break

            else:
                print(f"Price for '{const.PRODUCT_NAME}' not yet dropped ({time_now}).\n")
                break



