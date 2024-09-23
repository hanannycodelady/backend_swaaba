from flask import Flask, jsonify, request
from Models import Car, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db.init_app(app)

@app.route('/api/cars/search', methods=['GET'])
def search_cars():
    car_name = request.args.get('car_name', '').lower()  # Get car name from query parameter
    # Query database for matching cars
    cars = Car.query.filter(Car.name.ilike(f'%{car_name}%')).all()  # Case-insensitive search

    if cars:
        # Format the response with all matching cars
        car_list = [{'id': car.id, 'name': car.name, 'price': car.price, 'image': car.image_url} for car in cars]
        return jsonify({'status': 'success', 'data': car_list}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No cars found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
