import logging
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


# Прошу простите, как получить почту авторизованного пользователя я не разобрался
mail = 'SlavaKushch@yandex.ru'
sender = "slava.kush39@gmail.com"
password = "iqpk evew sdkm zxml"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)

@app.route('/post', methods=['POST'])
def main():

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    if request.json['session']['new']:
        response['response'][
            'text'] = 'Напишите текст напоминания, которое будет отправлено на почту'
    else:
        msg = MIMEText(request.json['request']['original_utterance'])
        msg["Subject"] = "Заметка от Алисы"
        server.sendmail(sender, mail, msg.as_string())
        response['response'][
            'text'] = 'Сообщение будет отправлено на почту'
        response['response']['end_session'] = True
    return jsonify(response)




if __name__ == '__main__':
    app.run(port=4324)
