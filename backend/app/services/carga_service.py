import io
import json
from typing import Any, Dict

import pandas as pd


def validar_archivo(
    contenido: bytes,
    filename: str,
    separador: str = ",",
    codificacion: str = "UTF-8",
) -> Dict[str, Any]:
    """
    Lee el archivo (CSV / XLSX / TXT) y retorna columnas + preview de 5 filas.
    """
    try:
        ext = filename.rsplit(".", 1)[-1].lower()

        if ext in ("xlsx", "xls"):
            df = pd.read_excel(io.BytesIO(contenido), nrows=5)
        else:
            sep = "\t" if separador == "TAB" else separador
            df = pd.read_csv(
                io.BytesIO(contenido),
                sep=sep,
                encoding=codificacion,
                nrows=5,
            )

        columnas = [
            {"nombre": col, "tipo": str(df[col].dtype)}
            for col in df.columns
        ]
        preview = df.fillna("").astype(str).values.tolist()

        return {
            "valido": True,
            "columnas": columnas,
            "preview": preview,
            "total_columnas": len(columnas),
        }
    except Exception as e:
        return {"valido": False, "error": str(e)}


def ejecutar_carga(carga, file) -> Dict[str, Any]:
    """
    Lee el archivo, aplica el mapping configurado e inserta en SQL Server.
    Stub — implementar según mapping_json del modelo Carga.
    """
    # TODO: conectar con servidor_service, leer DataFrame completo,
    #       aplicar mapping_json y hacer bulk insert con pyodbc / sqlalchemy.
    return {
        "estado": "pendiente_implementacion",
        "carga_id": carga.id,
        "mensaje": "Lógica de inserción por implementar según mapping de columnas",
    }
