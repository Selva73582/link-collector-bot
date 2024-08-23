import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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

def submit_form(url, fields,payload):
    # Prepare payload with form entry identifiers
    
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
    text = update.message.text
    user = update.message.from_user.username

    # Determine which form to use based on message content
    form_type = "general" if "general" in text else "quote"  # Adjust logic if needed
    print("----&&&&&&&&&&#@$@#######"+text)
    text=text.split('=')
    text=text[1]

    form_info = forms[form_type]
    url = form_info["url"]
    fields = {
        "username": user,   # Username field
        "link": text        # Link field
    }
    if form_type=="general":
        payload = {
        "entry.2000707645": fields["username"],  # Username field
        "entry.870981315": fields["link"]        # Link field
    }
    else:
        payload = {
        "entry.401212998": fields["username"],  # Username field
        "entry.1647661367": fields["link"]        # Link field
    }
    # Submit the form
    submit_form(url, fields,payload)
    update.message.reply_text("Form submission attempted. Check logs for details.")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    updater = Updater("7448679923:AAEkwnuTaj7RVXY3omPXKO1bIOGfYg00ZdY", use_context=True)
    dp = updater.dispatcher

    # Handle messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
