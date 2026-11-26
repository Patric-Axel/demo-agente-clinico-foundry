import os
import sqlite3
from pathlib import Path

# En Azure puedes definir DB_PATH=/home/data/consultorio.db.
# En local, por defecto se crea consultorio.db junto a este archivo.
DB_PATH = Path(os.getenv("DB_PATH", Path(__file__).with_name("consultorio.db")))


DOCTORES_INICIALES = [
    (1, "Ana Torres", "Psicología Clínica", "09:00", "17:00"),
    (2, "Luis Mendoza", "Psicología Infantil", "08:00", "16:00"),
    (3, "Carla Rojas", "Terapia de Pareja", "10:00", "18:00"),
    (4, "Diego Vargas", "Neuropsicología", "09:00", "17:00"),
    (5, "María Flores", "Psicología Clínica", "08:00", "16:00"),
    (6, "José Ramírez", "Psicología Organizacional", "09:00", "17:00"),
    (7, "Lucía Castro", "Psicología Infantil", "10:00", "18:00"),
    (8, "Pedro Salazar", "Terapia Familiar", "08:00", "16:00"),
    (9, "Sofía Herrera", "Neuropsicología", "09:00", "17:00"),
    (10, "Andrés Paredes", "Psicología Clínica", "10:00", "18:00"),
]


def obtener_conexion():
    """Abre una conexión SQLite y devuelve filas accesibles por nombre."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion


def inicializar_base_datos():
    """Crea la tabla e inserta los datos de prueba sin duplicarlos."""
    with obtener_conexion() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS doctores (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                hora_fin TEXT NOT NULL
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dni TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT UNIQUE
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
                FOREIGN KEY (doctor_id) REFERENCES doctores(id)
            )
        """)

        

        conexion.executemany("""
            INSERT OR IGNORE INTO doctores
                (id, nombre, especialidad, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?, ?)
        """, DOCTORES_INICIALES)


if __name__ == "__main__":
    inicializar_base_datos()
    with obtener_conexion() as conexion:
        total = conexion.execute(
            "SELECT COUNT(*) FROM doctores"
        ).fetchone()[0]
    print(f"Base de datos lista: {DB_PATH}")
    print(f"Doctores registrados: {total}")
