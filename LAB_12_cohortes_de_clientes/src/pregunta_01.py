from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    base_dir = Path(__file__).resolve().parent.parent
    sales_path = base_dir / "data" / "sales.csv.gz"
    output_dir = base_dir / "submission"

    # 1. Cargar los datos
    sales_df = pd.read_csv(sales_path, parse_dates=["OrderDate"])

    # 2. Calcular el mes de orden y el mes de primera compra (cohorte)
    order_period = sales_df["OrderDate"].dt.to_period("M")
    cohort_period = order_period.groupby(sales_df["CustomerID"]).transform("min")

    sales_df["cohort_month"] = cohort_period.astype(str)
    sales_df["period_index"] = (order_period - cohort_period).apply(lambda x: x.n)

    # 3. Contar clientes activos por cohorte y período
    cohort_data = (
        sales_df.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    # 4. Calcular tamaño de cohorte (período 0) y tasa de retención
    cohort_sizes = (
        cohort_data[cohort_data["period_index"] == 0][
            ["cohort_month", "active_customers"]
        ]
        .rename(columns={"active_customers": "cohort_size"})
    )

    cohort_data = cohort_data.merge(cohort_sizes, on="cohort_month", how="left")
    cohort_data["retention_rate"] = (
        cohort_data["active_customers"] / cohort_data["cohort_size"]
    )

    # Ordenar y seleccionar columnas exactas
    cohort_data = (
        cohort_data[
            [
                "cohort_month",
                "period_index",
                "active_customers",
                "cohort_size",
                "retention_rate",
            ]
        ]
        .sort_values(["cohort_month", "period_index"])
        .reset_index(drop=True)
    )

    # 5. Guardar el CSV en submission/
    output_dir.mkdir(parents=True, exist_ok=True)
    cohort_data.to_csv(output_dir / "cohort_retention.csv", index=False)

    # 6. Construir y guardar el mapa de calor (valores no observados quedan como NaN -> vacíos)
    retention_pivot = cohort_data.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        retention_pivot,
        annot=True,
        fmt=".1%",
        cmap="YlGnBu",
        cbar_kws={"label": "Retention Rate"},
        linewidths=0.5,
        linecolor="gray",
    )
    plt.title("Cohort Retention Heatmap")
    plt.xlabel("Period Index (Months)")
    plt.ylabel("Cohort Month")
    plt.tight_layout()
    plt.savefig(output_dir / "cohort_retention_heatmap.png", dpi=150)
    plt.close()

    return cohort_data