from flask import Blueprint, jsonify, make_response, request
from flask_expects_json import expects_json
from controllers.control_person import PersonaControl
from routes.schemas.schameas_person import save_person, edit_person, edit_person_email, change_state_person
from routes.schemas.schemes_auth import schema_login
from controllers.utils.errors import Errors
from controllers.auth import token_required

api_persona = Blueprint('api_persona_persona', __name__)

personaC = PersonaControl()

@api_persona.route('/person')
@token_required
def home():
    return make_response(
        jsonify({"msg" : "OK", "code" : 200, "datos" : ([i.serialize for i in personaC.list()])}), 
        200
    )


@api_persona.route('/person/save'   , methods = ["POST"])
#@token_required
@expects_json(save_person)
def save_person():
    data = request.json 
    id = personaC.savePerson(data = data)
    if(id >= 0):
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : {"tag" : "datos guardados"}}), 
                200
        )
    else:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(id)]}}), 
                400
    )


@api_persona.route('/person/modify' , methods = ["POST"])
@token_required
@expects_json(edit_person)
def modify_person():
    data = request.json 
    id = personaC.modifyPerson(data = data)
    if(id >= 0):
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : {"tag" : "datos guardados"}}), 
                200
        )
    else:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(id)]}}), 
                400
    )

@api_persona.route('/person/modify/email' , methods = ["POST"])
@token_required
@expects_json(edit_person_email)
def modify_personal_email():
    data = request.json 
    id = personaC.modifyPersonalEmail(data = data)
    if(id >= 0):
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : {"tag" : "datos guardados"}}), 
                200
        )
    else:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(id)]}}), 
                400
    )

@api_persona.route('/person/search/dni/<dni>' , methods = ["GET"])
@token_required
def search_person_dni(dni):
    persona = personaC.searchPersonByDni(dni) 
    if type(persona)==int:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(persona)]}}), 
                400
        )
    else:
        return make_response(
            jsonify({"msg" : "OK", "code" : 200, "datos" : (persona)}), 
            200
        )
    
@api_persona.route('/person/search/uid/<uid>' , methods = ["GET"])
@token_required
def search_person_uid(uid):
    persona = personaC.searchPersonByUid(uid) 
    if type(persona)==int:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(persona)]}}), 
                400
        )
    else:
        return make_response(
            jsonify({"msg" : "OK", "code" : 200, "datos" : (persona)}), 
            200
        )
 
@api_persona.route('/person/change_state' , methods = ["POST"])
@token_required
@expects_json(change_state_person)
def change_state_person():
    data = request.json 
    id = personaC.changeStatePerson(data = data) 
    if(id == 1):
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : {"tag" : "persona desactivada"}}), 
                200
        )
    elif (id == 2):
        return make_response(
                jsonify({"msg" : "OK", "code" : 200, "datos" : {"tag" : "persona activada"}}), 
                200
        )
    else:
        return make_response(
                jsonify({"msg" : "ERROR", "code" : 400, "datos" :{"error" : Errors.error[str(id)]}}), 
                400
    )

@api_persona.route('/login', methods = ['POST'])
@expects_json(schema_login)
def login():

    values = request.json

    response = personaC.login(values = values)

    return make_response(jsonify(response), response['code'])
    
