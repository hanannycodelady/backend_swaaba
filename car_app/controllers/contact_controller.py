from flask import jsonify,render_template,Blueprint, request, redirect, url_for, flash
from car_app.extensions import db
from car_app.Models.user import User
from car_app.Models.contact import Contact
from datetime import datetime

contact_bp = Blueprint('contact_bp', __name__, url_prefix='/api/v2/contact_bp')


@contact_bp.route('/send', methods=['POST'])
def contact():
    try:
        # Fetch form data from JSON payload
        username = request.json.get("username")
        email = request.json.get("email")
        subject = request.json.get("subject")
        message = request.json.get("message")
       

        # Debugging: Print received data
        print(f"Received data - Username: {username}, Email: {email}, Subject: {subject}, Message: {message}")

        # Retrieve user ID based on email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Create a new contact message
        contact = Contact(subject=subject, username=username, message=message, email=email, user_id=user.id)
        db.session.add(contact)
        db.session.commit()

        return jsonify({"message": "Your message has been sent successfully!", "status": "success"}), 201

    except KeyError as e:
        print(f"Missing form key: {e}")
        return jsonify({"error": f"Missing form key: {e}"}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
