from unidecode import unidecode
import pandas as pd

def comparar_con_unidecode(cadena1, cadena2):
    # 1. Quitar acentos y caracteres especiales (unidecode)
    # 2. Convertir a minúsculas (casefold/lower)
    if not isinstance(cadena1, str) or not isinstance(cadena2, str):
        return False
    return unidecode(cadena1).casefold() == unidecode(cadena2).casefold()    

def verificar_igualdad(
    movimiento_kerno, 
    movimiento_base,
    tolerancia=0.01
):
    """
    Verifica si dos movimientos son iguales con tolerancia en costo unitario e importe.
    
    Args:
        movimiento_kerno: Movimiento del Kardex
        movimiento_base: Movimiento base
        tolerancia: Porcentaje de tolerancia permitida (0-100)
    
    Returns:
        bool: True si los movimientos son iguales dentro de la tolerancia
    """
    # Convertir tolerancia de porcentaje a decimal
    tolerancia_decimal = tolerancia / 100
    
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

    # Verificacion de costo unitario con tolerancia
    costoUnitarioKerno = movimiento_kerno.getCostoUnitarioDosCifras()
    costoUnitarioBase = movimiento_base.getCostoUnitarioDosCifras()
    
    if costoUnitarioBase > 0:
        diferencia_costo = abs(costoUnitarioBase - costoUnitarioKerno)
        if diferencia_costo <= tolerancia:
            igualdades += 1
    elif costoUnitarioBase == costoUnitarioKerno:
        igualdades += 1
    
    # Importe o total con tolerancia
    importeKerno =  movimiento_kerno.getImporteDosCifras()
    importeBase =  movimiento_base.getImporteDosCifras()

    if importeBase > 0:
        diferencia_importe = abs(importeBase - importeKerno)
        if diferencia_importe <= tolerancia:
            igualdades += 1
    elif importeBase == importeKerno:
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

def exportar_movimientos_sobrantes(movimientos_ingresos_base, movimientos_salidas_base, movimientos_kerno, ruta_archivo):
    """
    Exporta los movimientos sobrantes (no coincidentes) a un archivo Excel.
    
    Args:
        movimientos_ingresos_base: Lista de movimientos ingresos base sobrantes
        movimientos_salidas_base: Lista de movimientos salidas base sobrantes
        movimientos_kerno: Lista de movimientos kerno sobrantes
        ruta_archivo: Ruta donde se guardará el archivo Excel
    
    Returns:
        str: Ruta del archivo creado
    """

    # Crear un escritor de Excel con múltiples hojas
    with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
        hojas = [
            ('Ingresos', movimientos_ingresos_base),
            ('Salidas', movimientos_salidas_base),
            ('Kerno Sobrantes', movimientos_kerno)
        ]

        columnas = ['Código', 'Descripción', 'Cantidad', 'Unidad',
                    'Costo Unitario', 'Importe', 'Fecha', 'Movimiento', 'Operación']
        
        # Convertir movimientos ingresos base a DataFrame
        for nombre, lista in hojas:
            if lista:
                df = convertir_movimientos_a_dataframe(lista)
            else:
                df = pd.DataFrame(columns=columnas)
            df.to_excel(writer, sheet_name=nombre, index=False)
    
    return ruta_archivo