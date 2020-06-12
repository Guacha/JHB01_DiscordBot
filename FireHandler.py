import pyrebase
from dotenv import load_dotenv
import os

load_dotenv()

class Database:

    def __init__(self):
        config = {
            "apiKey": os.environ.get('GAPI_TOKEN', "null"),
            "authDomain": os.environ.get('AUTH_DOMAIN', "null"),
            "databaseURL": os.environ.get('DB_URL', "null"),
            'storageBucket': os.environ.get('STO_BUK', "null")
        }

        self.__firebase = pyrebase.initialize_app(config)
        self.__db = self.__firebase.database()

    def get_penes(self, guid):
        lista = {}
        guild_users = self.__db.child(guid).child('user-stats').get()

        for user in guild_users.each():
            lista[user.key()] = user.val()['tamaño']

        return lista

    def set_penes(self, guid, uuid, new_tam):
        self.__db.child(guid).child('user-stats').child(uuid).update({'tamaño': new_tam})

    def get_pajas(self, guid):
        lista = {}
        guild_users = self.__db.child(guid).child('user-stats').get()

        for user in guild_users.each():
            lista[user.key()] = user.val()['pajas']

        return lista

    def add_paja(self, guid, uuid):
        act_pajas = self.__db.child(guid).child('user-stats').child(uuid).child('pajas').get()

        # Si el usuario tiene pajas, tomamos su valor actual y le sumamos uno
        if act_pajas.val():
            self.__db.child(guid).child('user-stats').child(uuid).update({'pajas': act_pajas.val() + 1})

        # Si no las tiene, creamos el campo pajas y le asignamos 1
        else:
            self.__db.child(guid).child('user-stats').child(uuid).update({'pajas': 1})

    def reset_countdown(self, guid):
        # Buscamos las estadisticas del servidor y reducimos por uno el contador de reset
        cont_act = self.__db.child(guid).child('server-stats').child('reset-timer').get()

        # Si el servidor tiene contador, debemos reducirlo por 1
        if cont_act.val():
            self.__db.child(guid).child('server-stats').update({'reset-timer': cont_act.val() - 1})

        # Si el servidor no tiene contador, debemos crearlo
            self.__db.child(guid).child('server-stats').update({'reset-timer': 10079})

    def get_all_users_uuid(self, guid):
        """Obtiene todos los usuarios registrados de un gremio que aparezcan en la base de datos"""
        users = self.__db.child(guid).child('user-stats').get()

        #

        for user in users.each():
            print(user.key())


nepe = Database()
nepe.get_all_users_uuid('server-id')