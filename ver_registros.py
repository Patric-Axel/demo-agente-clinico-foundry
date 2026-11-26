from database import obtener_conexion

with obtener_conexion() as conexion:

    print("\n" + "=" * 50)
    print("PACIENTES REGISTRADOS")
    print("=" * 50)

    pacientes = conexion.execute("""
        SELECT *
        FROM pacientes
        ORDER BY id
    """).fetchall()

    if not pacientes:
        print("No hay pacientes registrados.")
    else:
        for paciente in pacientes:
            print(
                f"ID: {paciente['id']} | "
                f"DNI: {paciente['dni']} | "
                f"Nombre: {paciente['nombre']} | "
                f"Teléfono: {paciente['telefono']} | "
                f"Email: {paciente['email']}"
            )

    print("\n" + "=" * 50)
    print("CITAS REGISTRADAS")
    print("=" * 50)

    citas = conexion.execute("""
        SELECT
            c.id,
            p.dni,
            p.nombre AS paciente,
            d.nombre AS doctor,
            d.especialidad,
            c.fecha,
            c.hora
        FROM citas c
        INNER JOIN pacientes p
            ON c.paciente_id = p.id
        INNER JOIN doctores d
            ON c.doctor_id = d.id
        ORDER BY c.id
    """).fetchall()

    if not citas:
        print("No hay citas registradas.")
    else:
        for cita in citas:
            print(
                f"ID Cita: {cita['id']} | "
                f"Paciente: {cita['paciente']} | "
                f"DNI: {cita['dni']} | "
                f"Doctor: {cita['doctor']} | "
                f"Especialidad: {cita['especialidad']} | "
                f"Fecha: {cita['fecha']} | "
                f"Hora: {cita['hora']}"
            )
            