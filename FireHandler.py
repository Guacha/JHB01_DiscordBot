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

    def get_pene(self, guid, uuid):
        user = self.__db.child(guid).child('user-stats').child(uuid).get()

        try:  # Verificar si el usuario existe
            if 'tamaño' in user.val():  # Y si tiene el campo de tamaño
                return user.val()['tamaño']
            else:
                return None
        except TypeError:
            return None

    def set_pene(self, guid, uuid, new_tam):
        self.__db.child(guid).child('user-stats').child(uuid).update({'tamaño': new_tam})

    def get_pajas(self, guid, uuid):
        """Obtiene las pajas de un usuario"""
        pajas = self.__db.child(guid).child('user-stats').child(uuid).child('pajas').get()

        if pajas.val():  # Si tiene el campo de pajas
            return pajas.val()
        else:
            return None

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
        self.__db.child(guid).child('server-stats').update({'reset-timer': cont_act.val() - 1})

    def get_reset_timer(self, guid):
        """Obtiene el estado actual del contador"""
        cont_act = self.__db.child(guid).child('server-stats').child('reset-timer').get()

        if cont_act.val():
            return cont_act.val()
        else: # En caso de que el contador aún no se haya creado en la base de datos
            self.__db.child(guid).child('server-stats').update({'reset-timer': 10079})
            return 10079

    def reset_all(self, guid):
        # Reiniciamos el timer
        self.__db.child(guid).child('server-stats').update({'reset-timer': 10080})

        # Obtenemos todos los usuarios en una lista
        guild_users = self.__db.child(guid).child('user-stats').get()

        for user in guild_users.each():
            # Para cada usuario ponemos sus pajas en 0 y borramos su tamaño
            self.__db.child(guid).child('user-stats').child(user.key()).update({'pajas': 0})
            self.__db.child(guid).child('user-stats').child(user.key()).child('tamaño').remove()

    def get_all_users_uuid(self, guid):
        """Obtiene todos los usuarios registrados de un gremio que aparezcan en la base de datos"""
        users = self.__db.child(guid).child('user-stats').get()

        # creamos una lista vacía que contendrá todos los uuid
        usr_list = []

        for user in users.each():
            usr_list.append(user.key())

        return usr_list

    def get_all_pajas(self, guid):
        guild_users = self.__db.child(guid).child("user-stats").get()

        # Diccionario que contendrá los UUID y la cantidad de pajas
        res = {}
        for user in guild_users.each():
            if 'pajas' in user.val():
                res[user.key()] = user.val()['pajas']

        return res

    def get_all_penes(self, guid):
        guild_users = self.__db.child(guid).child("user-stats").get()

        # Diccionario que contendrá los UUID y el tamaño del pene
        res = {}
        for user in guild_users.each():
            if 'tamaño' in user.val():
                res[user.key()] = user.val()['tamaño']

        return res


nepe = Database()
