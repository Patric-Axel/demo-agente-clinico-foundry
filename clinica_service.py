from database import obtener_conexion


def listar_doctores():
    """
    Consulta los doctores registrados en SQLite.

    Devuelve un diccionario serializable que luego podrá recibir
    el modelo mediante Function Calling.
    """
    with obtener_conexion() as conexion:
        filas = conexion.execute("""
            SELECT id, nombre, especialidad, hora_inicio, hora_fin
            FROM doctores
            ORDER BY id
        """).fetchall()

    doctores = [
        {
            "id": fila["id"],
            "nombre": fila["nombre"],
            "especialidad": fila["especialidad"],
            "hora_inicio": fila["hora_inicio"],
            "hora_fin": fila["hora_fin"],
        }
        for fila in filas
    ]

    return {
        "total": len(doctores),
        "doctores": doctores,
    }

def registrar_paciente(
    dni,
    nombre,
    telefono,
    email
):
    with obtener_conexion() as conexion:

        existe = conexion.execute("""
            SELECT id
            FROM pacientes
            WHERE dni = ?
        """, (dni,)).fetchone()

        if existe:
            return {
                "success": False,
                "mensaje": "Ya existe un paciente con ese DNI"
            }

        cursor = conexion.execute("""
            INSERT INTO pacientes
            (dni, nombre, telefono, email)
            VALUES (?, ?, ?, ?)
        """, (
            dni,
            nombre,
            telefono,
            email
        ))

        return {
            "success": True,
            "paciente_id": cursor.lastrowid
        }

def registrar_cita(paciente_id, doctor_id, fecha, hora):
    with obtener_conexion() as conexion:

        doctor = conexion.execute("""
            SELECT id,nombre
            FROM doctores
            WHERE id = ?
        """, (doctor_id,)).fetchone()

        if not doctor:
            return {
                "success": False,
                "mensaje": "Doctor no encontrado"
            }

        cursor = conexion.execute("""
            INSERT INTO citas
            (
                paciente_id,
                doctor_id,
                fecha,
                hora
            )
            VALUES (?, ?, ?, ?)
        """, (
            paciente_id,
            doctor_id,
            fecha,
            hora
        ))

        cita_id = cursor.lastrowid

    return {
        "success": True,
        "cita_id": cita_id,
        "mensaje": "Cita registrada correctamente"
    }

def buscar_paciente_por_dni(dni):

    with obtener_conexion() as conexion:

        paciente = conexion.execute("""
            SELECT *
            FROM pacientes
            WHERE dni = ?
        """, (dni,)).fetchone()

    if not paciente:
        return {
            "success": False,
            "mensaje": "Paciente no encontrado"
        }

    return {
        "success": True,
        "paciente": {
            "id": paciente["id"],
            "dni": paciente["dni"],
            "nombre": paciente["nombre"],
            "telefono": paciente["telefono"],
            "email": paciente["email"]
        }
    }

def obtener_citas_por_dni(dni):

    with obtener_conexion() as conexion:

        filas = conexion.execute("""
            SELECT
                c.id,
                c.fecha,
                c.hora,
                d.nombre as doctor,
                d.especialidad
            FROM citas c
            INNER JOIN pacientes p
                ON c.paciente_id = p.id
            INNER JOIN doctores d
                ON c.doctor_id = d.id
            WHERE p.dni = ?
        """, (dni,)).fetchall()

    citas = []

    for fila in filas:

        citas.append({
            "cita_id": fila["id"],
            "fecha": fila["fecha"],
            "hora": fila["hora"],
            "doctor": fila["doctor"],
            "especialidad": fila["especialidad"]
        })

    return {
        "total": len(citas),
        "citas": citas
    }