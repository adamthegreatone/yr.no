import time, datetime
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


while True:

    url = 'https://www.yr.no/place/Spain/Baleares/Palma_de_Mallorca/long.html'
    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, 'html.parser')
    forecast_before = str(soup.find('p').text)

    time.sleep(10)

    raw_html = simple_get(url)
    soup = BeautifulSoup(raw_html, 'html.parser')
    forecast_after = str(soup.find('p').text)


    if forecast_before != forecast_after:
        print('No change in the forecast')
        # print(forecast_before)
        # print(forecast_after)
        continue


    else:

        fromaddr = 'datascientist1987@gmail.com'
        toaddrs  = ['market.navra@gmail.com', 'djeidam@gmail.com']

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddrs)
        msg['Subject'] = "Subject: This is Adam\'s script talking, check YR.NO!"

        body = 'There is a change in the weather forecast in Mallorca! Check it out here: https://www.yr.no/place/Spain/Baleares/Palma_de_Mallorca/long.html \nText before: {}\nText after:{}'.format(forecast_before, forecast_after)

        msg.attach(MIMEText(body, 'plain'))


        # setup the email server,
        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        # add my account login name and password,
        server.login("datascientist1987@gmail.com", "Sracka123")

        text = msg.as_string()


        # send the email
        server.sendmail(fromaddr, toaddrs, text)
        # disconnect from the server
        server.quit()

        print('Change found, email sent')


# url = 'https://www.yr.no/place/Spain/Baleares/Palma_de_Mallorca/long.html'
# raw_html = simple_get(url)
# soup = BeautifulSoup(raw_html, 'html.parser')
# forecast_before = str(soup.find('p').text)
#
# print(forecast_before)