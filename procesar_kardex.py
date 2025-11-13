"""
    Módulo para procesar datos del archivo kardex.
    Contiene funciones relacionadas con el procesamiento del documento kardex.
"""
import pandas as pd
import ItemMovimiento


def getArrayListMovimientos(dataFrameDatosKardex):
    """
        Recorre fila a fila el DataFrame kardex y crea objetos ItemMovimiento.
    
        Args:
            dataFrameDatosKardex: DataFrame de pandas con los datos del kardex
        
        Returns:
            list: Lista de objetos ItemMovimiento
    """
    movimientos = []
    for fila in dataFrameDatosKardex.itertuples():
        valor_descripcion = fila[2]
        if (
            valor_descripcion != "Descripción"
            and pd.notna(valor_descripcion)
            and valor_descripcion != ""
            and valor_descripcion is not None
        ):
            descripcion = str(valor_descripcion).strip()
            cantidad = fila[13]
            unidad = fila[12]
            costo_unitario = fila[14]
            importe = fila[15]
            fecha = fila[4]
            codigo = fila[1]
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
            movimientos.append(item_movimiento)            
    return movimientos

