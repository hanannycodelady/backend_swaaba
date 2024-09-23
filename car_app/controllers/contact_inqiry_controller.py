from flask import jsonify, Blueprint, request
from car_app.extensions import db
from car_app.Models.user import User
from car_app.Models.contact_inquiry import Contact_inquiry

contact_blueprint = Blueprint('contact_blueprint', __name__, url_prefix='/api/v2/contact_blueprint')

@contact_blueprint.route('/send', methods=['POST'])
def contact():
    try:
        # Fetch form data from JSON payload
        username = request.json.get("username")
        email = request.json.get("email")
        message = request.json.get("message")
        car_id = request.json.get("car_id")  # Get car_id from request
        phone_number = request.json.get("phone_number")  # Get phone_number from request

        # Debugging: Print received data
        print(f"Received data - Username: {username}, Email: {email},  Message: {message}, Car ID: {car_id}, Phone Number: {phone_number}")

        # Retrieve user ID based on email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Create a new contact message
        contact_inquiry = Contact_inquiry(
            user_id=user.id,
            username=username,
            email=email,
            message=message,
            car_id=car_id,
            phone_number=phone_number
        )
        db.session.add(contact_inquiry)
        db.session.commit()

        return jsonify({"message": "Your message has been sent successfully!", "status": "success"}), 201

    except KeyError as e:
        print(f"Missing form key: {e}")
        return jsonify({"error": f"Missing form key: {e}"}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
 