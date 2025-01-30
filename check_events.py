import requests
import json
from datetime import datetime
import os
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '300'))
VENUE_ID = os.getenv('VENUE_ID', '334')

async def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram configuration missing. Please check your .env file.")
        return
    
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='HTML')
    except Exception as e:
        print(f"Error sending Telegram message: {str(e)}")

def fetch_events():
    url = "https://iticket.com.tr/en/events"
    params = {
        "venue_id": VENUE_ID
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        eventsData = soup.find_all("a", class_="event-list-item")

        events = []
        for event in eventsData:
            events.append({
                "title": event.find("div", class_="event-name").text.strip(),
                "date": event.find("div", class_="event-date").text.strip(),
                "url": "https://iticket.com.tr" + event["href"]
            })

        return events
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return None

def load_previous_events():
    if os.path.exists('previous_events.json'):
        try:
            with open('previous_events.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading previous events: {str(e)}")
    return []

def save_events(events):
    try:
        with open('previous_events.json', 'w') as f:
            json.dump(events, f, indent=2)
    except Exception as e:
        print(f"Error saving events: {str(e)}")

async def check_new_events():
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{current_time}] Checking for new events...")
        
        current_events = fetch_events()
        if current_events is None:
            print("Failed to fetch events, will retry in", CHECK_INTERVAL, "seconds")
            await asyncio.sleep(CHECK_INTERVAL)
            continue
        
        previous_events = load_previous_events()
        
        # Convert events to set of tuples for comparison
        current_event_set = {(event['title'], event['date'], event['url']) for event in current_events}
        previous_event_set = {(event['title'], event['date'], event.get('url', '')) for event in previous_events}
        
        # Find new events
        new_events = current_event_set - previous_event_set
        
        if new_events:
            print(f"Found {len(new_events)} new events:")
            # Prepare message for Telegram
            message = f"🎫 Found {len(new_events)} new events:\n\n"
            for event in new_events:
                event_msg = f"🎭 <b>{event[0]}</b>\n📅 {event[1]}\n🔗 {event[2]}\n\n"
                message += event_msg
                print(f"New event: {event[0]} on {event[1]}")
            
            # Send Telegram message
            await send_telegram_message(message)
        else:
            print("No new events found")
        
        # Save current events for next comparison
        save_events(current_events)
        
        print(f"Waiting {CHECK_INTERVAL} seconds before next check...")
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if not os.path.exists('.env'):
        print("Error: .env file not found!")
        print("Please create a .env file with TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
        sys.exit(1)
        
    print("Starting event checker...")
    print(f"Will check for new events every {CHECK_INTERVAL} seconds")
    asyncio.run(check_new_events()) 