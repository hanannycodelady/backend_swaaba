from flask import Blueprint, jsonify
from car_app.Models import db, latest_car
from datetime import datetime, timedelta

latest_car_blueprint = Blueprint('latest_car_blueprint', __name__)

# Fetch the latest cars added in the last X days or sorted by date
@latest_car_blueprint.route('/api/v1/latest-cars', methods=['GET'])
def get_latest_cars():
    try:
        # Define the number of days to consider as "latest" or fetch all cars ordered by the date added
        latest_days = 30
        cutoff_date = datetime.utcnow() - timedelta(days=latest_days)

        # Query cars that were added in the last 30 days
        latest_cars = latest_car.query.filter(latest_car.date_added >= cutoff_date).order_by(latest_car.date_added.desc()).all()

        if not latest_cars:
            return jsonify({"message": "No latest cars found"}), 404

        # Return the latest cars as JSON
        return jsonify({"latest_cars": [car.to_dict() for car in latest_cars]}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
