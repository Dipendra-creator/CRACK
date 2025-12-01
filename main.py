import os
from dotenv import load_dotenv
import requests
import json
from random import randint
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
load_dotenv()
LEAKOSINT_API_URL = os.getenv("LEAKOSINT_API_URL", "https://leakosintapi.com/")
LEAKOSINT_API_TOKEN = os.getenv("LEAKOSINT_API_TOKEN", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Settings
DEFAULT_LANG = "en"
DEFAULT_LIMIT = 300
MAX_MESSAGE_LENGTH = 4096

# Storage for reports
cached_reports = {}

# Authorized users (set to None to allow all users, or use a list of user IDs)
AUTHORIZED_USERS = None  # Example: [123456789, 987654321]


def is_user_authorized(user_id):
    """Check if user has access to the bot"""
    if AUTHORIZED_USERS is None:
        return True
    return user_id in AUTHORIZED_USERS


def generate_report(query, query_id):
    """
    Generate a report from the Leakosint API
    Returns a list of formatted report pages or None on error
    """
    global cached_reports
    
    data = {
        "token": LEAKOSINT_API_TOKEN,
        "request": query.split("\n")[0],
        "limit": DEFAULT_LIMIT,
        "lang": DEFAULT_LANG
    }
    
    try:
        logger.info(f"Searching for: {query}")
        response = requests.post(LEAKOSINT_API_URL, json=data, timeout=30)
        response.raise_for_status()
        json_response = response.json()
        
        logger.info(f"API Response: {json_response}")
        
        # Check for errors
        if "Error code" in json_response:
            logger.error(f"API Error: {json_response['Error code']}")
            return None
        
        # Process results
        cached_reports[str(query_id)] = []
        
        if "List" not in json_response:
            logger.warning("No 'List' in response")
            return None
        
        for database_name, database_data in json_response["List"].items():
            text_lines = [f"<b>📊 {database_name}</b>", ""]
            
            # Add leak info if available
            if "InfoLeak" in database_data:
                text_lines.append(f"ℹ️ {database_data['InfoLeak']}\n")
            
            # Add data entries
            if database_name != "No results found" and "Data" in database_data:
                for idx, record in enumerate(database_data["Data"], 1):
                    text_lines.append(f"<b>Record #{idx}</b>")
                    for column_name, column_value in record.items():
                        text_lines.append(f"  • <b>{column_name}</b>: {column_value}")
                    text_lines.append("")
            
            text = "\n".join(text_lines)
            
            # Truncate if too long
            if len(text) > MAX_MESSAGE_LENGTH - 100:
                text = text[:MAX_MESSAGE_LENGTH - 150] + "\n\n⚠️ <i>Message truncated - too much data</i>"
            
            cached_reports[str(query_id)].append(text)
        
        return cached_reports[str(query_id)]
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


def create_navigation_keyboard(query_id, current_page, total_pages):
    """Create inline keyboard for navigation"""
    markup = InlineKeyboardMarkup()
    
    if total_pages <= 1:
        return markup
    
    # Handle page wrapping
    if current_page < 0:
        current_page = total_pages - 1
    elif current_page >= total_pages:
        current_page = current_page % total_pages
    
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton(
            text="⬅️ Previous",
            callback_data=f"/page {query_id} {current_page - 1}"
        ),
        InlineKeyboardButton(
            text=f"{current_page + 1}/{total_pages}",
            callback_data="page_info"
        ),
        InlineKeyboardButton(
            text="Next ➡️",
            callback_data=f"/page {query_id} {current_page + 1}"
        )
    )
    
    return markup


# Initialize bot
if not TELEGRAM_BOT_TOKEN:
    logger.error("Please set TELEGRAM_BOT_TOKEN environment variable or provide a .env file!")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle /start and /help commands"""
    welcome_text = """
🔍 <b>Leakosint Search Bot</b>

Welcome! I can search leaked databases using the Leakosint API.

<b>How to use:</b>
Simply send me a search query (email, name, phone number, etc.) and I'll search for it in the database.

<b>Examples:</b>
• example@gmail.com
• John Smith
• +1234567890

<b>Commands:</b>
/start - Show this message
/help - Show this message
/stats - Show API statistics

⚠️ <i>Use responsibly and only for legitimate purposes.</i>
"""
    bot.reply_to(message, welcome_text, parse_mode="HTML")


@bot.message_handler(commands=['stats'])
def send_stats(message):
    """Show bot statistics"""
    stats_text = f"""
📊 <b>Bot Statistics</b>

API URL: {LEAKOSINT_API_URL}
Default Search Limit: {DEFAULT_LIMIT}
Language: {DEFAULT_LANG}
Cached Reports: {len(cached_reports)}

<i>Type any search query to begin searching.</i>
"""
    bot.reply_to(message, stats_text, parse_mode="HTML")


@bot.message_handler(func=lambda message: True)
def handle_search_query(message):
    """Handle search queries"""
    user_id = message.from_user.id
    
    # Check authorization
    if not is_user_authorized(user_id):
        bot.send_message(
            message.chat.id,
            "❌ You are not authorized to use this bot."
        )
        return
    
    # Only process text messages
    if message.content_type != "text":
        bot.send_message(
            message.chat.id,
            "⚠️ Please send a text query to search."
        )
        return
    
    # Generate unique query ID
    query_id = randint(10000000, 99999999)
    
    # Send "searching" message
    searching_msg = bot.send_message(
        message.chat.id,
        "🔎 Searching databases, please wait..."
    )
    
    # Perform search
    report_pages = generate_report(message.text, query_id)
    
    # Delete "searching" message
    try:
        bot.delete_message(message.chat.id, searching_msg.message_id)
    except:
        pass
    
    # Handle errors
    if report_pages is None or len(report_pages) == 0:
        bot.reply_to(
            message,
            "❌ <b>Search failed</b>\n\nThe API may be unavailable or there was an error processing your request.",
            parse_mode="HTML"
        )
        return
    
    # Send first page
    markup = create_navigation_keyboard(query_id, 0, len(report_pages))
    
    try:
        bot.send_message(
            message.chat.id,
            report_pages[0],
            parse_mode="HTML",
            reply_markup=markup
        )
    except telebot.apihelper.ApiTelegramException as e:
        # Fallback: send without HTML formatting
        logger.warning(f"HTML parse error: {e}")
        bot.send_message(
            message.chat.id,
            text=report_pages[0].replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", ""),
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: CallbackQuery):
    """Handle inline keyboard callbacks"""
    global cached_reports
    
    if call.data.startswith("/page "):
        # Parse callback data
        parts = call.data.split(" ")
        if len(parts) != 3:
            return
        
        query_id = parts[1]
        page_id = int(parts[2])
        
        # Check if report exists
        if query_id not in cached_reports:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⚠️ This search has expired. Please perform a new search."
            )
            return
        
        # Get report pages
        report_pages = cached_reports[query_id]
        
        # Handle page wrapping
        if page_id < 0:
            page_id = len(report_pages) - 1
        elif page_id >= len(report_pages):
            page_id = page_id % len(report_pages)
        
        # Create navigation
        markup = create_navigation_keyboard(query_id, page_id, len(report_pages))
        
        # Update message
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=report_pages[page_id],
                parse_mode="HTML",
                reply_markup=markup
            )
        except telebot.apihelper.ApiTelegramException as e:
            # Fallback: send without HTML formatting
            logger.warning(f"HTML parse error on navigation: {e}")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=report_pages[page_id].replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", ""),
                reply_markup=markup
            )
    
    elif call.data == "page_info":
        # Just answer the callback to remove loading state
        bot.answer_callback_query(call.id, "Page indicator")


def main():
    """Main function to run the bot"""
    logger.info("Starting Leakosint Telegram Bot...")
    logger.info(f"Bot configured with API token: {LEAKOSINT_API_TOKEN[:10]}...")
    
    # Start polling
    while True:
        try:
            logger.info("Bot is running and waiting for messages...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            logger.error(f"Bot polling error: {e}")
            import time
            time.sleep(5)


if __name__ == "__main__":
    main()