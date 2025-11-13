"""
Módulo para procesar datos del archivo base.
Contiene funciones relacionadas con el procesamiento del documento base.
"""
import pandas as pd
import ItemMovimiento
from datetime import date, datetime

def formatearFecha(fecha, mes) :
    fecha_formateada = ""
    if isinstance(fecha, (datetime, date)):
        fecha_formateada = fecha.strftime("%d/%m/%Y")
    elif isinstance(fecha, str):
        fecha_formateada = fecha.strip()
    else:
        fecha_formateada = str(fecha)

    mes_comparar = int(fecha_formateada[3:5])
    if mes_comparar != mes :
        return fecha_formateada[3:5]+"/"+fecha_formateada[0:2]+"/"+fecha_formateada[6:10]
    return fecha_formateada

def getArrayListBase(dataFrameDatosBase, mes):
    """
        Recorre fila a fila el DataFrame y procesa los datos del archivo base.
    
        Args:
            dataFrameDatosBase: DataFrame de pandas con los datos a procesar
        
        Returns:
            list: Lista con los datos procesados
    """
    resultados = []
    for fila in dataFrameDatosBase.itertuples():
        valor_celda = fila[12]
        if (
            valor_celda != "Descripción"
            and pd.notna(valor_celda)
            and valor_celda != ""
            and valor_celda is not None
        ):
            descripcion = fila[12].strip()            
            # Quitar caracteres especiales como _x0002_
            descripcion = descripcion.replace("_x0002_", "")
            cantidad = fila[13]
            unidad = fila[14].strip()
            costo_unitario = fila[15]
            importe = fila[16]
            fecha = formatearFecha(fila[5], mes)
            codigo = fila[11]
            movimiento = fila[8]
            operacion = fila[7]

            item_movimiento = ItemMovimiento.ItemMovimiento(
                descripcion,
                cantidad,
                unidad,
                costo_unitario,
                importe,
                fecha,
                codigo,
                movimiento,
                operacion
            )
            resultados.append(item_movimiento)
        
    return resultados
