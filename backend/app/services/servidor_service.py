from typing import Tuple
import psycopg2
#import pyodbc

def test_database_connection(servidor) -> Tuple[bool, str]:
    """
    Prueba conexión según el tipo de base de datos.
    Soporta PostgreSQL/Neon y SQL Server.
    """
    tipo_bd = getattr(servidor, "tipo_bd", "postgresql") or "postgresql"

    try:
        if tipo_bd.lower() in ["postgresql", "neon"]:

            conn = psycopg2.connect(
                host=servidor.host,
                port=int(getattr(servidor, "puerto", 5432) or 5432),
                database=servidor.name_bd,
                user=servidor.user_bd,
                password=servidor.pass_bd,
                sslmode=getattr(servidor, "ssl_mode", "require") or "require",
                connect_timeout=5,
            )

            conn.close()
            return True, "Conexión exitosa a PostgreSQL/Neon"

        if tipo_bd.lower() in ["sqlserver", "sql_server"]:

            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={servidor.host},{getattr(servidor, 'puerto', 1433) or 1433};"
                f"DATABASE={servidor.name_bd};"
                f"UID={servidor.user_bd};"
                f"PWD={servidor.pass_bd};"
                "Timeout=5;"
            )

            conn = pyodbc.connect(conn_str, timeout=5)
            conn.close()
            return True, "Conexión exitosa a SQL Server"

        return False, f"Tipo de base de datos no soportado: {tipo_bd}"

    except Exception as e:
        return False, str(e)


# Compatibilidad con tu código anterior
def test_sql_server_connection(servidor) -> Tuple[bool, str]:
    return test_database_connection(servidor)


def get_database_schemas(servidor):
    try:
        import psycopg2

        conn = psycopg2.connect(
            host=servidor.host,
            port=servidor.puerto,
            database=servidor.name_bd,
            user=servidor.user_bd,
            password=servidor.pass_bd,
            sslmode=servidor.ssl_mode,
            connect_timeout=5
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
            ORDER BY schema_name
        """)

        schemas = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return True, schemas

    except Exception as e:
        return False, str(e)