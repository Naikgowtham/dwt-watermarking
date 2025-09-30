import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from flask_cors import CORS
from backend.routes.watermark_routes import watermark_bp
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app():
    logger.info("Creating Flask app...")
    app = Flask(__name__)
    CORS(app)

    logger.info("Registering watermark blueprint...")
    app.register_blueprint(watermark_bp)

    @app.before_request
    def before_request():
        logger.debug("Received a new request.")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            logger.warning(f"App context teardown due to exception: {exception}")
        else:
            logger.info("App context teardown complete.")

    return app

app = create_app()

if __name__ == "__main__":
    logger.info("Launching Flask server...")
    app.run(debug=True)
