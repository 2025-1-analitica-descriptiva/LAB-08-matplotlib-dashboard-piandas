# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """

# 1. Crear la carpeta 'docs' si no existe
os.makedirs('docs', exist_ok=True)

# 2. Función para cargar los datos
def load_data():
    """
    Lee el CSV de datos desde la carpeta data y devuelve un DataFrame.
    """
    return pd.read_csv('files/input/shipping-data.csv')

# 3. Gráfico de envíos por bodega
def create_visual_for_shipping_per_warehouse(df):
    dfc = df.copy()  
    plt.figure()     
    counts = dfc['Warehouse_block'].value_counts()
    counts.plot.bar(
        title='Shipping per Warehouse',
        xlabel='Warehouse block',
        ylabel='Record Count',
        color='tab:blue'
    )
    ax = plt.gca()  
    ax.spines['top'].set_visible(False)   
    ax.spines['right'].set_visible(False)  
    plt.savefig('docs/shipping_per_warehouse.png') 
    plt.close()

# 4. Gráfico de modo de envío
def create_visual_for_mode_of_shipment(df):
    dfc = df.copy()
    plt.figure()
    counts = dfc['Mode_of_Shipment'].value_counts()
    wedge_props = {'width': 0.35, 'edgecolor': 'white'}
    counts.plot.pie(
        labels=counts.index,
        title='Mode of shipment',
        wedgeprops=wedge_props
    )
    plt.savefig('docs/mode_of_shipment.png')
    plt.close()

# 5. Gráfico de calificación promedio de clientes
def create_visual_for_average_customer_rating(df):
    dfc = df.copy()
    stats = dfc[['Mode_of_Shipment','Customer_rating']] \
                .groupby('Mode_of_Shipment') \
                .agg(['min','mean','max'])
    stats.columns = stats.columns.droplevel() 
    mins = stats['min']
    means = stats['mean']
    maxs = stats['max']

    plt.figure()
    plt.barh(
        y=stats.index,
        width=maxs - mins,
        left=mins,
        color='lightgray',
        height=0.9,
        alpha=0.8
    )

    colors = ['tab:green' if m >= 3.0 else 'tab:orange' for m in means]
    plt.barh(
        y=stats.index,
        width=means - 1,
        left=mins,
        color=colors,
        height=0.5,
        alpha=1.0
    )
    plt.title('Average Customer Rating')
    ax = plt.gca()
    ax.spines['left'].set_color('gray')    
    ax.spines['bottom'].set_color('gray')   
    ax.spines['top'].set_visible(False)    
    ax.spines['right'].set_visible(False)  
    plt.savefig('docs/average_customer_rating.png')
    plt.close()
    return colors

# 6. Histograma de peso enviado
def create_visual_for_weight_distribution(df):
    dfc = df.copy()
    plt.figure()
    dfc['Weight_in_gms'].plot.hist(
        title='Shipped Weight Distribution',
        edgecolor='white'
    )
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig('docs/weight_distribution.png')
    plt.close()

# 7. Programa principal
if __name__ == '__main__':
    df = load_data()
    create_visual_for_shipping_per_warehouse(df)
    create_visual_for_mode_of_shipment(df)
    create_visual_for_average_customer_rating(df)
    create_visual_for_weight_distribution(df)

    # 8. Generar el HTML
    html = """<!DOCTYPE html>
<html>
  <body>
    <h1>Shipping Dashboard Example</h1>
    <div style="width:45%;float:left">
      <img src="shipping_per_warehouse.png" alt="Fig 1">
      <img src="mode_of_shipment.png"      alt="Fig 2">
    </div>
    <div style="width:45%;float:left">
      <img src="average_customer_rating.png" alt="Fig 3">
      <img src="weight_distribution.png"     alt="Fig 4">
    </div>
  </body>
</html>
"""
    with open('docs/index.html','w', encoding='utf-8') as f:
        f.write(html)