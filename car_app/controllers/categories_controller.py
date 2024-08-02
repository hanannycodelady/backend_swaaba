from flask import Blueprint, request, jsonify
from car_app.extensions import db
from car_app.Models.categories import Make, BodyType, FuelType, Transmission, Condition, Color
from flask_jwt_extended import jwt_required, get_jwt_identity

# Blueprint for Make
make = Blueprint('make', __name__ )

@make.route('/create', methods=['POST'])
@jwt_required()
def create_make():
    name = request.json.get('name')
    if name:
        new_make = Make(name=name)
        db.session.add(new_make)
        db.session.commit()
        return jsonify({'message': 'Make created successfully'}), 201
    else:
        return jsonify({'error': 'Name is required'}), 400

# get all 
@make.route('/', methods=['GET'])
def get_all_makes():
    makes = Make.query.all()
    return jsonify([make.name for make in makes])

# get specific
@make.route('/<int:make_id>', methods=['GET'])
def get_make(make_id):
    make = Make.query.get(make_id)
    if make:
        return jsonify({'id': make.id, 'name': make.name})
    else:
        return jsonify({'error': 'Make not found'}), 404
   
#  updating endpoint
@make.route('/edit/<int:make_id>', methods=['PUT'])
@jwt_required()
def update_make(make_id):
    make = Make.query.get(make_id)
    if make:
        name = request.json.get('name')
        if name:
            make.name = name
            db.session.commit()
            return jsonify({'message': 'Make updated successfully'}), 200
        else:
            return jsonify({'error': 'Name is required'}), 400
    else:
        return jsonify({'error': 'Make not found'}), 404
    
# delete endpoints 
@make.route('/delete/<int:make_id>', methods=['DELETE'])
@jwt_required()
def delete_make(make_id):
    make = Make.query.get(make_id)
    if make:
        db.session.delete(make)
        db.session.commit()
        return jsonify({'message': 'Make deleted successfully'}), 200
    else:
        return jsonify({'error': 'Make not found'}), 404

# Blueprint for BodyType
body_type_blueprint = Blueprint('body_type_blueprint', __name__ )

# creating endpoint 

@body_type_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_body_type():
    type = request.json.get('type')
    if type:
        new_body_type = BodyType(type=type)
        db.session.add(new_body_type)
        db.session.commit()
        return jsonify({'message': 'BodyType created successfully'}), 201
    else:
        return jsonify({'error': 'Type is required'}), 400
    
# get all 
@body_type_blueprint.route('/', methods=['GET'])
def get_all_body_types():
    body_types = BodyType.query.all()
    return jsonify([body_type.type for body_type in body_types])

# get specific

@body_type_blueprint.route('/<int:body_type_id>', methods=['GET'])
def get_body_type(body_type_id):
    body_type = BodyType.query.get(body_type_id)
    if body_type:
        return jsonify({'id': body_type.id, 'type': body_type.type})
    else:
        return jsonify({'error': 'BodyType not found'}), 404
    
# udating endpoint
@body_type_blueprint.route('/edit/<int:body_type_id>', methods=['PUT'])
@jwt_required()
def update_body_type(body_type_id):
    body_type = BodyType.query.get(body_type_id)
    if body_type:
        type = request.json.get('type')
        if type:
            body_type.type = type
            db.session.commit()
            return jsonify({'message': 'BodyType updated successfully'}), 200
        else:
            return jsonify({'error': 'Type is required'}), 400
    else:
        return jsonify({'error': 'BodyType not found'}), 404
    
# deleting endpoints
@body_type_blueprint.route('/delete/<int:body_type_id>', methods=['DELETE'])
@jwt_required()
def delete_body_type(body_type_id):
    body_type = BodyType.query.get(body_type_id)
    if body_type:
        db.session.delete(body_type)
        db.session.commit()
        return jsonify({'message': 'BodyType deleted successfully'}), 200
    else:
        return jsonify({'error': 'BodyType not found'}), 404

# Blueprint for FuelType
fuel_type_blueprint = Blueprint('fuel_type_blueprint', __name__)

# creating endpoint
@fuel_type_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_fuel_type():
    type = request.json.get('type')
    if type:
        new_fuel_type = FuelType(type=type)
        db.session.add(new_fuel_type)
        db.session.commit()
        return jsonify({'message': 'FuelType created successfully'}), 201
    else:
        return jsonify({'error': 'Type is required'}), 400
    
# get all 
@fuel_type_blueprint.route('/', methods=['GET'])
def get_all_fuel_types():
    fuel_types = FuelType.query.all()
    return jsonify([fuel_type.type for fuel_type in fuel_types])

# get specific
@fuel_type_blueprint.route('/<int:fuel_type_id>', methods=['GET'])
def get_fuel_type(fuel_type_id):
    fuel_type = FuelType.query.get(fuel_type_id)
    if fuel_type:
        return jsonify({'id': fuel_type.id, 'type': fuel_type.type})
    else:
        return jsonify({'error': 'FuelType not found'}), 404
    
# updating endpoint
@fuel_type_blueprint.route('/edit/<int:fuel_type_id>', methods=['PUT'])
@jwt_required()
def update_fuel_type(fuel_type_id):
    fuel_type = FuelType.query.get(fuel_type_id)
    if fuel_type:
        type = request.json.get('type')
        if type:
            fuel_type.type = type
            db.session.commit()
            return jsonify({'message': 'FuelType updated successfully'}), 200
        else:
            return jsonify({'error': 'Type is required'}), 400
    else:
        return jsonify({'error': 'FuelType not found'}), 404
    
# delete endpoint
@fuel_type_blueprint.route('/delete/<int:fuel_type_id>', methods=['DELETE'])
@jwt_required()
def delete_fuel_type(fuel_type_id):
    fuel_type = FuelType.query.get(fuel_type_id)
    if fuel_type:
        db.session.delete(fuel_type)
        db.session.commit()
        return jsonify({'message': 'FuelType deleted successfully'}), 200
    else:
        return jsonify({'error': 'FuelType not found'}), 404

# Blueprint for Transmission
transmission_blueprint = Blueprint('transmission_blueprint', __name__)

# create endpoint
@transmission_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_transmission():
    type = request.json.get('type')
    if type:
        new_transmission = Transmission(type=type)
        db.session.add(new_transmission)
        db.session.commit()
        return jsonify({'message': 'Transmission created successfully'}), 201
    else:
        return jsonify({'error': 'Type is required'}), 400
    
# get all
@transmission_blueprint.route('/', methods=['GET'])
def get_all_transmissions():
    transmissions = Transmission.query.all()
    return jsonify([transmission.type for transmission in transmissions])

# get specific
@transmission_blueprint.route('/<int:transmission_id>', methods=['GET'])
def get_transmission(transmission_id):
    transmission = Transmission.query.get(transmission_id)
    if transmission:
        return jsonify({'id': transmission.id, 'type': transmission.type})
    else:
        return jsonify({'error': 'Transmission not found'}), 404
    
# creating endpoint  
@transmission_blueprint.route('/edit/<int:transmission_id>', methods=['PUT'])
@jwt_required()  
def update_transmission(transmission_id):
    transmission = Transmission.query.get(transmission_id)
    if transmission:
        type = request.json.get('type')
        if type:
            transmission.type = type
            db.session.commit()
            return jsonify({'message': 'Transmission updated successfully'}), 200
        else:
            return jsonify({'error': 'Type is required'}), 400
    else:
        return jsonify({'error': 'Transmission not found'}), 404
    
# deleting endpoint 
@transmission_blueprint.route('/delete/<int:transmission_id>', methods=['DELETE'])
@jwt_required()
def delete_transmission(transmission_id):
    transmission = Transmission.query.get(transmission_id)
    if transmission:
        db.session.delete(transmission)
        db.session.commit()
        return jsonify({'message': 'Transmission deleted successfully'}), 200
    else:
        return jsonify({'error': 'Transmission not found'}), 404

# Blueprint for Condition
condition_blueprint = Blueprint('condition_blueprint', __name__)

# creating endpoint
@condition_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_condition():
    condition = request.json.get('condition')
    if condition:
        new_condition = Condition(condition=condition)
        db.session.add(new_condition)
        db.session.commit()
        return jsonify({'message': 'Condition created successfully'}), 201
    else:
        return jsonify({'error': 'Condition is required'}), 400
    
# get all endpoints
@condition_blueprint.route('/', methods=['GET'])
def get_all_conditions():
    conditions = Condition.query.all()
    return jsonify([condition.condition for condition in conditions])

# get specific condition end point
@condition_blueprint.route('/<int:condition_id>', methods=['GET'])
def get_condition(condition_id):
    condition = Condition.query.get(condition_id)
    if condition:
        return jsonify({'id': condition.id, 'condition': condition.condition})
    else:
        return jsonify({'error': 'Condition not found'}), 404
    
# editing endpoint
@condition_blueprint.route('/edit/<int:condition_id>', methods=['PUT'])
@jwt_required() 
def update_condition(condition_id):
    condition = Condition.query.get(condition_id)
    if condition:
        condition_value = request.json.get('condition')
        if condition_value:
            condition.condition = condition_value
            db.session.commit()
            return jsonify({'message': 'Condition updated successfully'}), 200
        else:
            return jsonify({'error': 'Condition is required'}), 400
    else:
        return jsonify({'error': 'Condition not found'}), 404
# deletig endpoints 
@condition_blueprint.route('/delete/<int:condition_id>', methods=['DELETE'])
@jwt_required()
def delete_condition(condition_id):
    condition = Condition.query.get(condition_id)
    if condition:
        db.session.delete(condition)
        db.session.commit()
        return jsonify({'message': 'Condition deleted successfully'}), 200
    else:
        return jsonify({'error': 'Condition not found'}), 404

# Blueprint for Color
color_blueprint = Blueprint('color_blueprint', __name__)

# create color endpoint
@color_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_color():
    color = request.json.get('color')
    if color:
        new_color = Color(color=color)
        db.session.add(new_color)
        db.session.commit()
        return jsonify({'message': 'Color created successfully'}), 201
    else:
        return jsonify({'error': 'Color is required'}), 400
    
# get_all_colors endpoint
@color_blueprint.route('/', methods=['GET'])
def get_all_colors():
    colors = Color.query.all()
    return jsonify([color.color for color in colors])

# get aspecific color 
@color_blueprint.route('/<int:color_id>', methods=['GET'])
def get_color(color_id):
    color = Color.query.get(color_id)
    if color:
        return jsonify({'id': color.id, 'color': color.color})
    else:
        return jsonify({'error': 'Color not found'}), 404
# editing endpoint
@color_blueprint.route('/edit/<int:color_id>', methods=['PUT'])
@jwt_required()
def update_color(color_id):
    color = Color.query.get(color_id)
    if color:
        color_value = request.json.get('color')
        if color_value:
            color.color = color_value
            db.session.commit()
            return jsonify({'message': 'Color updated successfully'}), 200
        else:
            return jsonify({'error': 'Color is required'}), 400
    else:
        return jsonify({'error': 'Color not found'}), 404
    
# deleting the color
@color_blueprint.route('/delete/<int:color_id>', methods=['DELETE'])
@jwt_required()
def delete_color(color_id):
    color = Color.query.get(color_id)
    if color:
        db.session.delete(color)
        db.session.commit()
        return jsonify({'message': 'Color deleted successfully'}), 200
    else:
        return jsonify({'error': 'Color not found'}), 404