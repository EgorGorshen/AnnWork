import matplotlib.pyplot as plt
import json
import os


type_of_q = {
    "ID": 0,
    "Время создания": 0,
    "Время изменения": 0,
    "Введите ваш номер": 0,
    "Я спокоен": 1,
    "Мне ничто не угрожает": 1,
    "Я нахожусь в напряжении": -1,
    "Я испытываю сожаление": -1,
    "Я чувствую себя свободно": 1,
    "Я растроен": -1,
    "Меня волнуют возможные неудачи": -1,
    "Я чувствую себя отдохнувшим": 1,
    "Я встревожен": -1,
    "Я испытываю чувство внутреннего удовлетворения": 1,
    "Я уверен в себе": 1,
    "Я нервничаю": -1,
    "Я не нахожу себе места": -1,
    "Я взвинчен": -1,
    "Я не чувствую скованности": 1,
    "Я доволен": 1,
    "Я озабочен": -1,
    "Я слишком возбужден и мне не по себе": -1,
    "Мне радостно": 1,
    "Мне приятно": 1
}


short = {
    "Я спокоен": "Спокоен",
    "Мне ничто не угрожает": "Не угрожает",
    "Я нахожусь в напряжении": "В напряжении",
    "Я испытываю сожаление": "Сожаление",
    "Я чувствую себя свободно": "Свободно",
    "Я растроен": "Растроен",
    "Меня волнуют возможные неудачи": "Волнуют\nвозможные\nнеудачи",
    "Я чувствую себя отдохнувшим": "Отдохнувший",
    "Я встревожен": "Встревожен",
    "Я испытываю чувство внутреннего удовлетворения": "Чувство\nвнутреннего\n удовлетворения",
    "Я уверен в себе": "Уверен в себе",
    "Я нервничаю": "Нервничаю",
    "Я не нахожу себе места": "Не нахожу\nсебе места",
    "Я взвинчен": "Взвинчен",
    "Я не чувствую скованности": "Не чувствую\nскованности",
    "Я доволен": "Доволен",
    "Я озабочен": "Озабочен",
    "Я слишком возбужден и мне не по себе": "Слишком\nвозбужден",
    "Мне радостно": "Радостно",
    "Мне приятно": "Приятно"

}

def reform_dict(d: dict):
    returner = dict()
    for i in d.items():
        returner[short[i[0]]] = round(i[1], 3)

    return returner


def load_photo():
    with open('db.json', 'r') as file:
        D = reform_dict(json.load(file))
        plt.figure(figsize=(12, 6), dpi=80)
        plt.bar(range(len(D)), D.values(), align='edge', width=0.3)
        plt.xticks(range(len(D)), list(D.keys()), rotation=90)
        plt.savefig('db.png', bbox_inches='tight')


def text():
    with open('db.json', 'r') as file:
        db: dict = json.load(file)
        returner = ''

        for i in db.items():
            returner += i[0] + ' ' + str(round(i[1], 3)) + '\n'

        return returner


def loading_db(message, bot, type_db):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = json.loads(bot.download_file(file_info.file_path))
    with open(f'db_{type_db}.json', 'w') as new_file:
        returner = []
        for i in downloaded_file:
            returner.append(dict(i))
        json.dump(returner, new_file, indent=4, ensure_ascii=False)


def get_pair(before: list[dict[str, str]], after: list[dict[str, str]]):
    for b in before:
        for a in after:
            if b['Введите ваш номер'] == a['Введите ваш номер']:
                before.remove(b)
                after.remove(a)
                return b, a, before, after


def analysis():
    returner_1 = []
    returner = {}

    with open('db_after.json', 'r') as file:
        after = json.load(file)
    
    with open('db_before.json', 'r') as file:
        before = json.load(file)
    
    count = min(len(before), len(after))

    while count != 0:
        pair = get_pair(before=before, after=after)
        if pair is None:
            return False
        b, a, before, after = pair
        returner_1.append((b, a))
        count -= 1

    for man in returner_1:
        for i in man[0].keys():
            if type_of_q[i] != 0:
                returner[i] = returner.get(i, []) + [int(man[1][i]) - int(man[0][i])]

    for i in returner.keys():
        returner[i] = sum(returner[i]) / len(returner[i])

    os.system('python3 analysis.py')

    with open('db.json', 'w') as file:
        json.dump(returner, file, ensure_ascii=False, indent=4)
        return True


def mean():
    returner = []
    with open('./db.json') as data:
        data = json.load(data)

        for i in data.keys():
            returner.append(data[i] * type_of_q[i])
    return sum(returner) / len(returner)


if __name__ == "__main__":
    load_photo()

