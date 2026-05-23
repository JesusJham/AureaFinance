from typing import Tuple


def test_sql_server_connection(servidor) -> Tuple[bool, str]:
    """
    Prueba la conexión a un SQL Server usando pyodbc.
    Retorna (exitoso: bool, mensaje: str).
    """
    try:
        import pyodbc  # type: ignore

        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={servidor.host};"
            f"DATABASE={servidor.name_bd};"
            f"UID={servidor.user_bd};"
            f"PWD={servidor.pass_bd};"
            "Timeout=5;"
        )
        conn = pyodbc.connect(conn_str, timeout=5)
        conn.close()
        return True, "Conexión exitosa"
    except Exception as e:
        return False, str(e)
