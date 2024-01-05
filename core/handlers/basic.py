from RDB import RDB
from aiogram import Bot
from aiogram.types import Message
from collections import Counter
import operator
from aiogram.utils.keyboard import InlineKeyboardBuilder


GOORANDA = "6001130506:AAFNMXUh-iE3zdSq7PK2cpWWg4JFg_swwwg"
JARVIS = "6357305111:AAHzb68csA1ojiDn620m7FFvDXcTP9tYu_s"

CURRENT_BOT = JARVIS


async def add_preffix(bs_name):
    preffix = (4-len(bs_name))*"0"
    bs_name = "CR" + preffix + bs_name
    if not bs_name in RDB:
        bs_name = bs_name.replace("CR", "SE")
    return bs_name

async def get_yandex_button(bs_name,RDB):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=f"{bs_name} в Yandex",url=RDB[bs_name]["yandex_map"])
    return keyboard_builder.as_markup()




async def find_responcible(RDB,bs_name):
    responcible = ""
    Djankoysky = ["джанкойский", "джанкой","первомайский","первомайское", "красноперекопский", "армянcкий", "нижнегорский"]
    Yevpatoriysky = ["евпатория,","евпатория","сакский","саки","черноморский","раздольненский"]
    Simferopolsky = ["симферополь","симферопольский","красногвардейский","белогорский","бахчисарайский", "ялта", "ялтинский","алушта"]
    Feodosiysky = ["феодосия","судак","ленинский","керчь","кировский","советский"]
    address = RDB[bs_name]["address"]

    for part in address.replace("."," ").replace(","," ").replace("-"," ").split():
        # print(bs_name[:2])
        if bs_name[:2] == "SE":
            responcible = "Гречишников Анатолий"
            break
        elif part.lower() in Djankoysky:
            responcible = "Пономаренко Алексей"
            break
        elif part.lower() in Yevpatoriysky:
            responcible = "Пономаренко Алексей"
            break
        elif part.lower() in Simferopolsky:
            responcible = "Буханов Дмитрий"
            break
        elif part.lower() in Feodosiysky:
            responcible = "Грачёв Алексей"
            break

    return responcible

async def make_output_sheet(message,bs_name,RDB):
    await message.answer(f"------ {bs_name} ------\n"
                          f"КТК формат:  {RDB[bs_name]['arc_id']}\n"
                          f"Адрес: {RDB[bs_name]['address']}\n"
                          f"Координаты: {RDB[bs_name]['coordinates']}\n"
                          f"Арендодатель: {RDB[bs_name]['rent']}\n"
                          f"Конструктивный тип сайта: {RDB[bs_name]['constructional_type']}\n"
                          f"Ответственный: {await find_responcible(RDB,bs_name)}\n",
                         reply_markup=await get_yandex_button(bs_name,RDB)
                         )


async def find_arc(message: Message):
    global bs_name
    if (message.text[:3]).upper() == "ARC":
        for bs_name in RDB:
            ktk_bs_name = message.text.upper()
            ktk_cell = RDB[bs_name]["arc_id"]
            if ktk_cell != None:
                if ktk_bs_name[3:] in ktk_cell:
                    await make_output_sheet(message, bs_name, RDB)

async def search_by_address(message: Message):
    bs_name = message.text.upper()
    if len(bs_name.split()) > 1:
        keywords = []
        for keyword in bs_name.split():
            bs_string = ""
            for bs in RDB:
                if keyword in RDB[bs]["address"].upper():
                    keywords.append(bs)
        counter =Counter(keywords)
        counter = dict(counter)
        result = {element: count for element, count in counter.items() if count > 1}
        result_list = list(result)
        for bs in result_list:
            bs_string = f" {bs}\n{RDB[bs]['address']}\n\n" + bs_string
        if len(bs_string) > 4095:
            for x in range(0, len(bs_string), 4095):
                await message.answer(bs_string[x:x + 4095])
        else:
            await message.answer(bs_string)
    else:
        bs_string = ""
        for bs in RDB:
            if bs_name in RDB[bs]["address"].upper():
                bs_string = f" {bs}\n{RDB[bs]['address']}\n\n" + bs_string

        if len(bs_string) > 4095:
            for x in range(0, len(bs_string), 4095):
                await message.answer(bs_string[x:x + 4095])
        else:
            await message.answer(bs_string)


async def find_bs_info(message: Message):
    if len(message.text.split()) > 1:
        bs_name = message.text.upper()
        for bs in bs_name.split():
            bs_name = bs
            if bs_name in RDB:
                await make_output_sheet(message, bs_name, RDB)
            else:
                try:
                    bs_name = await add_preffix(bs_name)
                    await make_output_sheet(message, bs_name, RDB)
                except Exception as ex:
                    await message.answer(f"{bs} - такой БС нет.Сконцентрируйся и попробуй еще раз..")
    elif len(message.text.split()) == 1:
        bs_name = message.text.upper()
        if bs_name in RDB:
            await make_output_sheet(message, bs_name, RDB)
        else:
            try:
                bs_name = await add_preffix(bs_name)
                await make_output_sheet(message, bs_name, RDB)
            except Exception as ex:
                await message.answer(f"{bs_name[3:]} -такой БС нет. Сконцентрируйся и попробуй еще раз..")
