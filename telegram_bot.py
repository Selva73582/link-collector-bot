# import requests
# from telegram import Update
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# # Define form URLs and field names
# forms = {
#     "general": {
#         "url": "https://docs.google.com/forms/d/e/1FAIpQLSdQum5fNUkNm-i3zs_yWBuBe-ODqJmYunaWrmMQAeaM9F_MsQ/formResponse",
#         "fields": {
#             "entry.2000707645": "username",  # Field for username
#             "entry.870981315": "link"        # Field for link
#         }
#     },
#     "quote": {
#         "url": "https://docs.google.com/forms/d/e/1FAIpQLSeWkjxMcNxlqtNiDBzwZh1XUP3IwH0n1DXppgihT50Mzqp3Qg/formResponse",
#         "fields": {
#             "entry.401212998": "username",
#             "entry.1647661367": "link"
#         }
#     },
# }

# def submit_form(url, fields,payload):
#     # Prepare payload with form entry identifiers
    
#     print("Submitting form with URL:", url)
#     print("Payload:", payload)
    
#     try:
#         response = requests.post(url, data=payload)
#         response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
#         print("Response Status Code:", response.status_code)
#         print("Response Text:", response.text[:1000])  # Print first 1000 characters for brevity
#     except requests.exceptions.RequestException as e:
#         print(f"Error submitting form: {e}")

# def handle_message(update: Update, context: CallbackContext):
#     text = update.message.text
#     user = update.message.from_user.username

#     # Determine which form to use based on message content
#     form_type = "general" if "general" in text else "quote"  # Adjust logic if needed
#     print("----&&&&&&&&&&#@$@#######"+text)
#     text=text.split('=')
#     text=text[1]

#     form_info = forms[form_type]
#     url = form_info["url"]
#     fields = {
#         "username": user,   # Username field
#         "link": text        
#     }
#     if form_type=="general":
#         payload = {
#         "entry.2000707645": fields["username"],
#         "entry.870981315": fields["link"]        
#     }
#     else:
#         payload = {
#         "entry.401212998": fields["username"],  # Username field
#         "entry.1647661367": fields["link"]        # Link field
#     }
#     # Submit the form
#     submit_form(url, fields,payload)
#     update.message.reply_text("Form submission attempted. Check logs for details.")

# def main():
#     # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
#     updater = Updater("7448679923:AAEkwnuTaj7RVXY3omPXKO1bIOGfYg00ZdY", use_context=True)
#     dp = updater.dispatcher

#     # Handle messages
#     dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

#     # Start the bot
#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()


import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime

# Global variables to store time frame
start_time = None
end_time = None

# Define form URLs and field names
forms = {
    "general": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSdQum5fNUkNm-i3zs_yWBuBe-ODqJmYunaWrmMQAeaM9F_MsQ/formResponse",
        "fields": {
            "entry.2000707645": "username",  # Field for username
            "entry.870981315": "link"        # Field for link
        }
    },
    "quote": {
        "url": "https://docs.google.com/forms/d/e/1FAIpQLSeWkjxMcNxlqtNiDBzwZh1XUP3IwH0n1DXppgihT50Mzqp3Qg/formResponse",
        "fields": {
            "entry.401212998": "username",
            "entry.1647661367": "link"
        }
    },
}

def submit_form(url, fields, payload):
    print("Submitting form with URL:", url)
    print("Payload:", payload)
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text[:1000])  # Print first 1000 characters for brevity
    except requests.exceptions.RequestException as e:
        print(f"Error submitting form: {e}")

def handle_message(update: Update, context: CallbackContext):
    global start_time, end_time
    
    # Check if the current time is within the set time frame
    current_time = datetime.now()
    if start_time and end_time and (start_time <= current_time <= end_time):
        text = update.message.text
        user = update.message.from_user.username

        # Determine which form to use based on message content
        form_type = "general" if "general" in text else "quote"
        print("Received message:", text)
        
        # Extract the actual link or content after '='
        try:
            text = text.split('=')[1]
        except IndexError:
            update.message.reply_text("Invalid message format. Please provide the link in the format 'key=value'.")
            return

        form_info = forms[form_type]
        url = form_info["url"]
        fields = {
            "username": user,
            "link": text        
        }

        if form_type == "general":
            payload = {
                "entry.2000707645": fields["username"],
                "entry.870981315": fields["link"]
            }
        else:
            payload = {
                "entry.401212998": fields["username"],
                "entry.1647661367": fields["link"]
            }

        # Submit the form
        submit_form(url, fields, payload)
        update.message.reply_text("Form submission attempted. Check logs for details.")
    else:
        update.message.reply_text("Outside of the allowed time frame. Form submission not allowed.")

def set_timeframe(update: Update, context: CallbackContext):
    global start_time, end_time
    
    # Command format: /set_timeframe start=YYYY-MM-DD:HH:MM end=YYYY-MM-DD:HH:MM
    try:
        args = context.args
        start_str = args[0].split('=')[1]
        end_str = args[1].split('=')[1]

        start_time = datetime.strptime(start_str, '%Y-%m-%d:%H:%M')
        end_time = datetime.strptime(end_str, '%Y-%m-%d:%H:%M')

        update.message.reply_text(f"Time frame set from {start_time} to {end_time}.")
    except (IndexError, ValueError) as e:
        update.message.reply_text("Invalid command format. Use /set_timeframe start=YYYY-MM-DD:HH:MM end=YYYY-MM-DD:HH:MM")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    updater = Updater("7448679923:AAEkwnuTaj7RVXY3omPXKO1bIOGfYg00ZdY", use_context=True)
    dp = updater.dispatcher

    # Handle messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Command to set the time frame
    dp.add_handler(CommandHandler("set_timeframe", set_timeframe))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
