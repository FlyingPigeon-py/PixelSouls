from aiogram import Bot, Dispatcher, executor, types
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

from dbmanager import Manager
from exemple_generator import get_exemple

mp = ["тысячных", "десятитысячных", "стотысячных"]


class User:
    def __init__(self, id, name, difficult, current_exemple, current_answer):
        self.id = id
        self.name = name

    def get_difficult(self):
        difficult = db.get_user(self.id)[0][2]
        return difficult

    def get_current_exemple(self):
        current_exemple = db.get_user(self.id)[0][3]
        return current_exemple

    def get_current_answer(self):
        current_answer = db.get_user(self.id)[0][4]
        return current_answer

    def set_difficult(self, difficult):
        db.user_set_difficult(self.id, difficult)

    def set_current_exemple(self, exeple):
        db.user_set_exemple(self.id, exeple)

    def set_current_answer(self, answer):
        db.user_set_answer(self.id, answer)

    def send_exemple(self, exemple):
        db.user_set_exemple(self.id, exemple[0])
        db.user_set_answer(self.id, exemple[1])

    def refuse_exemple(self):
        db.user_set_exemple(self.id, None)
        db.user_set_answer(self.id, None)


class Server:
    def add_user(self, id, name):
        db.add_user(id, name)

    def isReg(self, id):
        users = db.get_users()
        for user in users:
            if user[0] == id:
                return True
        return False

    def get_user(self, id):
        return User(*db.get_user(id)[0])


async def create_example(user, message):
    rand = random.randint(1, 3)
    if rand == 1:
        e = list(map(str, get_exemple(user.get_difficult())))
        await message.answer(f"Ваша задача:\n\n{e[0]}\nОтветь округлите до {mp[user.get_difficult() - 1]}")
        user.send_exemple(e)
    elif rand == 2:
        id, ans = random.choice(db.get_image())
        photo = InputFile(f"image/{id}.png")
        await message.answer(f"Ваша задача:{' ' * 35}Beta\n\nОтветьте на вопрос с изображения")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        user.send_exemple(("img_" + str(id), ans))
    elif rand == 3:
        id, ans = random.choice(db.get_text())
        with open(f"text/{id}", encoding="UTF-8") as file:
            text = "\n".join(file.readlines())
        await message.answer(f"Ваша задача:{' ' * 35}Beta\n\n{text}")
        user.send_exemple(("txt_" + str(id), ans))


def main():
    global db, bot
    bot = Bot(token='1823627902:AAF06zrp3MV7_J0ubZ1NBbxcDzmT9Y4OBc8')
    server = Server()
    dp = Dispatcher(bot)
    db = Manager(r"DB/TelegramBotDB")

    @dp.message_handler()
    async def act(message: types.Message):

        if not server.isReg(message.from_user.id):
            server.add_user(message.from_user.id, message.from_user.username)

        user = server.get_user(message.from_user.id)

        if message.text.split()[0] == '/help':

            await message.answer(f"Ваша сложность:\t{user.name}\n\n"
                                 f"/exemple - Получить задание\n\n"
                                 f"/refuse - Отказаться от задания\n\n"
                                 f"/difficult (Уровень сложности) - выставить уровень сложности генерации примеров\n\n"
                                 f"/difficult_list - список сложностей")

        elif message.text.split()[0] == '/exemple':
            if user.get_current_exemple() == "None":
                await create_example(user, message)
            else:
                user.get_current_exemple()
                if str(user.get_current_exemple()).split("_")[0] != "img":
                    await message.answer(
                        f"Ваша задача:\n\n{user.get_current_exemple()}\nОтветь округлите до {mp[user.get_difficult() - 1]}")
                elif user.get_current_exemple().split("_")[0] == "img":
                    photo = InputFile(f"image/{user.get_current_exemple().split('_')[1]}.png")
                    await message.answer(f"Ваша задача:{' ' * 35}Beta\n\nОтветьте на вопрос с изображения")
                    await bot.send_photo(chat_id=message.chat.id, photo=photo)
                elif user.get_current_exemple().split("_")[0] == "txt":
                    with open(f"text/{user.get_current_exemple().split('_')[0]}", encoding="UTF-8") as file:
                        text = "\n".join(file.readlines())
                        await message.answer(f"Ваша задача:{' ' * 35}Beta\n\n{text}")
        elif message.text.split()[0] == '/refuse':
            if user.get_current_exemple() != "None":
                await message.answer(f"🔴 Вы отказались от задания\n\nВерный ответ был: {user.get_current_answer()}")
                user.refuse_exemple()
            else:
                await message.answer(f"У вас нет задания\n\nВы не можете от него отказаться")
        elif message.text.split()[0] == '/difficult':
            if user.get_current_exemple() == "None":
                if len(message.text.split()) == 2:
                    if message.text.split()[1] in ["1", "2", "3"]:
                        user.set_difficult(int(message.text.split()[1]))
                        await message.answer(f"Выставлен {message.text.split()[1]} уровень сложности")
                    else:
                        await message.answer(f"Некорректный уровень сложности")
                else:
                    await message.answer(
                        "/difficult {Уровень сложности}\n\nВозможные уровни сложности можно посмотеть здесь:\n/difficult_list")
            else:
                await message.answer(
                    f"Завершите текущее задание\n\nВыполните текущее задание или воспользуйтесь /refuse")
        elif message.text.split()[0] == '/difficult_list':
            text = """Сложности\n\n1| Лёгкий уровень (+, -, /, *)\n2| Сложный уровень (Степени)\n3| Нереальный уровень (Корни)
            """
            await message.answer(text)
        else:
            if user.get_current_exemple() != "None":
                if str(user.get_current_answer()).replace(",", ".") == message.text:
                    await message.answer(f"🟢 Задание выполнено!\n\nОтвет верный")
                    user.refuse_exemple()
                else:
                    await message.answer(f"🔻 Неверный ответ")

    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
