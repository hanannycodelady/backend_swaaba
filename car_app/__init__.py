from flask import Flask
from flask import send_from_directory
import secrets
from car_app.extensions import db, migrate, bcrypt, jwt
from car_app.controllers.user_controller import user
from car_app.controllers.car_Image_controller import car_image_blueprint
from car_app.controllers.car_controller import car_blueprint
from car_app.controllers.review_controller import review_blueprint
from car_app.controllers.transaction_cotroller import transaction
from car_app.controllers.categories_controller import body_type_blueprint
from car_app.controllers.categories_controller import transmission_blueprint
from car_app.controllers.categories_controller import condition_blueprint
from car_app.controllers.categories_controller import color_blueprint
from car_app.controllers.categories_controller import fuel_type_blueprint
# from car_app.controllers.latest_car_controller import latest_car_blueprint
from car_app.controllers.categories_controller import make
from car_app.controllers.contact_inqiry_controller import contact_blueprint
from car_app.controllers.order import order_blueprint
from flask_cors import CORS
from car_app.controllers.contact_controller import contact_bp


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object('config.Config')


        # Serve uploaded images
    @app.route('/uploaded_images/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Generate a secure random secret key
    secret_key = secrets.token_urlsafe(32)
    print("JWT Secret Key:", secret_key)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(user)
    app.register_blueprint(contact_bp)
    app.register_blueprint(car_blueprint)
    app.register_blueprint(car_image_blueprint)
    # app.register_blueprint(car_image_blueprint)
    app.register_blueprint(review_blueprint)
    app.register_blueprint(transaction)
    app.register_blueprint(make, url_prefix='/api/v1/makes')
    app.register_blueprint(body_type_blueprint, url_prefix='/api/v1/body_types')
    app.register_blueprint(fuel_type_blueprint, url_prefix='/api/v1/fuel_types')
    app.register_blueprint(transmission_blueprint, url_prefix='/api/v1/transmissions')
    app.register_blueprint(condition_blueprint, url_prefix='/api/v1/conditions')
    app.register_blueprint(color_blueprint, url_prefix='/api/v1/colors')
    app.register_blueprint(contact_blueprint)
    app.register_blueprint(order_blueprint)
    # app.register_blueprint(latest_car_blueprint)

    # Import models
    from car_app.Models.user import User
    from car_app.Models.car import Car
    from car_app.Models.review import Review
    from car_app.Models.transactions import Transaction
    from car_app.Models.categories import Make, BodyType, FuelType, Transmission, Condition, Color
    from car_app.Models.contact_inquiry import Contact_inquiry
    from car_app.Models.order import Order
    from car_app.Models.contact import Contact
    from car_app.Models.car_Image import CarImage 

    @app.route('/')
    def home():
        return "Hello programmers"

    return app
