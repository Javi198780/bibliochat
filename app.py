import os
import requests
import gradio as gr

# Token Wit.ai desde variable de entorno
WIT_TOKEN = os.getenv("WIT_TOKEN")
if not WIT_TOKEN:
    raise ValueError("No se encontró la variable de entorno 'WIT_TOKEN'. Agrega WIT_TOKEN en Render.")

def chatbot_respuesta(mensaje):
    url = "https://api.wit.ai/message?v=20250101&q=" + requests.utils.quote(mensaje)
    headers = {"Authorization": f"Bearer {WIT_TOKEN}"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        intent = data.get("intents", [{}])[0].get("name", "desconocido")

        if intent == "Hola":
            return "¡Hola! 👋 ¿Cómo estás?"
        elif intent == "Horario":
            return "La biblioteca atiende de lunes a viernes de 8:00 a 18:00. 📚"
        else:
            return "Lo siento, no entendí tu mensaje 🤖."
    except Exception as e:
        return f"Error conectando con Wit.ai: {e}"

iface = gr.Interface(
    fn=chatbot_respuesta,
    inputs="text",
    outputs="text",
    title="Chatbot Biblioteca con Wit.ai",
    description="Escribe un mensaje y el bot responderá usando Wit.ai."
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
