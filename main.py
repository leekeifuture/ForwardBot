import telebot

import config

bot = telebot.TeleBot(config.token)


# get all ids from trusted_ids file as array of digits
def get_trusted_ids():
    trusted_ids = []
    with open(config.file_name, 'r') as file:
        for line in file:
            trusted_ids.append(int(line))

    return trusted_ids


@bot.message_handler(func=lambda msg: msg.chat.id in get_trusted_ids() and
                                      msg.chat.id != config.my_id,
                     content_types=config.forwarding_messages_types)
def forward_message_handler(message):
    print(config.my_id, message.chat.id, message.message_id)
    bot.forward_message(config.my_id, message.chat.id, message.message_id)


# usage example: /add 365801236
@bot.message_handler(func=lambda msg: msg.chat.id == config.my_id,
                     commands=['add'])
def add_new_trusted_id_handler(message):
    id = message.text.split()[1]

    with open(config.file_name, 'a') as file:
        file.write(id + '\n')

    bot.send_message(message.chat.id, 'Added ' + id)


# usage example: /remove 365801236
@bot.message_handler(func=lambda msg: msg.chat.id == config.my_id,
                     commands=['remove'])
def add_new_trusted_id_handler(message):
    id = message.text.split()[1]

    with open(config.file_name, 'r') as f:
        lines = f.readlines()
    with open(config.file_name, 'w') as f:
        for line in lines:
            if line.strip('\n') != id:
                f.write(line)

    bot.send_message(message.chat.id, 'Removed ' + id)


bot.polling()
