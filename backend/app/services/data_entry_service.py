import os
import pandas as pd
import tempfile
import psycopg2
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.models import Servidor, DataEntry, DataEntryColumn


def get_conn(servidor):
    return psycopg2.connect(
        host=servidor.host,
        port=servidor.puerto,
        database=servidor.name_bd,
        user=servidor.user_bd,
        password=servidor.pass_bd,
        sslmode=servidor.ssl_mode,
        connect_timeout=10
    )


def test_data_entry_config(db: Session, data, usuario_id: int):
    servidor = db.query(Servidor).filter(
        Servidor.id == data.servidor_id,
        Servidor.usuario_id == usuario_id,
        Servidor.activo == True
    ).first()

    if not servidor:
        return False, "Servidor no encontrado o no pertenece al usuario"

    if not data.columnas:
        return False, "Debe configurar al menos una columna"

    if data.tipo_carga == "INCREMENTAL_PERIOD" and not data.columna_periodo:
        return False, "Debe indicar columna de período"

    if data.tipo_carga == "INCREMENTAL_DATE" and not data.columna_fecha:
        return False, "Debe indicar columna de fecha"

    try:
        conn = get_conn(servidor)
        cur = conn.cursor()

        cur.execute("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name IN (%s, %s)
        """, (data.esquema_raw, data.esquema_silver))

        schemas = [x[0] for x in cur.fetchall()]

        if data.esquema_raw not in schemas:
            return False, f"No existe el esquema RAW: {data.esquema_raw}"

        if data.esquema_silver not in schemas:
            return False, f"No existe el esquema SILVER: {data.esquema_silver}"

        tipos_validos = [
            "VARCHAR(500)",
            "TEXT",
            "INTEGER",
            "BIGINT",
            "DECIMAL(20,6)",
            "DOUBLE PRECISION",
            "DATE",
            "TIMESTAMP",
            "BOOLEAN"
        ]

        for col in data.columnas:
            if col.tipo_destino not in tipos_validos:
                return False, f"Tipo no válido: {col.tipo_destino}"

        cur.close()
        conn.close()

        return True, "Validación correcta. La carga puede ejecutarse."

    except Exception as e:
        return False, str(e)


def guardar_data_entry(db: Session, data, usuario_id: int):

    existente = db.query(DataEntry).filter(
        DataEntry.usuario_id == usuario_id,
        DataEntry.servidor_id == data.servidor_id,
        DataEntry.nombre_tabla_raw == data.nombre_tabla_raw,
        DataEntry.nombre_tabla_silver == data.nombre_tabla_silver
    ).first()

    # =========================================================
    # UPDATE
    # =========================================================
    if existente:

        existente.esquema_raw = data.esquema_raw
        existente.esquema_silver = data.esquema_silver
        existente.tipo_archivo = data.tipo_archivo
        existente.encoding = data.encoding
        existente.separador = data.separador
        existente.tipo_carga = data.tipo_carga
        existente.columna_periodo = data.columna_periodo
        existente.columna_fecha = data.columna_fecha
        existente.columna_delete = data.columna_delete
        existente.activo = True

        db.commit()

        # ============================================
        # BORRAR COLUMNAS ANTERIORES
        # ============================================
        db.query(DataEntryColumn).filter(
            DataEntryColumn.data_entry_id == existente.id
        ).delete()

        db.commit()

        # ============================================
        # INSERTAR NUEVAS COLUMNAS
        # ============================================
        for col in data.columnas:

            db.add(DataEntryColumn(
                data_entry_id=existente.id,
                columna_origen=col.columna_origen,
                columna_limpia=col.columna_limpia,
                tipo_origen=col.tipo_origen,
                tipo_destino=col.tipo_destino,
                permite_nulos=col.permite_nulos,
                es_primary_key=col.es_primary_key,
                orden=col.orden
            ))

        db.commit()
        db.refresh(existente)

        return existente

    # =========================================================
    # INSERT
    # =========================================================
    entry = DataEntry(
        usuario_id=usuario_id,
        servidor_id=data.servidor_id,
        nombre_tabla_raw=data.nombre_tabla_raw,
        nombre_tabla_silver=data.nombre_tabla_silver,
        esquema_raw=data.esquema_raw,
        esquema_silver=data.esquema_silver,
        tipo_archivo=data.tipo_archivo,
        encoding=data.encoding,
        separador=data.separador,
        tipo_carga=data.tipo_carga,
        columna_periodo=data.columna_periodo,
        columna_fecha=data.columna_fecha,
        columna_delete=data.columna_delete,
        truncate_before_load=False,
        activo=True
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    for col in data.columnas:

        db.add(DataEntryColumn(
            data_entry_id=entry.id,
            columna_origen=col.columna_origen,
            columna_limpia=col.columna_limpia,
            tipo_origen=col.tipo_origen,
            tipo_destino=col.tipo_destino,
            permite_nulos=col.permite_nulos,
            es_primary_key=col.es_primary_key,
            orden=col.orden
        ))

    db.commit()
    db.refresh(entry)

    return entry

def tabla_existe(cur, esquema, tabla):
    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_name = %s
        )
    """, (esquema, tabla))

    return cur.fetchone()[0]

def crear_tabla_raw(cur, data):
    columnas_sql = []

    for col in data.columnas:
        columnas_sql.append(f'"{col.columna_limpia}" VARCHAR(500)')

    columnas_sql.extend([
        '"file_name" VARCHAR(500)',
        '"ingestion_time" TIMESTAMP',
        '"processing_time" TIMESTAMP',
        '"data_entry_id" INTEGER'
    ])

    sql = f"""
        CREATE TABLE IF NOT EXISTS "{data.esquema_raw}"."{data.nombre_tabla_raw}" (
            {", ".join(columnas_sql)}
        )
    """

    cur.execute(sql)


def crear_tabla_silver(cur, data):
    columnas_sql = []

    for col in data.columnas:
        nullable = "" if col.permite_nulos else " NOT NULL"
        columnas_sql.append(
            f'"{col.columna_limpia}" {col.tipo_destino}{nullable}'
        )

    columnas_sql.extend([
        '"file_name" VARCHAR(500)',
        '"ingestion_time" TIMESTAMP',
        '"processing_time" TIMESTAMP',
        '"data_entry_id" INTEGER'
    ])

    sql = f"""
        CREATE TABLE IF NOT EXISTS "{data.esquema_silver}"."{data.nombre_tabla_silver}" (
            {", ".join(columnas_sql)}
        )
    """

    cur.execute(sql)


def insertar_raw(cur, data, df):
    columnas = [col.columna_limpia for col in data.columnas]

    placeholders = ", ".join(["%s"] * len(columnas))
    columnas_sql = ", ".join([f'"{c}"' for c in columnas])

    sql = f"""
        INSERT INTO "{data.esquema_raw}"."{data.nombre_tabla_raw}"
        ({columnas_sql})
        VALUES ({placeholders})
    """

    rows = df[columnas].astype(str).values.tolist()
    cur.executemany(sql, rows)


def insertar_silver(cur, data):
    columnas = [col.columna_limpia for col in data.columnas]

    select_casts = []

    for col in data.columnas:
        select_casts.append(
            f'NULLIF("{col.columna_limpia}", \'\')::{col.tipo_destino} AS "{col.columna_limpia}"'
        )

    columnas_sql = ", ".join([f'"{c}"' for c in columnas])

    sql = f"""
        INSERT INTO "{data.esquema_silver}"."{data.nombre_tabla_silver}"
        ({columnas_sql})
        SELECT {", ".join(select_casts)}
        FROM "{data.esquema_raw}"."{data.nombre_tabla_raw}"
    """

    cur.execute(sql)

async def ejecutar_data_entry(db, data, archivo, usuario_id, data_entry_id=None):
    ok, mensaje = test_data_entry_config(db, data, usuario_id)

    if not ok:
        raise Exception(mensaje)

    if not data_entry_id:
        existente = db.query(DataEntry).filter(
            DataEntry.usuario_id == usuario_id,
            DataEntry.servidor_id == data.servidor_id,
            DataEntry.nombre_tabla_raw == data.nombre_tabla_raw,
            DataEntry.nombre_tabla_silver == data.nombre_tabla_silver,
            DataEntry.activo == True
        ).first()

        if existente:
            data_entry_id = existente.id
        else:
            entry = guardar_data_entry(db, data, usuario_id)
            data_entry_id = entry.id

    servidor = db.query(Servidor).filter(
        Servidor.id == data.servidor_id,
        Servidor.usuario_id == usuario_id
    ).first()

    suffix = os.path.splitext(archivo.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await archivo.read())
        path = tmp.name

    try:
        if data.tipo_archivo == "CSV":
            df = pd.read_csv(path, sep=data.separador or ",", encoding=data.encoding)
        else:
            df = pd.read_excel(path)

        rename_map = {
            col.columna_origen: col.columna_limpia
            for col in data.columnas
        }

        df = df.rename(columns=rename_map)

        columnas_limpias = [col.columna_limpia for col in data.columnas]
        df = df[columnas_limpias]

        conn = get_conn(servidor)
        cur = conn.cursor()

        if tabla_existe(cur, data.esquema_raw, data.nombre_tabla_raw):
            raise Exception(
                f"La tabla RAW {data.esquema_raw}.{data.nombre_tabla_raw} ya existe. No se puede ejecutar dos veces."
            )

        if tabla_existe(cur, data.esquema_silver, data.nombre_tabla_silver):
            raise Exception(
                f"La tabla SILVER {data.esquema_silver}.{data.nombre_tabla_silver} ya existe. No se puede ejecutar dos veces."
            )

        crear_tabla_raw(cur, data)
        crear_tabla_silver(cur, data)

        conn.commit()

        insertar_raw(cur, data, df)
        insertar_silver(cur, data)

        conn.commit()

        cur.close()
        conn.close()

        os.remove(path)

        return {
            "exitoso": True,
            "mensaje": "Carga ejecutada correctamente",
            "data_entry_id": data_entry_id,
            "registros": len(df)
        }

    except Exception as e:
        try:
            conn.rollback()
            cur.close()
            conn.close()
        except Exception:
            pass

        if os.path.exists(path):
            os.remove(path)

        raise e

async def cargar_archivo_existente(db, data_entry_id: int, archivo, usuario_id: int):

    entry = db.query(DataEntry).filter(
        DataEntry.id == data_entry_id,
        DataEntry.usuario_id == usuario_id,
        DataEntry.activo == True
    ).first()

    if not entry:
        raise Exception("Configuración de carga no encontrada")

    servidor = db.query(Servidor).filter(
        Servidor.id == entry.servidor_id,
        Servidor.usuario_id == usuario_id,
        Servidor.activo == True
    ).first()

    if not servidor:
        raise Exception("Servidor no encontrado")

    columnas = db.query(DataEntryColumn).filter(
        DataEntryColumn.data_entry_id == entry.id
    ).order_by(DataEntryColumn.orden.asc()).all()

    if not columnas:
        raise Exception("La configuración no tiene columnas registradas")

    suffix = os.path.splitext(archivo.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await archivo.read())
        path = tmp.name

    try:
        if entry.tipo_archivo == "CSV":
            df = pd.read_csv(
                path,
                sep=entry.separador or ",",
                encoding=entry.encoding or "UTF-8"
            )
        elif entry.tipo_archivo == "XLSX":
            df = pd.read_excel(path)
        else:
            raise Exception(f"Tipo de archivo no soportado: {entry.tipo_archivo}")

        rename_map = {
            col.columna_origen: col.columna_limpia
            for col in columnas
        }

        columnas_origen = list(rename_map.keys())

        faltantes = [
            col for col in columnas_origen
            if col not in df.columns
        ]

        if faltantes:
            raise Exception(
                "El archivo no contiene las columnas esperadas: "
                + ", ".join(faltantes)
            )

        df = df.rename(columns=rename_map)

        columnas_limpias = [
            col.columna_limpia
            for col in columnas
        ]

        df = df[columnas_limpias]

        now = datetime.now()

        df["file_name"] = archivo.filename
        df["ingestion_time"] = now
        df["processing_time"] = now
        df["data_entry_id"] = entry.id

        conn = get_conn(servidor)
        cur = conn.cursor()

        columnas_insert = columnas_limpias + [
            "file_name",
            "ingestion_time",
            "processing_time",
            "data_entry_id"
        ]

        placeholders = ", ".join(["%s"] * len(columnas_insert))
        columnas_limpias = [
            col.columna_limpia
            for col in columnas
        ]

        columnas_insert = columnas_limpias + [
            "file_name",
            "ingestion_time",
            "processing_time",
            "data_entry_id"
        ]

        columnas_sql = ", ".join([f'"{c}"' for c in columnas_insert])

        insert_raw = f"""
            INSERT INTO "{entry.esquema_raw}"."{entry.nombre_tabla_raw}"
            ({columnas_sql})
            VALUES ({placeholders})
        """

        rows_raw = df[columnas_insert].astype(object).where(
            pd.notnull(df[columnas_insert]),
            None
        ).values.tolist()

        cur.executemany(insert_raw, rows_raw)

        if entry.tipo_carga == "FULL":
            cur.execute(
                f'TRUNCATE TABLE "{entry.esquema_silver}"."{entry.nombre_tabla_silver}"'
            )

        elif entry.tipo_carga == "INCREMENTAL_PERIOD":
            if not entry.columna_periodo:
                raise Exception("La carga incremental por período no tiene columna_periodo configurada")

            periodos = (
                df[entry.columna_periodo]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            if periodos:
                cur.execute(
                    f'''
                    DELETE FROM "{entry.esquema_silver}"."{entry.nombre_tabla_silver}"
                    WHERE "{entry.columna_periodo}" = ANY(%s::text[])
                    ''',
                    (periodos,)
                )

        elif entry.tipo_carga == "INCREMENTAL_DATE":
            if not entry.columna_fecha:
                raise Exception("La carga incremental por fecha no tiene columna_fecha configurada")

            fechas = df[entry.columna_fecha].dropna().unique().tolist()

            if fechas:
                cur.execute(
                    f'''
                    DELETE FROM "{entry.esquema_silver}"."{entry.nombre_tabla_silver}"
                    WHERE "{entry.columna_fecha}" = ANY(%s)
                    ''',
                    (fechas,)
                )

        columnas_limpias = [
            col.columna_limpia
            for col in columnas
        ]

        columnas_insert = columnas_limpias + [
            "file_name",
            "ingestion_time",
            "processing_time",
            "data_entry_id"
        ]

        columnas_sql = ", ".join([f'"{c}"' for c in columnas_insert])

        select_casts = []

        for col in columnas:
            tipo = col.tipo_destino.upper().strip()

            if (
                "DOUBLE" in tipo
                or "DECIMAL" in tipo
                or "NUMERIC" in tipo
                or tipo in ["INTEGER", "BIGINT"]
            ):
                select_casts.append(
                    f'CAST(NULLIF("{col.columna_limpia}", \'\') AS {col.tipo_destino}) AS "{col.columna_limpia}"'
                )

            elif tipo in ["DATE", "TIMESTAMP"]:
                select_casts.append(
                    f'CAST(NULLIF("{col.columna_limpia}", \'\') AS {col.tipo_destino}) AS "{col.columna_limpia}"'
                )

            elif tipo == "BOOLEAN":
                select_casts.append(
                    f'CAST(NULLIF("{col.columna_limpia}", \'\') AS BOOLEAN) AS "{col.columna_limpia}"'
                )

            else:
                select_casts.append(
                    f'CAST("{col.columna_limpia}" AS {col.tipo_destino}) AS "{col.columna_limpia}"'
                )

        select_casts.extend([
            '"file_name"',
            '"ingestion_time"',
            '"processing_time"',
            '"data_entry_id"'
        ])

        insert_silver = f"""
            INSERT INTO "{entry.esquema_silver}"."{entry.nombre_tabla_silver}"
            ({columnas_sql})
            SELECT {", ".join(select_casts)}
            FROM "{entry.esquema_raw}"."{entry.nombre_tabla_raw}"
            WHERE "file_name" = %s
            AND "data_entry_id" = %s
        """
        cur.execute(insert_silver, (archivo.filename, entry.id))

        conn.commit()

        cur.close()
        conn.close()

        return {
            "exitoso": True,
            "mensaje": "Archivo cargado correctamente a RAW y SILVER",
            "raw": f"{entry.esquema_raw}.{entry.nombre_tabla_raw}",
            "silver": f"{entry.esquema_silver}.{entry.nombre_tabla_silver}",
            "registros": len(df)
        }

    except Exception as e:
        try:
            conn.rollback()
            cur.close()
            conn.close()
        except Exception:
            pass

        raise e

    finally:
        if os.path.exists(path):
            os.remove(path)


async def validar_archivo_existente(db, data_entry_id: int, archivo, usuario_id: int):

    entry = db.query(DataEntry).filter(
        DataEntry.id == data_entry_id,
        DataEntry.usuario_id == usuario_id,
        DataEntry.activo == True
    ).first()

    if not entry:
        raise Exception("Configuración de carga no encontrada")

    columnas = db.query(DataEntryColumn).filter(
        DataEntryColumn.data_entry_id == entry.id
    ).order_by(DataEntryColumn.orden.asc()).all()

    if not columnas:
        raise Exception("La configuración no tiene columnas registradas")

    suffix = os.path.splitext(archivo.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await archivo.read())
        path = tmp.name

    try:
        if entry.tipo_archivo == "CSV":
            df = pd.read_csv(
                path,
                sep=entry.separador or ",",
                encoding=entry.encoding or "UTF-8",
                nrows=20
            )

        elif entry.tipo_archivo == "XLSX":
            df = pd.read_excel(path, nrows=20)

        else:
            raise Exception(f"Tipo de archivo no soportado: {entry.tipo_archivo}")

        columnas_esperadas = [
            col.columna_origen
            for col in columnas
        ]

        faltantes = [
            col for col in columnas_esperadas
            if col not in df.columns
        ]

        if faltantes:
            raise Exception(
                "El archivo no contiene las columnas esperadas: "
                + ", ".join(faltantes)
            )

        return {
            "exitoso": True,
            "mensaje": "Archivo validado correctamente",
            "columnas_esperadas": columnas_esperadas,
            "columnas_archivo": list(df.columns)
        }

    finally:
        if os.path.exists(path):
            os.remove(path)