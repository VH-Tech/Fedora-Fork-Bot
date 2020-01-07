from telegram.ext import Updater , CommandHandler,MessageHandler, Filters
import logging
import json
import requests


r = requests.get('https://api.github.com/orgs/fedora-infra/repos').content.decode('UTF-8')

key = '' #Your API token goes here


updater = Updater(token=key, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def forks(update, context):
    words = update.message.text.split(' ')

    for j in json.loads(r):
        if j['name'] == words[1]:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Number of forks for " + words[1] + " are: " + str(j['forks']))
            return

    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a valid repository name")
    print(update.message.text)


def serve(update, context):
    if update.message.text.lower() == 'hi' or update.message.text.lower() == 'hello':
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry I don't understand that Please use /help for instructions on how to use me :)")
    print(update.message.text)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! \n Here's a list of commands you can use: \n /repos : Tell all the repositories in the organization\n /forks <repos_name> : returns number of forks for <repos_name> \n /help : to see list of available commands \nSo how may I help you ?")


def repos(update, context):
    repositories = []

    for j in json.loads(r):
        repositories.append(j['name'])

    context.bot.send_message(chat_id=update.effective_chat.id, text=str(repositories)[1:-1])


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', start)
dispatcher.add_handler(help_handler)

forks_handler = CommandHandler('forks', forks)
dispatcher.add_handler(forks_handler)

repos_handler = CommandHandler('repos', repos)
dispatcher.add_handler(repos_handler)

text_handler = MessageHandler(Filters.text, serve)
dispatcher.add_handler(text_handler)

updater.start_polling()
