from models.person import Person
import uuid
from app import Base
import jwt
from datetime import datetime, timedelta
from flask import current_app
from .utils.errors import Errors
import re

class PersonaControl():

    def list(self):
        return Person.query.all()
    
    def savePerson(self, data):
        correo = Person.query.filter_by(email = data['email']).first()
        dni = Person.query.filter_by(dni = data['dni']).first()

        if correo:
            return -41
        
        elif dni:
            return -42
        
        elif len(data['dni']) > 10:
          return -8
        
        elif not data['email'].endswith('@unl.edu.ec'):
            return -3
        
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@unl\.edu\.ec$', data['email']):
            return -3 
        
        else:
            
            persona = Person()
            persona.uid = uuid.uuid4()
            persona.name = data['name'] 
            persona.dni = data['dni']
            persona.last_name = data['last_name']
            persona.email = data['email']
            persona.password = data['password']
            persona.status = True

            Base.session.add(persona)
            Base.session.commit()
            
            return persona.id   


    def modifyPerson(self, data):
        uid = data['external']
        tem_persona = Person.query.filter_by(uid=uid).first()
        if tem_persona:
            if tem_persona.password == data['old_password']:
                persona = Person()
                persona = tem_persona.copy()
                persona.uid = uuid.uuid4()
                persona.name = data['name']
                persona.last_name = data['last_name']
                persona.email = data['email'] 
                persona.password = data['password']  
                Base.session.merge(persona)
                Base.session.commit()
                return persona.id
            else:
                return -43
        else:
            return -40
        
    def modifyPersonalEmail(self, data):
        persona = Person.query.filter_by(uid=data['external']).first()
        if persona:
            correo = Person.query.filter_by(email = data['email']).first()
            if correo:
                return -41
            else:
                temp_persona = persona.copy()
                temp_persona.uid = uuid.uuid4()
                temp_persona.email = data['email'] 
                temp_persona.password = data['password']  
                Base.session.merge(temp_persona)
                Base.session.commit()
                return temp_persona.id
        else:
            return -40
        
    def searchPersonByDni(self, dni):
        persona = Person.query.filter_by(dni=dni).first()
        if persona:
            info = {
                "name": persona.name,
                "email": persona.email,
                "dni": persona.dni,
                "last_name": persona.last_name
            }
            return info
        else:
            return -40
        
    def searchPersonByUid(self, uid):
        persona = Person.query.filter_by(uid=uid).first()
        if persona:
            info = {
                "name": persona.name,
                "email": persona.email,
                "dni": persona.dni,
                "last_name": persona.last_name
            }
            return info
        else:
            return -40  
        
    def changeStatePerson(self, data):
        persona = Person.query.filter_by(uid=data['external']).first()
        if persona:
            try:
                persona.uid = uuid.uuid4()
                if persona.status:
                    persona.status = False
                    id = 1
                else:
                    persona.status = True
                    id = 2
                Base.session.merge(persona)
                Base.session.commit()
                return id
            except:
                return -40
        else:
            return -40
        
    
    def login(self, values):
            
        person = Person.query.filter_by(email = values['email']).first()
            
        if not person:
            return {'msg': 'error', 'code' : 400, 'data': {'error' : Errors.error[str(-11)]}}
            
        if person.password != values['password']:
            return {'msg': 'error', 'code' : 400, 'data': {'error' : Errors.error[str(-11)]}}
            
        token = jwt.encode(
            {
            'uid' : person.uid,
            'exp' : datetime.utcnow() + timedelta(minutes = 20)
            },
            key = current_app.config['SECRET_KEY'],
            algorithm = 'HS512',
        )

        return {
            'token'   : token,
            'code'    : 200,
            'person'  : person.name +" "+ person.last_name,
            'necesary': person.uid
        }
