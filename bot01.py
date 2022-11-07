# Создать игру с ботом в телеграм.
# Условие задачи: На столе лежит 2021 конфета. 
# Играют два игрока делая ход друг после друга. 
# Первый ход определяется жеребьёвкой. 
# За один ход можно забрать не более чем 28 конфет. 
# Все конфеты оппонента достаются сделавшему последний ход.


from random import randint
from telegram import Update
from telegram.ext import Updater, ContextTypes, CommandHandler, MessageHandler, Filters
import logging


logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename="bot_log.txt")
logger = logging.getLogger(__name__)
updater = Updater(token = "ВСТАВЬТЕ СЮДА СВОЙ ТОКЕН")

dispatcher = updater.dispatcher

def main_menu(update:Update,context:ContextTypes):
    context.bot.send_message(chat_id=update.effective_chat.id,text = f'''Приветствую, {update.effective_user.first_name}
    2021 Bloody candies on the cursed table
	The Game

    Правила игры: На столе лежит 2021 конфета 
	Игрок и компьютер ходят по очереди 
    Первый игрок определяется случайным образом 
	За один ход можно забрать до 28 конфет 
    Все конфеты оппонента достаются сделавшему последний ход.''')
    context.user_data['counter'] = 2021
    player_select = randint(1,2)
    if player_select == 1:
        turn_info_output(update,context,player_select)
    else:
        turn_info_output(update,context,player_select)
        bot_turn(update,context)


def turn_info_output(update:Update,context:ContextTypes,player_select):
    candies_quantity=context.user_data.get('counter')
    if player_select == 1:
        name = f'{update.effective_user.first_name}, сделайте Ваш ход'
    else:
        name = 'Ход компьютера'
    context.bot.send_message(chat_id=update.effective_chat.id,text=f'''{name} На столе осталось {candies_quantity} конфет.''')


def game_canceled(update:Update,context:ContextTypes):
    del context.user_data["counter"]
    update.message.reply_text("GAME OVER. Чтобы начать игру заново выберите команду \"Начать игру\"")

    context.user_data.clear()


def player_turn(update:Update,context:ContextTypes):
    candies_quantity = context.user_data.get('counter')
    if candies_quantity == 0 or candies_quantity == None:
        context.bot.send_message(chat_id=update.effective_chat.id,text="Для начала игры выберите команду \"Начать игру\"")
        return
    try:
        user_text=int(update.message.text)
        if 0 < user_text < 29:
            move = user_text
            context.bot.send_message(chat_id=update.effective_chat.id,text=f'Игрок забрал {move} конфет(ы). На столе осталось {candies_quantity-move} конфет(ы)')
        else:
            if candies_quantity < 29:
                message = f'Число конфет должно быть от 1 до {candies_quantity}'
            else:
                message = "Число может быть от 1 до 28"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            return
    except Exception:
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Введены не корректные данные")
    candies_quantity = candies_quantity - move
    if candies_quantity == 0:
        context.bot.send_message(chat_id = update.effective_chat.id, text='Congratulations! Вы выиграли! \nЧтобы начать игру заново выберите команду \"Начать игру\"')
        return
    context.user_data['counter'] = candies_quantity
    bot_turn(update,context)


def bot_turn(update:Update,context:ContextTypes):
    candies_quantity = context.user_data.get('counter')
    if candies_quantity > 28:
        move = randint(1,28)
        context.bot.send_message(chat_id = update.effective_chat.id,text = f'''Компьютер забирает {move} конфет(ы).''')
    else:
        move = candies_quantity
        context.bot.send_message(chat_id = update.effective_chat.id,text = f'''Компьютер забирает {move} конфет(ы).''')
    candies_quantity = candies_quantity - move
    if candies_quantity == 0:
        context.bot.send_message(chat_id = update.effective_chat.id, text='SHAME ON YOU! Компьютер выиграл! \nЧтобы начать игру заново выберите команду \"Начать игру\"')    
        del context.user_data['counter']
        context.user_data.clear()
        return
    context.user_data['counter']=candies_quantity
    turn_info_output(update,context,1)


start_game = CommandHandler("start", main_menu)
user_move = MessageHandler(Filters.text, player_turn)
game_over = CommandHandler("cancel", game_canceled)

dispatcher.add_handler(start_game)
dispatcher.add_handler(game_over)
dispatcher.add_handler(user_move)

updater.start_polling()

updater.idle()