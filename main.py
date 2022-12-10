import requests
import datetime as dt
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY = "STOCK API KEY"
parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": API_KEY,
}
today = dt.date.today()
yesterday = today - dt.timedelta(days = 1)
yesterday = yesterday.strftime('%Y-%m-%d')
day_before_yesterday = today - dt.timedelta(days=2)
day_before_yesterday=day_before_yesterday.strftime('%Y-%m-%d')
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


response = requests.get(url=STOCK_ENDPOINT,params=parameters)
response.raise_for_status()
last_day_price = response.json()["Time Series (Daily)"][yesterday]
day_before_yesterday_price = response.json()["Time Series (Daily)"][day_before_yesterday]
yesterday_closing_price = float(last_day_price["4. close"])
print(yesterday_closing_price)

day_before_yesterday_closing_price = float(day_before_yesterday_price["4. close"])
print(day_before_yesterday_closing_price)

absoulute_difference = abs(day_before_yesterday_closing_price-yesterday_closing_price)
print(absoulute_difference)

percentage_difference = absoulute_difference/day_before_yesterday_closing_price*100
print(percentage_difference)

NEWS_API_KEY = "NEWS API KEY"
news_parameter = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}
# if percentage_difference>5:
new_response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameter)
new_response.raise_for_status()
articles = new_response.json()['articles'][:3]
if percentage_difference>5:
    for article in articles:
        title = article['title']
        description = article['description']
        print(title)
        print(description)
        account_sid = 'TWILIO SID'
        auth_token = 'TWILIO TOKEN'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"{title}\n\n{description}",
            from_='REGISTERED NUMBER',
            to='PHONE NUMBER WITH COUNTRY CODE'
        )
        print(message.sid)
