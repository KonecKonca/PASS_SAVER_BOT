from time import sleep

import telebot
from telebot import types

bot = telebot.TeleBot("1487973700:AAFpwcL_ozPUK6bK6EglwWkqGTz4fsXTbaA")

# Имена кнопок
# Главное меню
PASSWORD_MENU = "password_menu"
GROUP_MENU = "group_menu"
# Вернуться в главное меню
MAIN_MENU = "main_menu"
# пароли
ADD_PASSWORD = "add_password"
REMOVE_PASSWORD = "remove_password"
MOVE_PASSWORD = "move_password"
# категории
SHOW_CATEGORY = "show_category"
ADD_CATEGORY = "add_category"
REMOVE_CATEGORY = "remove_category"

passwords = {
    "шлак": [
        ("1111", "2222", "3333", ["#вк", "#инста"])
    ],
    "coц_сети": [
        ("мой акк в вк", "akozit", "12345", ["#контач", "#вк"]),
        ("мой акк в инсте", "koneckonca", "Lnmx", ["#инст"])
    ],
    "другое": [
        ("мой акк в алике", "Alilysik", "Lnmx123", ["#инст"]),
        ("мой акк в алике", "akaz", "1234", ["#алик"]),
        ("мой акк в куфаре", "andrei", "123", [])
    ]
}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == GROUP_MENU:
        show_keyboard(call.message.chat.id, keyboard=group_keyboard())
    elif call.data == PASSWORD_MENU:
        show_keyboard(call.message.chat.id, keyboard=password_keyboard())
    elif call.data == SHOW_CATEGORY:
        show_category(call.message)
    elif call.data == ADD_CATEGORY:
        add_category(call.message)
    elif call.data == ADD_PASSWORD:
        add_password(call.message)
    elif call.data == MOVE_PASSWORD:
        move_password(call.message)
    elif call.data == REMOVE_PASSWORD:
        remove_password(call.message)
    elif call.data == MAIN_MENU:
        show_keyboard(call.message.chat.id)
    elif call.data == REMOVE_CATEGORY:
        remove_category(call.message)
    # ответ пользователя кнопкой
    elif call.data.endswith("~show_cat"):
        show_passwords(call.message, call.data.replace("~show_cat", ""))
    elif call.data.endswith("~del_cat"):
        remove_category_after_user_input(call.message, call.data.replace("~del_cat", ""))


@bot.message_handler(commands=['start', 's'])
# @bot.message_handler(regexp=".*[^-gr]$")
# @bot.message_handler(regexp="^(.*-gr)|(.*-ppp)")
def start(message):
    show_keyboard(message.chat.id)


# Обработка текстовых сообщений, которые ввёл пользователь
@bot.message_handler(regexp=".*-mv")
def move_password_after_user_input(message):
    try:
        input_data = message.text.replace("-mv", "").split("--")
        old_category = input_data[0].strip()
        password_number = input_data[1].strip()
        new_category = input_data[2].strip()
        password = passwords[old_category].pop(int(password_number) - 1)
        if new_category in passwords:
            passwords[new_category].append(password)
        else:
            passwords[new_category] = [password]
    except :
        bot.send_message(message.chat.id, "😡😡😡 поробуйте ещё раз")
    show_keyboard(message.chat.id)


@bot.message_handler(regexp=".*-gr")
def add_category_after_user_input(message):
    try:
        passwords[message.text.replace("-gr", "").strip()] = []
    except :
        bot.send_message(message.chat.id, "😡😡😡 поробуйте ещё раз")
    show_keyboard(message.chat.id)


@bot.message_handler(regexp=".*-rm")
def add_category_after_user_input(message):
    try:
        input = message.text.replace("-rm", "").split("--")
        category = input[0]
        password_position = int(input[1]) - 1
        del passwords[category][password_position]
    except :
        bot.send_message(message.chat.id, "😡😡😡 поробуйте ещё раз")
    show_keyboard(message.chat.id)


@bot.message_handler(regexp=".*-ps")
def add_password_after_user_input(message):
    try:
        input_data = message.text.replace("-ps", "").split("--")
        category = input_data[0].strip()
        description = input_data[1].strip()
        login = input_data[2].strip()
        password = input_data[3].strip()
        hash_tags = [tag.strip for tag in input_data[4:]] if len(input_data) > 5 else []
        if category in passwords:
            passwords[category].append((description, login, password, hash_tags))
        else:
            passwords[category] = [(description, login, password, hash_tags)]
    except :
        bot.send_message(message.chat.id, "😡😡😡 поробуйте ещё раз")
    show_keyboard(message.chat.id)


def remove_category_after_user_input(message, to_remove_category):
    del passwords[to_remove_category]
    show_keyboard(message.chat.id)


def remove_category(message):
    categories_to_remove = [
        types.InlineKeyboardButton(
            text="❌ " + category + (" -> !не пустая!" if len(passwords[category]) >= 1 else ""),
            callback_data=category + "~del_cat")
        for category in passwords.keys()
    ]
    categories_to_remove.append(types.InlineKeyboardButton(text='🔙🔙🔙       В главное меню', callback_data=MAIN_MENU))
    show_keyboard(
        message.chat.id,
        create_keyboard(categories_to_remove)
    )


def remove_password(message):
    show_existing_passwords(message)
    bot.send_message(message.chat.id, "Напишите:\nкатегория--номер пароля-rm\n")


def show_existing_passwords(message):
    output = "=" * 20 + "\n"
    group_counter = 1
    for category, passwords_for_category in passwords.items():
        password_counter = 1
        output += "%s. %s:\n" % (group_counter, category)
        for password in passwords_for_category:
            output += "      %s. %s\n" % (password_counter, password[0])
            password_counter += 1
        group_counter += 1
    output += "=" * 20 + "\n"
    bot.send_message(message.chat.id, output)


def show_existing_categories(message):
    result_message = "Категории: \n"
    counter = 1
    for category in passwords.keys():
        result_message += "      %s. %s\n" % (counter, category)
        counter += 1
    bot.send_message(message.chat.id,  result_message)


def move_password(message):
    show_existing_categories(message)
    bot.send_message(message.chat.id, "Напишите:\nстарая категория--номер пароля--новая категория-mv\n")


def add_password(message):
    show_existing_categories(message)
    bot.send_message(message.chat.id, "Напишите:\nкатегория--описание--логин--пароль--#тег1--#тег2-ps\n")


def add_category(message):
    bot.send_message(message.chat.id, "Напишите:\nназвание категории-gr\n")


def show_category(message):
    keyboard = types.InlineKeyboardMarkup()
    for category in passwords.keys():
        keyboard.add(types.InlineKeyboardButton(text=category, callback_data=category + "~show_cat"))
    bot.send_message(message.chat.id, "Выбирай", reply_markup=keyboard)


def show_passwords(message, category):
    output = "Пароли в категории: %s" % category + "\n"
    output += "=" * 20 + "\n"
    counter = 1
    for password in passwords[category]:
        output += "%s. %s\n     логин: %s \n     пароль: %s \n" % (counter, password[0], password[1], password[2])
        output += "хештеги: " + ", ".join(password[3])
        output += "\n"
        counter += 1
    output += "=" * 20 + "\n"
    show_keyboard(message.chat.id, root_keyboard(), output)


# Клавиатуры для ввода
def root_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(text='⭐⭐⭐       Управление категориями', callback_data=GROUP_MENU))
    keyboard.add(types.InlineKeyboardButton(text='🔑🔑🔑       Управление паролями', callback_data=PASSWORD_MENU))
    keyboard.add(types.InlineKeyboardButton(text='🔍🔍🔍       Показать пароли', callback_data=SHOW_CATEGORY))

    return keyboard


def password_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(text='❌❌❌       Удалить пароль', callback_data=REMOVE_PASSWORD))
    keyboard.add(types.InlineKeyboardButton(text='✨✨✨       Переместить пароль', callback_data=MOVE_PASSWORD))
    keyboard.add(types.InlineKeyboardButton(text='✅✅✅       Добавить пароль', callback_data=ADD_PASSWORD))
    keyboard.add(types.InlineKeyboardButton(text='🔙🔙🔙       В главное меню', callback_data=MAIN_MENU))

    return keyboard


def group_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(types.InlineKeyboardButton(text='✅✅✅      Добавить категорию', callback_data=ADD_CATEGORY))
    keyboard.add(types.InlineKeyboardButton(text='❌❌❌       Удалить категорию', callback_data=REMOVE_CATEGORY))
    keyboard.add(types.InlineKeyboardButton(text='🔙🔙🔙       В главное меню', callback_data=MAIN_MENU))

    return keyboard


def create_keyboard(buttons):
    keyboard = types.InlineKeyboardMarkup()
    [keyboard.add(button) for button in buttons]
    return keyboard


def show_keyboard(chat_id, keyboard=root_keyboard(), message="🔑🔑🔑🔑🔑🔑🔑🔑🔑"):
    bot.send_message(chat_id, message, reply_markup=keyboard)


while True:
    try:
        bot.polling(none_stop=True)
        break
    except Exception as e:
        sleep(10)
        continue

