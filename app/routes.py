"""
Rutas principales de la aplicación Flask.
"""
from flask import Blueprint, render_template, request, jsonify, send_file, current_app
import os
import sys
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos del proyecto original
import procesar_base
import procesar_kardex
import metodos
import ItemMovimiento

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def comparar_listas_vs_kerno(base_list, kerno_list, tipo, contador, tolerancia=0.01):
    """
    Compara dos listas de movimientos y marca coincidencias.
    tolerancia: porcentaje permitido de diferencia (0-100)
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

            # Usar tolerancia en la verificación
            if metodos.verificar_igualdad(item_kerno, item_base, tolerancia):
                kerno_list.pop(j)
                base_list.pop(i)
                contador['coincidencias'] += 1
                coincidencia_encontrada = True
                break

            j -= 1

        i -= 1

@main_bp.route('/')
def index():
    """Página principal."""
    return render_template('index.html')

@main_bp.route('/api/procesar', methods=['POST'])
def procesar():
    """
    Endpoint para procesar los archivos cargados.
    """
    try:
        # Validar que se recibieron los archivos y el mes
        if 'ingresos' not in request.files:
            return jsonify({'error': 'Falta archivo de ingresos'}), 400
        if 'salidas' not in request.files:
            return jsonify({'error': 'Falta archivo de salidas'}), 400
        if 'kardex' not in request.files:
            return jsonify({'error': 'Falta archivo de kardex'}), 400
        if 'mes' not in request.form:
            return jsonify({'error': 'Falta el parámetro mes'}), 400
        if 'tolerancia' not in request.form:
            return jsonify({'error': 'Falta el parámetro tolerancia'}), 400

        ingresos_file = request.files['ingresos']
        salidas_file = request.files['salidas']
        kardex_file = request.files['kardex']
        mes_str = request.form['mes']
        tolerancia_str = request.form['tolerancia']

        # Validar nombres de archivos
        if ingresos_file.filename == '':
            return jsonify({'error': 'Archivo de ingresos vacío'}), 400
        if salidas_file.filename == '':
            return jsonify({'error': 'Archivo de salidas vacío'}), 400
        if kardex_file.filename == '':
            return jsonify({'error': 'Archivo de kardex vacío'}), 400

        # Validar que sean archivos Excel
        if not allowed_file(ingresos_file.filename):
            return jsonify({'error': 'Archivo de ingresos debe ser .xlsx o .xls'}), 400
        if not allowed_file(salidas_file.filename):
            return jsonify({'error': 'Archivo de salidas debe ser .xlsx o .xls'}), 400
        if not allowed_file(kardex_file.filename):
            return jsonify({'error': 'Archivo de kardex debe ser .xlsx o .xls'}), 400

        # Validar mes
        try:
            mes = int(mes_str)
            if mes < 1 or mes > 12:
                return jsonify({'error': 'El mes debe estar entre 1 y 12'}), 400
        except ValueError:
            return jsonify({'error': 'El mes debe ser un número'}), 400

        # Validar tolerancia
        try:
            tolerancia = float(tolerancia_str)
            if tolerancia < 0 or tolerancia > 100:
                return jsonify({'error': 'La tolerancia debe estar entre 0 y 100'}), 400
        except ValueError:
            return jsonify({'error': 'La tolerancia debe ser un número'}), 400

        # Guardar archivos temporales
        upload_folder = current_app.config['UPLOAD_FOLDER']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        
        ingresos_path = os.path.join(upload_folder, f'ingresos_{timestamp}.xlsx')
        salidas_path = os.path.join(upload_folder, f'salidas_{timestamp}.xlsx')
        kardex_path = os.path.join(upload_folder, f'kardex_{timestamp}.xlsx')

        ingresos_file.save(ingresos_path)
        salidas_file.save(salidas_path)
        kardex_file.save(kardex_path)

        # Cargar archivos Excel
        df_ingresos = pd.read_excel(ingresos_path, sheet_name='Hoja1')
        df_salidas = pd.read_excel(salidas_path, sheet_name='Hoja1')
        df_kardex = pd.read_excel(kardex_path, sheet_name='Page 1')

        # Procesar documentos
        movimientos_ingresos_base = procesar_base.getArrayListBase(df_ingresos, mes, "INGRESO") or []
        movimientos_salidas_base = procesar_base.getArrayListBase(df_salidas, mes, "SALIDA") or []
        movimientos_kerno = procesar_kardex.getArrayListMovimientos(df_kardex) or []

        # Listas de trabajo (copias)
        ingresos_trabajo = movimientos_ingresos_base.copy()
        salidas_trabajo = movimientos_salidas_base.copy()
        kerno_trabajo = movimientos_kerno.copy()

        contador = {'coincidencias': 0, 'total_comparaciones': 0}

        # Comparar movimientos con tolerancia
        comparar_listas_vs_kerno(ingresos_trabajo, kerno_trabajo, "INGRESO", contador, tolerancia)
        comparar_listas_vs_kerno(salidas_trabajo, kerno_trabajo, "SALIDA", contador, tolerancia)

        # Actualizar listas de sobrantes
        movimientos_ingresos_base = ingresos_trabajo
        movimientos_salidas_base = salidas_trabajo
        movimientos_kerno = kerno_trabajo

        # Exportar resultados
        results_folder = current_app.config['RESULTS_FOLDER']
        nombre_archivo = f'movimientos_sobrantes_mes{mes}_{timestamp}.xlsx'
        ruta_resultado = os.path.join(results_folder, nombre_archivo)

        metodos.exportar_movimientos_sobrantes(
            movimientos_ingresos_base,
            movimientos_salidas_base,
            movimientos_kerno,
            ruta_resultado
        )

        # Limpiar archivos temporales
        for archivo in [ingresos_path, salidas_path, kardex_path]:
            try:
                os.remove(archivo)
            except:
                pass

        return jsonify({
            'success': True,
            'resultado': {
                'coincidencias': contador['coincidencias'],
                'total_comparaciones': contador['total_comparaciones'],
                'ingresos_sobrantes': len(movimientos_ingresos_base),
                'salidas_sobrantes': len(movimientos_salidas_base),
                'kerno_sobrantes': len(movimientos_kerno)
            },
            'archivo': nombre_archivo
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error al procesar: {str(e)}'}), 500

@main_bp.route('/api/descargar/<nombre_archivo>', methods=['GET'])
def descargar(nombre_archivo):
    """
    Endpoint para descargar el archivo de resultados.
    """
    try:
        # Validar nombre de archivo para seguridad
        nombre_archivo = secure_filename(nombre_archivo)
        
        results_folder = current_app.config['RESULTS_FOLDER']
        ruta_archivo = os.path.join(results_folder, nombre_archivo)

        # Verificar que el archivo existe y está dentro de la carpeta permitida
        if not os.path.exists(ruta_archivo) or not ruta_archivo.startswith(results_folder):
            return jsonify({'error': 'Archivo no encontrado'}), 404

        return send_file(
            ruta_archivo,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        return jsonify({'error': f'Error al descargar: {str(e)}'}), 500
