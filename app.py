from flask import Flask, request
import sett
import services

app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return 'Hola mundo Tecker, desde TempTech'

@app.route('/webhook', methods=['GET'])
def verificarToken():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge:
            return challenge, 200
        else: 
            return 'Token incorrecto, acceso no autorizado', 403
    except Exception as e:
        return str(e), 403
    
@app.route('/webhook', methods=['POST'])
def recibirMensaje():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtenerMensajeWhatsApp(message)

        services.administrar_chatbot(text, number, messageId, name)
        return 'Enviado'

    except Exception as e:
        return 'No enviado: ' + str(e)

if __name__ == '__main__':
    app.run()
