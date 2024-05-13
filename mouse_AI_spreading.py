# импортируем библиотеки
import logging

from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
pred_qwetion = ''
# Ссыдки нет пока, жду пока мой дружочек css допишет)
link = 'Тык'


@app.route('/post', methods=['POST'])
def main():
    global pred_qwetion
    if pred_qwetion:
        logging.info(pred_qwetion)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    return jsonify(response)


def handle_dialog(req, res):
    global pred_qwetion, link
    user_id = req['session']['user_id']

    consents = ['да', 'есть', 'конечно']
    # Знаю что слова 'нету' нет =)
    negations = ['нет', 'нету']
    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': ["Нет", "Нет для Mouse AI", "Да", ]
        }
        res['response'][
            'text'] = 'Mouse AI сделает вашу жизнь проще\nНо для начала ответьте на вопрос:\nУ вас есть деньги?'
        res['response']['buttons'] = get_suggests(user_id)
        pred_qwetion = 'У вас есть деньги?'
        return
    else:
        sessionStorage[user_id] = {
            'suggests': ["Нет", "Да"]
        }
        res['response']['buttons'] = get_suggests(user_id)
    # Первая ступень (У вас есть деньги?)
    if pred_qwetion == 'У вас есть деньги?' and req['request']['original_utterance'].lower() == "нет для Mouse ai":
        res['response']['text'] = f'Жмот\nMouse AI можно найти по ссылке:\n{link}'
        res['response']['end_session'] = True
        return
    if pred_qwetion == 'У вас есть деньги?' and req['request']['original_utterance'].lower() in consents:
        res['response']['text'] = f'Mouse AI можно найти по ссылке:\n{link}'
        res['response']['end_session'] = True
        return
    if pred_qwetion == 'У вас есть деньги?' and req['request']['original_utterance'].lower() in negations:
        res['response']['text'] = 'У вас есть работа?'
        pred_qwetion = 'У вас есть работа?'
        return

    # Вторая ступень (У вас есть работа?)
    if pred_qwetion == 'У вас есть работа?' and req['request']['original_utterance'].lower() in consents:
        res['response']['text'] = 'Они вам платят?'
        pred_qwetion = 'Они вам платят?'
        return
    if pred_qwetion == 'У вас есть работа?' and req['request']['original_utterance'].lower() in negations:
        res['response']['text'] = 'У вас есть имущество?'
        pred_qwetion = 'У вас есть имущество?'
        return

    # Третья ступень (Они вам платят?)
    if pred_qwetion == 'Они вам платят?' and req['request']['original_utterance'].lower() in ['да', 'конечно']:
        res['response']['text'] = f'Купите Mouse AI\n Найти можно найти по ссылке:\n{link}'
        res['response']['end_session'] = True
        return
    if pred_qwetion == 'Они вам платят?' and req['request']['original_utterance'].lower() in negations:
        res['response']['text'] = 'У вас есть имущество?'
        pred_qwetion = 'У вас есть имущество?'
        return
    # Третья ступень (У вас есть имущество?)
    if pred_qwetion == 'У вас есть имущество?' and req['request']['original_utterance'].lower() in consents:
        res['response']['text'] = f'Продайте\nИ купите Mouse AI\nНайти можно найти по ссылке:\n{link}'
        res['response']['end_session'] = True
        return
    if pred_qwetion == 'У вас есть имущество?' and req['request']['original_utterance'].lower() in negations:
        res['response']['text'] = 'У вас есть душа?'
        pred_qwetion = 'У вас есть душа?'
        return
    # Четвёртая ступень (У вас есть душа?)
    if 'У вас есть душа?' in pred_qwetion and req['request']['original_utterance'].lower() in consents:
        res['response']['text'] = f'Продайте\nИ купите Mouse AI\nНайти можно найти по ссылке:\n{link}'
        res['response']['end_session'] = True
        return
    if 'У вас есть душа?' in pred_qwetion and req['request']['original_utterance'].lower() in negations:
        res['response']['text'] = 'Ложь\nУ вас есть душа?'
        pred_qwetion = 'У вас есть душа?'
        return

    res['response']['text'] = \
        f"Что-что?\n{pred_qwetion}"


def get_suggests(user_id):
    global pred_qwetion
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    session['suggests'] = session['suggests']
    sessionStorage[user_id] = session
    return suggests


if __name__ == '__main__':
    app.run(port=2020)
