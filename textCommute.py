import datetime
from twilio.rest import Client
import googlemaps

def get_commute_duration():
    home_address = ""
    school_address = ""
    
    google_maps_apikey = ""
    gmaps = googlemaps.Client(key = google_maps_apikey)
    
    directions = gmaps.directions(home_address, school_address)
    first_leg = directions[0]['legs'][0]
    duration = first_leg['duration']['text']
    return duration

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

def main():
    duration = get_commute_duration()
    
    now = datetime.now()
    arrival_time = (now + duration).strftime('%I:%M %p')
    
    message = (
        f"Good Morning!\n\n"
        f"Estimated commute time from home to school at 9am: {duration}.\n\n"
        f"Leave now at 9am to arrive at school at approximately {arrival_time}.\n"
    )
    
    send_text_message(message)
    
if __name__ == "__main__":
    main()