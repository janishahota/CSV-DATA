import io
import pandas as pd
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Function to fetch CSV data from GitHub
def get_csv_data(csv_url):
    response = requests.get(csv_url)
    data = pd.read_csv(io.StringIO(response.text))
    return data

# Load data from the CSV file on GitHub
csv_url = "https://raw.githubusercontent.com/janishahota/CSV-DATA/main/in%20table%20form%20-%20in%20table%20form.csv"
df = get_csv_data(csv_url)

# Get unique subcauses
subcauses = df['subcause'].unique()

# Create a dictionary to store NGOs based on subcause
ngos_by_subcause = {subcause: df[df['subcause'] == subcause] for subcause in subcauses}

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    context.user_data[user_id] = {}

    # Display available subcauses
    subcause_buttons = [
        [
            InlineKeyboardButton(f"{subcause}", callback_data=f"subcause_{subcause}")
        ] for subcause in subcauses
    ]
    update.message.reply_text(
        "Hello! I am CommunityServiceBot here to help you find an active Banglore-based NGO to volunteer at, that fits your passion!"
        "\n What would you like the cause of the NGO to be?",
        reply_markup=InlineKeyboardMarkup(subcause_buttons),
    )

# Define the subcause handler
def subcause_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    chosen_subcause = query.data.split("_")[1]

    # Store chosen sub cause in user_data
    context.user_data[user_id]['subcause'] = chosen_subcause

    # Display NGOs under the chosen subcause
    ngos = ngos_by_subcause[chosen_subcause]['name'].tolist()
    ngo_buttons = [
        [
            InlineKeyboardButton(f"{ngo}", callback_data=f"ngo_{ngo}")
        ] for ngo in ngos
    ]
    query.edit_message_text(
        f"Choose an NGO under {chosen_subcause}:",
        reply_markup=InlineKeyboardMarkup(ngo_buttons),
    )

# Define the NGO handler
def ngo_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    chosen_ngo = query.data.split("_")[1]

    # Retrieve contact information for the chosen NGO
    contact_info = ngos_by_subcause[context.user_data[user_id]['subcause']][
        ngos_by_subcause[context.user_data[user_id]['subcause']]['name'] == chosen_ngo
    ]['Contact Information'].values[0]

    query.edit_message_text(
        f"Contact and Additional information for {chosen_ngo}:\n{contact_info}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]]),
    )

# Define the back handler
def back_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    # Display available subcauses
    subcause_buttons = [
        [
            InlineKeyboardButton(f"{subcause}", callback_data=f"subcause_{subcause}")
        ] for subcause in subcauses
    ]
    query.edit_message_text(
        "What would you like the cause of the NGO to be?",
        reply_markup=InlineKeyboardMarkup(subcause_buttons),
    )

# Define the main function
def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater("6715340979:AAGEKChsB8aAxUWkUVNORxrQnyjUxIKoBmU")

    dp = updater.dispatcher


    # Register handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(subcause_handler, pattern=r"^subcause_"))
    dp.add_handler(CallbackQueryHandler(ngo_handler, pattern=r"^ngo_"))
    dp.add_handler(CallbackQueryHandler(back_handler, pattern=r"^back$"))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == "__main__":
    main()