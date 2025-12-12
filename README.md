
# 🕵️‍♂️ Telegram Leak Monitor Guide

This tool allows you to scrape potential credit card leaks from public Telegram channels to verify if compromised credentials belong to you or your friends.

## 🚀 Setup

1.  **Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration (.env)**:
    Get your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
    Create a `.env` file:
    ```ini
    API_ID=123456
    API_HASH=abcdef123456789...
    SESSION_NAME=userbot_session
    ```

3.  **Run**:
    ```bash
    python userbot_scrapper.py
    ```
    *First time run will ask for your phone number and login code.*

## 🎮 Usage

Once the script is running, open Telegram (any chat, e.g., "Saved Messages") and use the command:

### Scrape a Channel
```
/sc https://t.me/target_channel_link
```
*   **What it does**: Scans **ALL** messages in that channel history.
*   **Output**: Finds cards in `PAN|MM|YY|CVV` format, performs Luhn validation, and uploads a text file with the list.

### Quick Scan (Optional Limit)
```
/sc https://t.me/target_channel_link 500
```
*   **What it does**: Scans only the last **500** messages. Useful for large channels to get recent leaks quickly.

## ⚠️ Disclaimer
This tool is for **defensive security and monitoring purposes only**.
- Do not use this to exploit or defraud.
- Only process data to verify if it belongs to you or authorized parties.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
