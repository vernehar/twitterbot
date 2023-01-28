from telegram.ext import Updater
from telegram.update import Update
import os

sponsorMessages = []

#api key to tg
updater = Updater(token=os.environ['TELEGRAM_CRED'], use_context=True)
job_queue = updater.job_queue

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ready to take sponsor message")



def append(update, context):
    print(update.message.text.split(" ",1)[1])
    sponsorMessages.append(update.message.text.split(" ",1)[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sponsor message updated")


#handles commands such as /start, /update
from telegram.ext import CommandHandler, MessageHandler, Filters, PrefixHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
append_handler = PrefixHandler("/","add", append)
dispatcher.add_handler(append_handler)

def getSponsorMessage():
    if sponsorMessages != []:
        return sponsorMessages[len(sponsorMessages)-1]
    else:
        return ""

updater.start_polling()


