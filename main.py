import requests
from datetime import datetime, timezone
import smtplib
import time

my_email = 'email@gmail.com'
my_password = 'password'
MY_LAT = 41.230181420628725
MY_LONG = -80.4619499012704


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc)
    hour_now = time_now.hour

    if sunrise >= hour_now >= sunset:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if iss_overhead() is True and is_night() is True:
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email, to_addrs='email@yahoo.com',
                                msg=f'Subject:Look Up!\n\nThe ISS is currently overhead. See if you can spot it!')
