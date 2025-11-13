"""
Script principal para comparar inventarios.
Importa funciones de módulos separados para procesar cada tipo de documento.
"""
import pandas as pd
import procesar_base
import procesar_kardex
import metodos

# --- Rutas de los archivos ---
base = input("Ingrese la ruta del archivo base: ").strip()
kardex = input("Ingrese la ruta del archivo kardex kernobi: ").strip()
mes_comparar = input("Ingrese mes a comparar: ")

# --- Cargar hojas ---
dataFrameDatosBase = pd.read_excel(base, sheet_name="Hoja1")
dataFrameDatosKardex = pd.read_excel(kardex, sheet_name="Page 1")

# --- Procesar documentos ---
# Procesar archivo base
movimientos_base = procesar_base.getArrayListBase(dataFrameDatosBase, mes_comparar)
# Procesar archivo kardex
movimientos_kerno = procesar_kardex.getArrayListMovimientos(dataFrameDatosKardex)

# datos al principio
print(f"cantidad de elementos base inicio: {len(movimientos_base)}")
print(f"cantidad de elementos kerno inicio: {len(movimientos_kerno)}")

# Usar listas de trabajo que se van reduciendo dinámicamente
# Esto permite eliminar elementos ya comparados para evitar comparaciones innecesarias
movimientos_base_trabajo = movimientos_base.copy()
movimientos_kerno_trabajo = movimientos_kerno.copy()

# Contador de coincidencias encontradas
coincidencias_encontradas = 0
total_comparaciones = 0

# Comparar movimientos de forma eficiente y dinámica
# Las listas de trabajo se reducen dinámicamente al eliminar coincidencias
# Esto evita comparar elementos que ya coincidieron (optimización clave)
print("\nComparando movimientos...")

# Iterar en reversa sobre base para poder eliminar elementos sin afectar índices
# Al iterar en reversa, cuando eliminamos un elemento en índice i,
# los elementos en índices < i no se ven afectados
i = len(movimientos_base_trabajo) - 1
while i >= 0:
    # Verificar que aún hay elementos en la lista (puede haber sido vaciada)
    if len(movimientos_base_trabajo) == 0:
        break
        
    movimiento_base = movimientos_base_trabajo[i]
    coincidencia_encontrada = False
    
    # Buscar coincidencia en kerno (iterar en reversa también)
    # Al encontrar coincidencia, eliminamos ambos elementos inmediatamente
    j = len(movimientos_kerno_trabajo) - 1
    while j >= 0 and not coincidencia_encontrada:
        # Verificar que aún hay elementos en la lista
        if len(movimientos_kerno_trabajo) == 0:
            break
            
        movimiento_kerno = movimientos_kerno_trabajo[j]
        total_comparaciones += 1
        
        # Verificar si coinciden
        if metodos.verificar_igualdad(movimiento_kerno, movimiento_base):
            # Coincidencia encontrada: eliminar ambos elementos INMEDIATAMENTE
            # Esto es la clave de la optimización: evita comparaciones futuras
            movimientos_kerno_trabajo.pop(j)
            movimientos_base_trabajo.pop(i)
            coincidencias_encontradas += 1
            coincidencia_encontrada = True
            
            # Mostrar progreso periódicamente
            if coincidencias_encontradas % 50 == 0:
                print(f"  ✓ {coincidencias_encontradas} coincidencias | "
                    f"Base: {len(movimientos_base_trabajo)} | "
                    f"Kerno: {len(movimientos_kerno_trabajo)} | "
                    f"Comparaciones: {total_comparaciones}")
            # Salir del bucle interno ya que encontramos coincidencia
            break
        
        j -= 1
    
    # Decrementar índice para procesar el siguiente elemento base
    # Si encontramos coincidencia, el elemento en i ya fue eliminado,
    # así que el siguiente elemento a procesar está en i-1
    i -= 1

# Las listas de trabajo ahora contienen solo los sobrantes
movimientos_base = movimientos_base_trabajo
movimientos_kerno = movimientos_kerno_trabajo

print(f"\n{'='*60}")
print("Comparación completada:")
print(f"  - Coincidencias encontradas: {coincidencias_encontradas}")
print(f"  - Total comparaciones realizadas: {total_comparaciones}")
print(f"  - Elementos base sobrantes: {len(movimientos_base)}")
print(f"  - Elementos kerno sobrantes: {len(movimientos_kerno)}")
print(f"{'='*60}")

# --- Exportar movimientos sobrantes a archivo Excel ---
if movimientos_base or movimientos_kerno:
    from datetime import datetime
    import os

    # Generar nombre de archivo con fecha y hora
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"movimientos_sobrantes_{mes_comparar}_{fecha_hora}.xlsx"

    # Obtener directorio del archivo base como directorio por defecto
    directorio_base = os.path.dirname(base) if os.path.dirname(base) else "."
    ruta_archivo_sobrantes = os.path.join(directorio_base, nombre_archivo)

    # Exportar movimientos sobrantes
    print(f"\nExportando movimientos sobrantes a: {ruta_archivo_sobrantes}")
    metodos.exportar_movimientos_sobrantes(movimientos_base, movimientos_kerno, ruta_archivo_sobrantes)
    print(f"✅ Archivo creado exitosamente: {ruta_archivo_sobrantes}")
    print(f"   - Base sobrantes: {len(movimientos_base)} movimientos")
    print(f"   - Kerno sobrantes: {len(movimientos_kerno)} movimientos")
else:
    print("\n✅ No hay movimientos sobrantes. Todos los movimientos coincidieron.")