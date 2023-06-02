import os
import PyPDF2
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# States for conversation handler
STATE_PURCHASE = 1
STATE_SALES = 2

def start(update, context):
    update.message.reply_text(
        "Hello! Please upload the purchase bill (PDF file)."
    )

    return STATE_PURCHASE

def process_purchase_bill(update, context):
    # Check if the uploaded file is a PDF
    if update.message.document.mime_type != 'application/pdf':
        update.message.reply_text("Please upload a PDF file.")
        return STATE_PURCHASE

    # Get the PDF file sent by the user
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    pdf_file = file.download()

    # Process the PDF file
    # Rest of the code...

    # Prompt the user to upload the sales bill
    update.message.reply_text("Purchase bill processed successfully! Please upload the sales bill (PDF file).")

    return STATE_SALES

def process_sales_bill(update, context):
    # Check if the uploaded file is a PDF
    if update.message.document.mime_type != 'application/pdf':
        update.message.reply_text("Please upload a PDF file.")
        return STATE_SALES

    # Get the PDF file sent by the user
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    pdf_file = file.download()

    # Process the PDF file
    # Rest of the code...

    # Prompt the user to upload the alternate bill
    update.message.reply_text("Sales bill processed successfully! Please upload any overhead expenses (PDF file).")

    return STATE_PURCHASE

def cancel(update, context):
    update.message.reply_text("Cancelled.")

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
            STATE_PURCHASE: [MessageHandler(Filters.document, process_purchase_bill)],
            STATE_SALES: [MessageHandler(Filters.document, process_sales_bill)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
