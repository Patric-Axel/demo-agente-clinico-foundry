from clinica_service import (
    listar_doctores,
    registrar_paciente,
    registrar_cita
)

TOOLS = [
    {
        "type": "function",
        "name": "listar_doctores",
        "description": (
            "Consulta todos los doctores registrados "
            "en el consultorio y sus horarios."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },

    {
        "type": "function",
        "name": "registrar_paciente",
        "description": "Registra un nuevo paciente.",
        "parameters": {
            "type": "object",
            "properties": {
                "dni": {
                    "type": "string"
                },
                "nombre": {
                    "type": "string"
                },
                "telefono": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                }
            },
            "required": [
                "nombre",
                "telefono",
                "email"
            ]
        }
    },

    {
        "type": "function",
        "name": "registrar_cita",
        "description": "Registra una cita médica.",
        "parameters": {
            "type": "object",
            "properties": {
                "paciente_id": {
                    "type": "integer"
                },
                "doctor_id": {
                    "type": "integer"
                },
                "fecha": {
                    "type": "string"
                },
                "hora": {
                    "type": "string"
                }
            },
            "required": [
                "paciente_id",
                "doctor_id",
                "fecha",
                "hora"
            ]
        }
    }
]

AVAILABLE_FUNCTIONS = {
    "listar_doctores": listar_doctores,
    "registrar_paciente": registrar_paciente,
    "registrar_cita": registrar_cita
}