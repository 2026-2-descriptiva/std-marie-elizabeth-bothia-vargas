import pandas as pd
from pathlib import Path
import numpy as np



def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    base_dir = Path(__file__).resolve().parent.parent
    web_path = base_dir / "data" / "historical_requests_web.csv.gz"
    letter_path = base_dir / "data" / "historical_requests_letter.csv.gz"
    output_dir = base_dir / "submission"

    # Cargar los datos y eliminar duplicados dentro de cada canal
    web_df = pd.read_csv(web_path, parse_dates=["in_date", "out_date"]).drop_duplicates()
    letter_df = pd.read_csv(
        letter_path, parse_dates=["in_date", "out_date"]
    ).drop_duplicates()

    web_df["channel"] = "web"
    letter_df["channel"] = "letter"

    df = pd.concat([web_df, letter_df], ignore_index=True)

    # Calcular días calendario y días hábiles (excluyendo in_date e incluyendo out_date)
    answered_mask = df["out_date"].notna()

    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days

    df["business_days"] = np.nan
    in_dates = df.loc[answered_mask, "in_date"].values.astype("datetime64[D]")
    out_dates = df.loc[answered_mask, "out_date"].values.astype("datetime64[D]")

    # Desplazar +1 día ambos extremos convierte [in_date, out_date) en (in_date, out_date]
    one_day = np.timedelta64(1, "D")
    df.loc[answered_mask, "business_days"] = np.busday_count(
        in_dates + one_day, out_dates + one_day
    )

    # Indicadores de estado y cumplimiento (NaN <= 15 evalúa a False)
    df["is_answered"] = answered_mask
    df["is_pending"] = ~answered_mask
    df["on_time"] = df["business_days"] <= 15
    df["year"] = df["in_date"].dt.year

    #  Tabla 1: channel_summary.csv (ordenada alfabéticamente por channel)
    channel_summary = (
        df.groupby("channel", as_index=False)
        .agg(
            requests=("in_date", "size"),
            answered=("is_answered", "sum"),
            pending=("is_pending", "sum"),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .sort_values("channel")
        .reset_index(drop=True)
    )
    channel_summary["answered"] = channel_summary["answered"].astype(int)
    channel_summary["pending"] = channel_summary["pending"].astype(int)

    #  Tabla 2: yearly_summary.csv (ordenada por year y luego por channel)
    yearly_summary = (
        df.groupby(["year", "channel"], as_index=False)
        .agg(
            requests=("in_date", "size"),
            pending=("is_pending", "sum"),
            on_time_rate=("on_time", "mean"),
        )
        .sort_values(["year", "channel"])
        .reset_index(drop=True)
    )
    yearly_summary["pending"] = yearly_summary["pending"].astype(int)

    #  Tabla 3: entry_day_summary.csv (de lunes a domingo)
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    if "Lunes" in df["day_name"].values or "lunes" in df["day_name"].str.lower().values:
        day_order = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ]

    df["day_name"] = pd.Categorical(df["day_name"], categories=day_order, ordered=True)
    entry_day_summary = (
        df.groupby("day_name", observed=False, as_index=False)
        .agg(
            requests=("in_date", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .sort_values("day_name")
        .reset_index(drop=True)
    )
    entry_day_summary["day_name"] = entry_day_summary["day_name"].astype(str)

    #  Guardar los archivos en submission/ sin índice y retornar las tres tablas
    output_dir.mkdir(parents=True, exist_ok=True)
    channel_summary.to_csv(output_dir / "channel_summary.csv", index=False)
    yearly_summary.to_csv(output_dir / "yearly_summary.csv", index=False)
    entry_day_summary.to_csv(output_dir / "entry_day_summary.csv", index=False)

    return channel_summary, yearly_summary, entry_day_summary   