import asyncio
from email.mime.text import MIMEText
import smtplib
from temporalio import activity
import requests
import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
@activity.defn
async def fetch_weather(location: str) -> dict:
    api_key = os.environ.get('WEATHER_API_KEY')  # Use environment variable
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    weather_data = response.json()
    print(weather_data)
    return weather_data

@activity.defn  
async def send_email(recipient: str, weather_data: dict):
    sender = os.environ.get('SENDER_EMAIL')  # Use environment variable
    subject = "Weather Update"
    body = f"The current weather in your location is: {weather_data['weather'][0]['description']}, with a temperature of {weather_data['main']['temp']}°C."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    print(f"Sending email to {recipient}...", weather_data)
    # with smtplib.SMTP('localhost') as smtp:
    #     smtp.send_message(msg)

@activity.defn
async def store_data(location: str, weather_data: dict):
    SUPABASE_URL = "https://ateiiwftkupkvlpgeyqh.supabase.co"
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    # ------------------------------------------ Reomve this line ------------------------------------------
    
    response = supabase.table('countries').select("*").execute()
    print(response)
# ------------------------------------ Remove this line ------------------------------------------
    table_name = "weather_data"
    data = {
        "location": location,
        "description": weather_data['weather'][0]['description'],
        "temperature": weather_data['main']['temp']
    }
    supabase.table(table_name).insert(data).execute()

async def main():
    weather_data = await fetch_weather("London")
    await send_email("freetoweb7@gmail.com", weather_data)
    await store_data("London", weather_data)
if __name__ == "__main__":
    asyncio.run(main())