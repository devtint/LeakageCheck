import os
import re
import sys
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events # type: ignore

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "userbot_session"

if not API_ID or not API_HASH:
    print("Error: API_ID and API_HASH must be set in .env file.")
    sys.exit(1)

client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

FULLZ_PATTERN = r'(\d{13,19})[\|/:;,\s-]+(\d{1,2})[\|/:;,\s-]+(\d{2,4})[\|/:;,\s-]+(\d{3,4})'

def luhn_check(card_number: str) -> bool:
    digits = [int(d) for d in str(card_number)]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 1:
            doubled = digit * 2
            if doubled > 9: doubled -= 9
            checksum += doubled
        else:
            checksum += digit
    return checksum % 10 == 0

def clean_number(raw_number: str) -> str:
    return raw_number.replace(" ", "").replace("-", "")

async def scrape_channel(channel_link: str, limit: int = None) -> list[str]:
    found_cards = set()
    
    try:
        entity = await client.get_entity(channel_link)
        
        limit_text = "ALL" if limit is None else str(limit)
        print(f"   > Accessing {channel_link} (Limit: {limit_text})...")
        
        async for message in client.iter_messages(entity, limit=limit):
            if message.text:
                matches = re.findall(FULLZ_PATTERN, message.text)
                for match in matches:
                    pan, month, year, cvv = match
                    
                    pan = clean_number(pan)
                    
                    if 13 <= len(pan) <= 19 and luhn_check(pan):
                        if len(month) == 1: month = "0" + month 
                        if len(year) == 2: year = "20" + year
                        
                        formatted_card = f"{pan}|{month}|{year}|{cvv}"
                        found_cards.add(formatted_card)
                        
    except Exception as e:
        print(f"Error scraping {channel_link}: {e}")
        return []

    return list(found_cards)

@client.on(events.NewMessage(pattern=r'/sc'))
async def sc_handler(event):
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply("Usage: `/sc <channel_link> [optional_limit]`")
        return

    channel_link = args[1]
    
    limit = None
    if len(args) > 2:
        try:
            limit = int(args[2])
        except ValueError:
            pass 

    limit_str = "ALL" if limit is None else str(limit)
    status_msg = await event.reply(f"🔍 Scraping {channel_link} for potential cards... (Limit: {limit_str} messages)\nThis may take a while for large channels!")

    cards = await scrape_channel(channel_link, limit)

    if cards:
        filename = f"leak_report_{channel_link.split('/')[-1]}.txt"
        with open(filename, "w") as f:
            f.write(f"Source: {channel_link}\n")
            f.write(f"Scanned Messages: {limit_str}\n")
            f.write(f"Found: {len(cards)} cards\n")
            f.write("-" * 20 + "\n")
            f.write("\n".join(cards))
        
        await event.reply(f"✅ Found {len(cards)} cards in {channel_link}. Uploading list...", file=filename)
        
        try:
            os.remove(filename)
        except:
            pass
            
        await status_msg.delete()
    else:
        await status_msg.edit(f"No valid cards found in {channel_link} (Check limit: {limit_str}).")

async def main():
    print("Starting Userbot...")
    await client.start()
    print("Userbot is running! Waiting for commands (e.g. /sc <link>)...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
