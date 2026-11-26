import os
import json

from openai import OpenAI

from database import inicializar_base_datos
from tools import TOOLS, AVAILABLE_FUNCTIONS

FOUNDRY_ACCOUNT = os.getenv("FOUNDRY_ACCOUNT")
ENDPOINT = (f"https://{FOUNDRY_ACCOUNT}.services.ai.azure.com/openai/v1")
MODEL = os.getenv("FOUNDRY_MODEL")
API_KEY = os.getenv("API_KEY_FOUNDRY")

SYSTEM_PROMPT = """
Eres Alicia, asistente virtual del Consultorio Psicológico.

Tus funciones son:

- Mostrar doctores disponibles.
- Mostrar especialidades.
- Registrar pacientes.
- Registrar citas.

Reglas:

1. Si el usuario desea reservar una cita, primero obtén:
   - DNI
   - Nombre completo
   - Teléfono
   - Correo electrónico

2. Luego muestra los doctores disponibles.

3. Solicita:
   - Doctor elegido
   - Fecha
   - Hora

4. Utiliza siempre las herramientas disponibles para obtener información.

5. Nunca inventes doctores, especialidades ni horarios.

6. Responde de forma cordial y profesional.
"""



client = OpenAI(
    base_url=ENDPOINT,
    api_key=API_KEY
)


inicializar_base_datos()


ultima_respuesta_id = None

def preguntar_agente(mensaje_usuario: str):

    global ultima_respuesta_id

    parametros = {
        "model": MODEL,
        "instructions": SYSTEM_PROMPT,
        "input": mensaje_usuario,
        "tools": TOOLS
    }

    # Si ya existe una conversación previa,
    # continuarla usando previous_response_id
    if ultima_respuesta_id:
        parametros["previous_response_id"] = ultima_respuesta_id

    response = client.responses.create(**parametros)

    # Guardar el id de la respuesta
    ultima_respuesta_id = response.id

    function_calls = []

    for item in response.output:

        if item.type == "function_call":
            function_calls.append(item)

    #SI NO REQUIERE USAR FUNTION CALLING

    if not function_calls:
        return response.output_text

    tool_outputs = []

    for function_call in function_calls:

        nombre_funcion = function_call.name

        argumentos = {}

        if function_call.arguments:
            argumentos = json.loads(function_call.arguments)

        funcion = AVAILABLE_FUNCTIONS[nombre_funcion]

        resultado = funcion(**argumentos)

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": function_call.call_id,
                "output": json.dumps(
                    resultado,
                    ensure_ascii=False
                )
            }
        )

    segunda_respuesta = client.responses.create(
        model=MODEL,
        previous_response_id=response.id,
        input=tool_outputs
    )

    # Guardar el nuevo id para seguir
    # la conversación en el siguiente turno

    ultima_respuesta_id = segunda_respuesta.id

    return segunda_respuesta.output_text


# CHAT DE CONSOLA

if __name__ == "__main__":

    print("Consultorio Psicológico")
    print("Escriba 'reiniciar' para limpiar memoria.\n")
    print("Escriba 'salir' para terminar.\n")

    while True:

        pregunta = input("Usuario: ")

        if pregunta.lower() == "salir":
            break

        respuesta = preguntar_agente(pregunta)

        if pregunta.lower() == "reiniciar":
            ultima_respuesta_id = None
            print("\nConversación reiniciada.\n")
            continue

        respuesta = preguntar_agente(pregunta)

        print(f"\nAsistente: {respuesta}\n")