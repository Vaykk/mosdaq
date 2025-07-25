import telebot
from openai import OpenAI
bot = telebot.TeleBot("8207554168:AAFfrCZLcL9x2s6WRh7VcoZYHkkzFJ2Na9k")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

userPrompts = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"ку")

@bot.message_handler(commands=['prompt'])
def prompt(message):
    current = userPrompts.get(message.from_user.id, "Промпт не установлен")
    bot.send_message(message.chat.id, f"Текущий промпт: {current}\nВведите новый промпт или /cancel для отмены, /empty чтобы очистить промпт")
    bot.register_next_step_handler(message, newPrompt)

def newPrompt(message):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "Изменение промпта отменено")
    elif message.text == "/empty":
        del userPrompts[message.from_user.id]
        bot.send_message(message.chat.id, "Промпт очищен")
    else:
        userPrompts[message.from_user.id] = message.text
        bot.send_message(message.chat.id, f"Промпт успешно обновлен!\nНовый промпт: {message.text}")



@bot.message_handler(content_types='text')
def text(message):
    bot.send_message(message.chat.id, "Ожидайте")
    content=message.text

    currentPrompt = userPrompts.get(message.from_user.id, "")

    completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {"role": "system", "content": currentPrompt},
        {"role": "user", "content": content}
    ]
    )
    bot.send_message(message.chat.id, completion.choices[0].message.content)

bot.polling()
