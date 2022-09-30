from unittest import installHandler
from flask_app.config.mysqlconnection import connectToMySQL
from .ninjas import Ninja

class Dojo:
    def __init__(self, data):
        #data = {"id":1, name:Chile, created_at_ ......}
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        #Una lista con todos los ninjas
        self.ninjas = []

    @classmethod
    def save(cls, formulario):
        #formulario recibo un diccionario que va a tener como name:Chile por ejemplo
        query = "INSERT INTO dojos (name) VALUES (%(name)s)"
        result = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, formulario)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query)
        #results = [
        # {id:1, name:"Colombia", created at....}
        # {id:2, name:"Chile", created at....}
        # {id:3, name:"Perú", created at....}
        # ]
        dojos = []
        for d in results:
            #d= {id:1, name:"Colombia", created at....}
            dojos.append(cls(d)) #cls(d) --> crea una instancia de dojos y luego el append ingresa esa instancia en la lista de dojos
        return dojos

    @classmethod
    def get_dojo_with_ninja(cls, data):
        #data = {id: 1}(del dojo que queremos ver)
        query = "select * from dojos left join ninjas on ninjas.dojo_id = dojos.id where dojos.id = %(id)s"
        results = connectToMySQL('esquema_dojos_y_ninjas').query_db(query, data)
        #voy a recibir al menos una fila, y esa fila tiene los datos del dojo que quiero desplegar
        dojo = cls(results[0])#por default en 0 siempre voy a tener los valores de dojo
        for row in results:
            ninja = {
                'id': row['ninjas.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'age': row['age'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'dojo_id': row['dojo_id'],

            }
            instancia_ninja = Ninja(ninja)
            dojo.ninjas.append(instancia_ninja)

        return dojo

