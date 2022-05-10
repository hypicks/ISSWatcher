import requests
from datetime import datetime
import time
import smtplib

MY_EMAIL = "stenberg.p.b@gmail.com"
MY_PASSWORD = "##ThebigbadbearGmail89"

MY_LONG = 18.068581
MY_LAT = 59.329323

MY_POSITION = MY_LONG, MY_LAT


def iss_above_you():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

# API request, that gets sent back as a response. This is the END point
# response = requests.get(url="http://api.open-notify.org/iss-now.json")
#
# # This is the request module
# response.raise_for_status()
#
# # To get the information printed as data
# data = response.json()

# Gets the Long/Lat position in different variables
# iss_longitude = float(data["iss_position"]["longitude"])
# iss_latitude = float(data["iss_position"]["latitude"])

# Create tuple for position
# iss_position = (iss_longitude, iss_latitude)
#
# # Your position is within +5 or -5 degrees of the ISS position
# if iss_position == MY_POSITION:
#     print("Above you!")


def is_dark_enough():
    parameters = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    # It's dark
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_above_you() and is_dark_enough():
        email_message = f"Subject: Look Up!\n\nThe ISS is passing over you right now!".encode("utf-8")
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, 
                                to_addrs="bjorn.p.stenberg@gmail.com",
                                msg=email_message)

# If the ISS is close to my current position,
# and it is currently dark.
# Then email me to tell me to look up
# BONUS: run the code every 60 seconds

# Response code which we get back is 200 in this case.
# What is response codes? The most usual one is response code 404 - does not exist.
# 1XX - Hold On, something is happening
# 2XX - Here You Go, something is done and it did something
# 3XX - Go Away, you do not have permission to do this
# 4XX - You Screwed Up - does not exist
# 5XX - I Screwed Up - i.e. the server/data made a mistake/failure.
# .status_code returns only the status code.
# Here are all the Error codes: https://www.webfx.com/web-development/glossary/http-status-codes/

# If you would like to personalize your codes, you can do this for specific Error codes. Else use request modules
# if response.status_code == 404:
#     raise Exception("That resource does not exist.")
# elif response.status_code == 401:
#     raise Exception("You are not authorized to access this data")


