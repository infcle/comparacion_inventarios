from flask import Flask
import os

def create_app(config_name='development'):
    """
    Función factory para crear la aplicación Flask.
    """
    # Obtener rutas correctas
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Configuración
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Máximo 50MB por archivo
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app_dir), 'uploads')
    app.config['RESULTS_FOLDER'] = os.path.join(os.path.dirname(app_dir), 'results')
    app.config['SECRET_KEY'] = 'tu-clave-secreta-cambiar-en-produccion'
    
    # Crear carpetas si no existen
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
    
    # Registrar blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
