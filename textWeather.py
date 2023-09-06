import requests
from twilio.rest import Client
import schedule
import time

def get_weather(latitude, longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,rain,showers&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch"
    response = requests.get(base_url)
    data = response.json()
    return data

def send_text_message(body):
    account_sid = "ACCOUNT_SID"
    auth_token = "AUTH_TOKEN"
    from_phone_number = "from_number" # twilio #
    to_phone_number = "to_number" # personal #
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = body,
        from_=from_phone_number,
        to=to_phone_number
    )
    print("Message Sent")
    
def send_weather_update():
    #Example location
    #hardcoded long/lat for Atlanta, Georgia
    latitude = 33.7488
    longitude = 84.3877
    
    weather_data = get_weather(latitude, longitude)
    temperature_fahrenheit = weather_data["hourly"]["temperature_2m"][0]
    relative_humidity = weather_data["hourly"]["relativehumidity_2m"][0]
    
    weather_info = {
        f"Good Morning!\n"
        f"Current weather in Atlanta, GA:\n"
        f"Temperature: {temperature_fahrenheit:.2f}°F\n"
        f"Relative Humidity: {relative_humidity}%\n"
    }
    
    send_text_message(weather_info)
        
    
def main():
    schedule.every().day.at("09:00AM").do(send_weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    
if __name__ == "__main__":
    main()