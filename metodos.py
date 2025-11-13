from unidecode import unidecode
import pandas as pd

def comparar_con_unidecode(cadena1, cadena2):
    # 1. Quitar acentos y caracteres especiales (unidecode)
    # 2. Convertir a minúsculas (casefold/lower)
    return unidecode(cadena1).casefold() == unidecode(cadena2).casefold()

def verificar_igualdad(
    movimiento_kerno, 
    movimiento_base
):
    # verificacion fecha
    fechaKerno = movimiento_kerno.getFechaCorta()
    fechaBase = movimiento_base.getFechaCorta()
    igualdades = 0
    if(fechaKerno == fechaBase):
        igualdades += 1
    # Verificar descripcion
    descripcionKerno = movimiento_kerno.descripcion
    descripcionBase = movimiento_base.descripcion

    if(comparar_con_unidecode(descripcionKerno, descripcionBase)):
        igualdades += 1

    # VERIFICACION CANTIDAD
    cantidadKerno = movimiento_kerno.getCantidad()
    cantidadBase = movimiento_base.getCantidad()

    if(cantidadBase == cantidadKerno) :
        igualdades += 1

    # Verificacion de costo unitario
    costoUnitarioKerno = movimiento_kerno.getCostoUnitarioDosCifras()
    costoUnitarioBase = movimiento_base.getCostoUnitarioDosCifras()
    if(costoUnitarioBase == costoUnitarioKerno):
        igualdades += 1
    
    # Importe o total
    importeKerno =  movimiento_kerno.getImporteDosCifras()
    importeBase =  movimiento_base.getImporteDosCifras()

    if(importeBase == importeKerno):
        igualdades += 1

    if igualdades == 5 :
        return True
    return False

def convertir_movimientos_a_dataframe(movimientos):
    """
    Convierte una lista de objetos ItemMovimiento a un DataFrame de pandas.
    
    Args:
        movimientos: Lista de objetos ItemMovimiento
    
    Returns:
        pandas.DataFrame: DataFrame con los datos de los movimientos
    """
    datos = []
    for movimiento in movimientos:
        datos.append({
            'Código': movimiento.codigo if hasattr(movimiento, 'codigo') else '',
            'Descripción': movimiento.descripcion,
            'Cantidad': movimiento.cantidad,
            'Unidad': movimiento.unidad,
            'Costo Unitario': movimiento.getCostoUnitarioDosCifras(),
            'Importe': movimiento.getImporteDosCifras(),
            'Fecha': movimiento.getFechaCorta(),
            'Movimiento': movimiento.movimiento if hasattr(movimiento, 'movimiento') else '',
            'Operación': movimiento.operacion if hasattr(movimiento, 'operacion') else ''
        })
    
    return pd.DataFrame(datos)

def exportar_movimientos_sobrantes(movimientos_base, movimientos_kerno, ruta_archivo):
    """
    Exporta los movimientos sobrantes (no coincidentes) a un archivo Excel.
    
    Args:
        movimientos_base: Lista de movimientos base sobrantes
        movimientos_kerno: Lista de movimientos kerno sobrantes
        ruta_archivo: Ruta donde se guardará el archivo Excel
    
    Returns:
        str: Ruta del archivo creado
    """

    # Crear un escritor de Excel con múltiples hojas
    with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
        # Convertir movimientos base a DataFrame
        if movimientos_base:
            df_base = convertir_movimientos_a_dataframe(movimientos_base)
            df_base.to_excel(writer, sheet_name='Base Sobrantes', index=False)
        else:
            # Crear DataFrame vacío con las columnas
            df_base = pd.DataFrame(columns=['Código', 'Descripción', 'Cantidad', 'Unidad', 
                                           'Costo Unitario', 'Importe', 'Fecha', 'Movimiento', 'Operación'])
            df_base.to_excel(writer, sheet_name='Base Sobrantes', index=False)
        
        # Convertir movimientos kerno a DataFrame
        if movimientos_kerno:
            df_kerno = convertir_movimientos_a_dataframe(movimientos_kerno)
            df_kerno.to_excel(writer, sheet_name='Kerno Sobrantes', index=False)
        else:
            # Crear DataFrame vacío con las columnas
            df_kerno = pd.DataFrame(columns=['Código', 'Descripción', 'Cantidad', 'Unidad', 
                                            'Costo Unitario', 'Importe', 'Fecha', 'Movimiento', 'Operación'])
            df_kerno.to_excel(writer, sheet_name='Kerno Sobrantes', index=False)
    
    return ruta_archivo