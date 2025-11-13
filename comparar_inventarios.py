"""
    Script principal para comparar inventarios.
    Importa funciones de módulos separados para procesar cada tipo de documento.
"""
import pandas as pd
import procesar_base
import procesar_kardex
import metodos
from datetime import datetime
import os
import sys

def cargar_excel(path, sheet):
    try:
        df = pd.read_excel(path, sheet_name=sheet)
        print(f"✔ Cargado: {path} (hoja: {sheet}) — filas: {len(df)}")
        return df
    except Exception as e:
        print(f"✖ Error al cargar '{path}' (hoja: '{sheet}'): {e}")
        sys.exit(1)

def comparar_listas_vs_kerno(base_list, kerno_list, tipo, contador):
    """
    base_list y kerno_list son listas mutables de trabajo (se eliminarán elementos al coincidir).
    tipo: cadena para mensajes (e.g. "INGRESO" o "SALIDA")
    contador: dic con 'coincidencias' y 'total_comparaciones' para ser actualizado por referencia.
    """
    i = len(base_list) - 1
    while i >= 0:
        if len(base_list) == 0:
            break

        item_base = base_list[i]
        coincidencia_encontrada = False

        j = len(kerno_list) - 1
        while j >= 0 and not coincidencia_encontrada:
            if len(kerno_list) == 0:
                break

            item_kerno = kerno_list[j]
            contador['total_comparaciones'] += 1

            if metodos.verificar_igualdad(item_kerno, item_base):
                # eliminar ambos inmediatamente
                kerno_list.pop(j)
                base_list.pop(i)
                contador['coincidencias'] += 1
                coincidencia_encontrada = True

                if contador['coincidencias'] % 50 == 0:
                    print(f"  ✓ {contador['coincidencias']} coincidencias | "
                          f"{tipo} base sobrantes: {len(base_list)} | "
                          f"Kerno sobrantes: {len(kerno_list)} | "
                          f"Comparaciones: {contador['total_comparaciones']}")
                break

            j -= 1

        i -= 1

def main():
    # --- Rutas de los archivos ---
    base_ingresos = input("Ingrese la ruta del archivo INGRESOS base: ").strip()
    base_salidas = input("Ingrese la ruta del archivo SALIDAS base: ").strip()
    kardex = input("Ingrese la ruta del archivo kardex kernobi: ").strip()
    mes_comparar = input("Ingrese mes a comparar: ").strip()

    # --- Cargar hojas (con manejo de errores) ---
    df_ingresos = cargar_excel(base_ingresos, sheet="Hoja1")
    df_salidas = cargar_excel(base_salidas, sheet="Hoja1")
    df_kardex = cargar_excel(kardex, sheet="Page 1")

    # --- Procesar documentos ---
    movimientos_ingresos_base = procesar_base.getArrayListBase(df_ingresos, mes_comparar, "INGRESO") or []
    movimientos_salidas_base = procesar_base.getArrayListBase(df_salidas, mes_comparar, "SALIDA") or []
    movimientos_kerno = procesar_kardex.getArrayListMovimientos(df_kardex) or []

    print(f"\nDatos iniciales:")
    print(f"  - Ingresos base: {len(movimientos_ingresos_base)}")
    print(f"  - Salidas base: {len(movimientos_salidas_base)}")
    print(f"  - Kerno: {len(movimientos_kerno)}")

    # Listas de trabajo (copias)
    ingresos_trabajo = movimientos_ingresos_base.copy()
    salidas_trabajo = movimientos_salidas_base.copy()
    kerno_trabajo = movimientos_kerno.copy()

    contador = {'coincidencias': 0, 'total_comparaciones': 0}

    print("\nComparando movimientos (INGRESOS vs KERNO)...")
    comparar_listas_vs_kerno(ingresos_trabajo, kerno_trabajo, "INGRESO", contador)

    print("\nComparando movimientos (SALIDAS vs KERNO)...")
    comparar_listas_vs_kerno(salidas_trabajo, kerno_trabajo, "SALIDA", contador)

    # Resultados finales
    movimientos_ingresos_base = ingresos_trabajo
    movimientos_salidas_base = salidas_trabajo
    movimientos_kerno = kerno_trabajo

    print(f"\n{'='*60}")
    print("Comparación completada:")
    print(f"  - Coincidencias encontradas: {contador['coincidencias']}")
    print(f"  - Total comparaciones realizadas: {contador['total_comparaciones']}")
    print(f"  - Elementos base sobrantes Ingresos: {len(movimientos_ingresos_base)}")
    print(f"  - Elementos base sobrantes Salidas: {len(movimientos_salidas_base)}")
    print(f"  - Elementos kerno sobrantes: {len(movimientos_kerno)}")
    print(f"{'='*60}")

    # --- Exportar movimientos sobrantes a archivo Excel ---
    if movimientos_ingresos_base or movimientos_salidas_base or movimientos_kerno:
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"movimientos_sobrantes_{mes_comparar}_{fecha_hora}.xlsx"
        directorio_base = os.path.dirname(base_ingresos) if os.path.dirname(base_ingresos) else "."
        ruta_archivo_sobrantes = os.path.join(directorio_base, nombre_archivo)

        print(f"\nExportando movimientos sobrantes a: {ruta_archivo_sobrantes}")
        try:
            metodos.exportar_movimientos_sobrantes(
                movimientos_ingresos_base,
                movimientos_salidas_base,
                movimientos_kerno,
                ruta_archivo_sobrantes
            )
            print(f"✅ Archivo creado exitosamente: {ruta_archivo_sobrantes}")
            print(f"   - Base sobrantes Ingresos: {len(movimientos_ingresos_base)} movimientos")
            print(f"   - Base sobrantes Salidas: {len(movimientos_salidas_base)} movimientos")
            print(f"   - Kerno sobrantes: {len(movimientos_kerno)} movimientos")
        except Exception as e:
            print(f"✖ Error al exportar: {e}")
    else:
        print("\n✅ No hay movimientos sobrantes. Todos los movimientos coincidieron.")

if __name__ == "__main__":
    main()
