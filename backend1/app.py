from flask import Flask
from flask_cors import CORS
from routes.watermark_routes import watermark_bp
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app():
    logger.info("Creating Flask app for DCT Watermarking...")
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

if __name__ == "__main__":
    logger.info("Launching DCT Watermarking Flask server...")
    app = create_app()
    app.run(debug=True, port=5000)  # Different port to avoid conflicts 