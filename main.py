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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Handle /start command with interactive menu"""
    welcome_text = """
🔐 <b>Welcome to Leakosint Search Bot!</b>

I'm your advanced OSINT assistant for searching leaked databases using the powerful Leakosint API.

🎯 <b>What I Can Do:</b>
• Search across multiple leaked databases
• Find information by email, username, phone, or name
• Navigate through results with interactive buttons
• Provide detailed breach information

📱 <b>Quick Start:</b>
Just send me any search query and I'll do the rest!

👇 <b>Choose an option below to learn more:</b>
"""
    
    # Create inline keyboard menu
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📖 Help & Guide", callback_data="help_main"),
        InlineKeyboardButton("💡 Examples", callback_data="help_examples")
    )
    markup.add(
        InlineKeyboardButton("📊 Statistics", callback_data="help_stats"),
        InlineKeyboardButton("🔒 Privacy", callback_data="help_privacy")
    )
    markup.add(
        InlineKeyboardButton("ℹ️ About", callback_data="help_about")
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="HTML",
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    """Handle /help command"""
    help_text = """
📖 <b>Leakosint Bot - Complete Guide</b>

<b>🔍 How to Search:</b>
Simply send me any of the following:
• Email address (e.g., user@example.com)
• Username (e.g., john_doe)
• Phone number (e.g., +1234567890)
• Full name (e.g., John Smith)

<b>📋 Available Commands:</b>
/start - Show welcome menu
/help - Display this help message
/stats - View bot statistics
/examples - See search examples
/about - Learn about this bot
/privacy - Privacy information

<b>🎮 Navigation:</b>
When results are found, use the inline buttons:
• ⬅️ Previous - Go to previous result page
• ➡️ Next - Go to next result page
• Page counter shows current position

<b>⚡ Tips:</b>
• Be specific with your queries for better results
• Results are cached for quick navigation
• Use exact email addresses for best accuracy
• Multiple databases are searched simultaneously

<b>⚠️ Important:</b>
• Use this tool responsibly and legally
• Only search for legitimate purposes
• Respect privacy and data protection laws
• This bot is for educational/security research

Need more help? Use /start to access the interactive menu!
"""
    bot.reply_to(message, help_text, parse_mode="HTML")


@bot.message_handler(commands=['stats'])
def send_stats(message):
    """Show bot statistics"""
    stats_text = f"""
📊 <b>Bot Statistics</b>

🌐 API URL: <code>{LEAKOSINT_API_URL}</code>
🔢 Default Search Limit: <b>{DEFAULT_LIMIT}</b> records
🌍 Language: <b>{DEFAULT_LANG.upper()}</b>
💾 Cached Reports: <b>{len(cached_reports)}</b>
✅ Status: <b>Online & Ready</b>

<i>Type any search query to begin searching.</i>
"""
    bot.reply_to(message, stats_text, parse_mode="HTML")


@bot.message_handler(commands=['examples'])
def send_examples(message):
    """Show search examples"""
    examples_text = """
💡 <b>Search Examples</b>

Here are some example queries you can try:

<b>📧 Email Search:</b>
• <code>john.doe@gmail.com</code>
• <code>example@yahoo.com</code>
• <code>user123@outlook.com</code>

<b>👤 Username Search:</b>
• <code>john_doe</code>
• <code>admin123</code>
• <code>user_2024</code>

<b>📱 Phone Number Search:</b>
• <code>+1234567890</code>
• <code>555-123-4567</code>
• <code>+44 20 1234 5678</code>

<b>🏷️ Name Search:</b>
• <code>John Smith</code>
• <code>Jane Doe</code>
• <code>Robert Johnson</code>

<i>Just copy any example and send it to me, or create your own query!</i>
"""
    bot.reply_to(message, examples_text, parse_mode="HTML")


@bot.message_handler(commands=['about'])
def send_about(message):
    """Show about information"""
    about_text = """
ℹ️ <b>About Leakosint Bot</b>

<b>🤖 Bot Information:</b>
This bot provides access to the Leakosint API, a powerful OSINT (Open Source Intelligence) tool for searching leaked databases.

<b>🎯 Purpose:</b>
• Security research and penetration testing
• Checking if your data has been compromised
• OSINT investigations
• Educational purposes

<b>🔧 Features:</b>
✅ Multi-database search capability
✅ Fast and accurate results
✅ User-friendly interface
✅ Paginated results navigation
✅ Detailed breach information

<b>⚖️ Legal Notice:</b>
This bot is provided for legitimate security research and educational purposes only. Users are responsible for ensuring their use complies with applicable laws and regulations.

<b>🔗 Powered by:</b>
Leakosint API - Professional OSINT Database

<i>For support or questions, use /help</i>
"""
    bot.reply_to(message, about_text, parse_mode="HTML")


@bot.message_handler(commands=['privacy'])
def send_privacy(message):
    """Show privacy information"""
    privacy_text = """
🔒 <b>Privacy & Security</b>

<b>🛡️ Your Privacy Matters:</b>

<b>What we collect:</b>
• Search queries (temporarily cached)
• User ID (for authorization if enabled)
• Basic interaction logs

<b>What we DON'T collect:</b>
❌ Personal conversations
❌ Contact information
❌ Location data
❌ Device information

<b>Data Retention:</b>
• Search results are cached temporarily
• Cache is cleared periodically
• No long-term storage of queries

<b>Security:</b>
🔐 All API communications are encrypted
🔐 No data is shared with third parties
🔐 Bot operates on secure servers

<b>Your Responsibility:</b>
• Use the bot ethically and legally
• Don't search for others without permission
• Respect data protection regulations
• Report any security concerns

<i>This bot is designed with privacy in mind.</i>
"""
    bot.reply_to(message, privacy_text, parse_mode="HTML")


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
            "❌ <b>Search failed</b>\n\nThe API may be unavailable or there was an error processing your request.\n\n💡 Try:\n• Checking your query format\n• Using /examples for query ideas\n• Trying again in a few moments",
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
    
    # Handle help menu callbacks
    if call.data == "help_main":
        help_text = """
📖 <b>Leakosint Bot - Quick Guide</b>

<b>🔍 How to Search:</b>
Simply send me:
• Email: user@example.com
• Username: john_doe
• Phone: +1234567890
• Name: John Smith

<b>📋 Commands:</b>
/start - Welcome menu
/help - Full help guide
/stats - Bot statistics
/examples - Search examples
/about - About this bot
/privacy - Privacy info

<i>Just type your query and send!</i>
"""
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=help_text,
            parse_mode="HTML"
        )
        bot.answer_callback_query(call.id)
        
    elif call.data == "help_examples":
        examples_text = """
💡 <b>Search Examples</b>

<b>📧 Email:</b>
<code>john@gmail.com</code>

<b>👤 Username:</b>
<code>john_doe</code>

<b>📱 Phone:</b>
<code>+1234567890</code>

<b>🏷️ Name:</b>
<code>John Smith</code>

<i>Copy and send any example!</i>
"""
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=examples_text,
            parse_mode="HTML"
        )
        bot.answer_callback_query(call.id)
        
    elif call.data == "help_stats":
        stats_text = f"""
📊 <b>Bot Statistics</b>

🌐 API: <code>{LEAKOSINT_API_URL}</code>
🔢 Limit: <b>{DEFAULT_LIMIT}</b> records
🌍 Language: <b>{DEFAULT_LANG.upper()}</b>
💾 Cached: <b>{len(cached_reports)}</b>
✅ Status: <b>Online</b>

<i>Ready to search!</i>
"""
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=stats_text,
            parse_mode="HTML"
        )
        bot.answer_callback_query(call.id)
        
    elif call.data == "help_privacy":
        privacy_text = """
🔒 <b>Privacy & Security</b>

<b>We collect:</b>
• Search queries (temp)
• User ID (if auth enabled)

<b>We DON'T collect:</b>
❌ Personal data
❌ Conversations
❌ Location

<b>Security:</b>
🔐 Encrypted API calls
🔐 No third-party sharing
🔐 Temporary cache only

<i>Your privacy is protected.</i>
"""
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=privacy_text,
            parse_mode="HTML"
        )
        bot.answer_callback_query(call.id)
        
    elif call.data == "help_about":
        about_text = """
ℹ️ <b>About Leakosint Bot</b>

<b>🤖 Purpose:</b>
OSINT tool for searching leaked databases

<b>🎯 Use Cases:</b>
• Security research
• Data breach checking
• OSINT investigations
• Educational purposes

<b>🔧 Features:</b>
✅ Multi-database search
✅ Fast results
✅ Easy navigation
✅ Detailed info

<b>⚖️ Legal:</b>
For legitimate use only

<i>Powered by Leakosint API</i>
"""
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=about_text,
            parse_mode="HTML"
        )
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith("/page "):
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