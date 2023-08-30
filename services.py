#Este nos ayudara a gestionar el envio de mensajes a wpp

import requests
import sett
import json
import time

def obtenerMensajeWhatsApp(message):
    if 'type' not in message:
        text = 'Mensaje no Reconocido'
        return text
    
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['buttons']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_Reply': text = message['interactive']['list_Reply']['title'] 
    elif typeMessage =='interactive' and message['interactive']['type'] == 'button_Reply': text = message['interactive']['button_Reply']['title']
    else:
        text = 'Mensaje no Reconocido'

    return text

def enviarMensajeWhatsApp(data):
    try: 
        whatsAppToken = sett.whatsAppToken
        whatsapp_url  = sett.whatsAppUrl
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsAppToken}
        reponse = requests.post(whatsapp_url,
                                headers=headers,
                                data=data)
        
        if reponse.status_code == 200:
            return 'mensaje_enviado', 200
        else: 
            return 'Error al enviar el mensaje', reponse.status_code
    except Exception as e: 
        return e, 403

def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply":{
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data 

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "url": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    elif media_type == "image":
        media_id = sett.images.get(media_name, None)
    elif media_type == "video":
        media_id = sett.videos.get(media_name, None)
    elif media_type == "audio":
        media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {"message_id": messageId},
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "messageId": messageId
        }
    )
    return data

def administrar_chatbot(text, number, messageId, name):
    text = text.lower() #Mensaje que se le envia al usuario
    list = []

    if "hola" in text:
        body = "🙌 Hola bienvenido a este *Chatbot*. ¿Cómo te podemos ayudar?"
        footer = "Equipo de Teckers 🤖"
        options = ["✅ *Servicios*", "📆 *Agendar Cita*"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "✅")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "servicios" in text:
        body = "Tenemos varias áreas de consulta para elegir. ¿Cual de estos servicios te gustaría explorar? 🤔"
        footer = "Equipo de Teckers 🤖"
        options = ["Ver productos 💼", "Ver Promociones 📉", "Consultar Politicas de uso 👮‍♂️"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2", messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje","sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "Consultar Politicas de uso" in text:
        body = "Claro que sí, Te enviaremos un pdf para que puedas ver todas nuestras politicas de Uso"
        footer = "Equipo de Teckers 🤖"
        options = ["✅ Sip, enviame el pdf", "No, Gracias ❌"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)
    elif "Sip, enviame el pdf" in text:
        sticker = sticker_Message(number, get_media_id("pelfet","sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento 😉")

        enviarMensajeWhatsApp(sticker)
        enviarMensajeWhatsApp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "", "Politicas de Uso.pdf")
        enviarMensajeWhatsApp(document)
        time.sleep(3)

        body = "¿Te gustaria programar una cita con un especialista para discutir mas a fondo nuestros servicos?"
        footer = "Equipo de Teckers 🤖"
        options = ["✅ Sí agenda una cita", "No, Gracias ❌"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4", messageId)
        list.append(replyButtonData)
    elif "Si, agenda una reunion" in text: 
        body = "Estupendo, Selecciona una fecha y hora para la cita:"
        footer = "Equipo de Teckers 🤖"
        options = ["📆 10: mañana 10:00am", "📆 7 de junio, 2:00pm", "📆 8: de junio, 3:00pm"]

        listReply = listReply_Message(number, options, body, footer, "sed5", messageId)
        list.append(listReply)
    elif "7 de junio, 2:00pm" in text:
        body = "Excelente, has seleccionado el 7 de junio. Te enviaremos un recordatorio un dia antes. ¿Necesitas otra consulta el dia de hoy?"
        footer = "Equipo de Teckers 🤖"
        options = ["✅ Sí, Por favor", "No, Gracias ❌"]

        buttonReply = buttonReply_Message(number, options, body, footer,"sed6", messageId)
        list.append(buttonReply)
    elif ("no, gracias") in text:
        textMessage = textMessage(number, "Perfecto, no dudes en contactarnos sí tienes mas preguntas. ¡Hasta luego! 👋")
        list.append(textMessage)
    else : 
        data = text_Message(number, "Lo siento no te entendi lo que dijiste ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)
    
    for item in list:
        enviarMensajeWhatsApp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s

# para argentina
def replace_start(s):
    if s.startswith("549"):
        return "54" + s[3:]
    else:
        return s       