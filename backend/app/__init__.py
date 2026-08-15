from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .auth.routes import auth_bp
    # from .contact.routes import contact_bp
    # from .feedback.routes import feedback_bp
    from .health.routes import health_bp
    # from .products.routes import products_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    # app.register_blueprint(products_bp, url_prefix="/api/products")
    # app.register_blueprint(contact_bp, url_prefix="/api/contact")
    # app.register_blueprint(feedback_bp, url_prefix="/api/feedback")
    app.register_blueprint(health_bp, url_prefix="/api/health")

    return app
