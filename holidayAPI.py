import requests
from bs4 import BeautifulSoup
import datetime

url = "https://www.calend.ru/holidays/"


def getTodayDate():
    # get today date in format yyyy-mm-dd
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")


def getHoliday(date=getTodayDate()):
    response = requests.get(url+date+"/")
    soup = BeautifulSoup(response.text, 'html.parser')
    # extract holiday name from path ".holidays>.title"
    holiday = soup.select(".holidays .title")
    # if holiday is not found, return None
    if len(holiday) == 0:
        return None
    # else return holiday names
    return [h.text.strip() for h in holiday]


print(getHoliday())
