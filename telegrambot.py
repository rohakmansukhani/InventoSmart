import os
import PyPDF2
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from collections import defaultdict

# States for conversation handler
STATE1 = 1
STATE2 = 2

def start(update, context):
    reply_keyboard = [['Upload Purchase Bill'], ['Upload Sales Bill']]
    update.message.reply_text(
        "Hello! Please choose an option.",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return STATE1

def process_purchase_bill(update, context):
    # Get the PDF file sent by the user
    pdf_file = context.bot.get_file(update.message.document).download()

    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract text from each page of the PDF
        bill_text = ""
        for page in pdf_reader.pages:
            bill_text += page.extract_text()

        # Perform calculations based on the extracted text
        # Implement your logic to calculate profits and losses here

        # Example calculation: Count the occurrences of each product name
        product_count = defaultdict(int)
        for word in bill_text.split():
            # Assuming the product names are single words
            product_count[word] += 1

        # Example output: Print the product names and their occurrence count
        for product, count in product_count.items():
            update.message.reply_text(f"Product: {product}, Count: {count}")

    update.message.reply_text("Purchase bill processed successfully! Please upload the sales bill.")

    return STATE2

def process_sales_bill(update, context):
    # Get the PDF file sent by the user
    pdf_file = context.bot.get_file(update.message.document).download()

    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract text from each page of the PDF
        bill_text = ""
        for page in pdf_reader.pages:
            bill_text += page.extract_text()

        # Perform calculations based on the extracted text
        # Implement your logic to calculate profits and losses here

        # Example calculation: Count the occurrences of each product name
        product_count = defaultdict(int)
        for word in bill_text.split():
            # Assuming the product names are single words
            product_count[word] += 1

        # Example output: Print the product names and their occurrence count
        for product, count in product_count.items():
            update.message.reply_text(f"Product: {product}, Count: {count}")

    update.message.reply_text("Sales bill processed successfully! Please upload the alternate bill.")

    return STATE1

def cancel(update, context):
    update.message.reply_text("Cancelled.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def main():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: Please set the TELEGRAM_BOT_TOKEN environment variable.")
        return

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE1: [
                MessageHandler(Filters.regex('^Upload Purchase Bill$'), process_purchase_bill),
                MessageHandler(Filters.regex('^Upload Sales Bill$'), process_sales_bill)
            ],
            STATE2: [
                MessageHandler(Filters.document & ~Filters.regex('^Upload Purchase Bill$'), process_sales_bill)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
