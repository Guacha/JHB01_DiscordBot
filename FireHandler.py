import pyrebase
from dotenv import load_dotenv
import os
from Economia import Item

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

    def get_pene(self, guid: int, uuid: int):
        """Obtiene el pene de un usuario en un servidor específico"""
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

    def get_pajas(self, guid: int, uuid: int):
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
        if cont_act.pyres is not None:
            self.__db.child(guid).child('server-stats').update({'reset-timer': cont_act.val() - 5})

        else:
            self.__db.child(guid).child('server-stats').update({'reset-timer': 7200 - 5})

    def get_reset_timer(self, guid):
        """Obtiene el estado actual del contador"""
        cont_act = self.__db.child(guid).child('server-stats').child('reset-timer').get()

        value = cont_act.val()

        if value is not None:
            return value

        else:  # En caso de que el contador aún no se haya creado en la base de datos
            self.__db.child(guid).child('server-stats').update({'reset-timer': 10079})
            return 10079

    def reset_all(self, guid):
        # Reiniciamos el timer
        self.__db.child(guid).child('server-stats').update({'reset-timer': 7200})

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
                if user.val()['pajas'] > 0:
                    res[user.key()] = user.val()['pajas']

        return res

    def get_paja_winners(self, guid):

        lista_pajas = self.get_all_pajas(guid)

        if lista_pajas == {}:
            return []

        lista_ordenada = sorted(lista_pajas.items(), key=lambda x: x[1], reverse=True)

        ganadores = []

        main_pajero = lista_ordenada[0]
        ganadores.append(main_pajero)

        for pajero in lista_ordenada[1:]:
            if pajero[1] == main_pajero[1]:
                ganadores.append(pajero)

            else:
                break

        return ganadores

    def get_inventory(self, guid, uuid):
        """Obtiene el inventario de un usuario en un servidor específico"""

        inventory_response = self.__db.child(guid).child('user-stats').child(uuid).child('inventario').get()

        inventory = inventory_response.val()

        return inventory if inventory is not None else {}

    def get_all_penes(self, guid):
        guild_users = self.__db.child(guid).child("user-stats").get()

        # Diccionario que contendrá los UUID y el tamaño del pene
        res = {}
        for user in guild_users.each():
            if 'tamaño' in user.val():
                res[user.key()] = user.val()['tamaño']

        return res

    def get_pene_mayor(self, guid):
        penes = self.get_all_penes(guid)

        max_tam = -1
        for uuid in penes:
            if penes[uuid] > max_tam:
                max_tam = penes[uuid]

        return max_tam

    def get_admins(self, guid):
        admin_ids = []
        max_tam = self.get_pene_mayor(guid)

        penes = self.get_all_penes(guid)

        for pene in penes:
            if penes[pene] == max_tam:
                admin_ids.append(pene)

        return admin_ids

    def get_penecreditos(self, guid, uuid):
        creditos = self.__db.child(guid).child('user-stats').child(uuid).child('penecreditos').get()

        num = creditos.val()

        return num if num is not None else 0

    def give_penecreditos(self, guid, uuid, given_creditos):

        creditos_actuales = self.__db.child(guid).child('user-stats').child(uuid).child('penecreditos').get()

        num = creditos_actuales.val()

        if num is None:
            self.__db.child(guid).child('user-stats').child(uuid).update({'penecreditos': given_creditos})

        else:
            self.__db.child(guid).child('user-stats').child(uuid).update(
                {'penecreditos': num + given_creditos}
            )

    def consume_pc(self, guid, uuid, credits: int):
        user = self.__db.child(guid).child('user-stats').child(uuid).child('penecreditos').get()
        new_creditos = user.val() - credits
        self.__db.child(guid).child('user-stats').child(uuid).update({'penecreditos': new_creditos})

    def purchase(self, guid, uuid, item: Item):
        inventario = self.__db.child(guid).child('user-stats').child(uuid).child('inventario').get()
        self.consume_pc(guid, uuid, item.cost)

        try:
            item_amount = inventario.val()[item.name]
            self.__db.child(guid).child('user-stats').child(uuid)\
                .child('inventario').update({item.name: item_amount + 1})

        except KeyError:
            self.__db.child(guid).child('user-stats').child(uuid).child('inventario').update({item.name: 1})

        except TypeError:
            self.__db.child(guid).child('user-stats').child(uuid).child('inventario').update({item.name: 1})

    def consume_item(self, guid, uuid, item: Item):
        inventario = self.__db.child(guid).child('user-stats').child(uuid).child('inventario').get()
        item_amount = inventario.val()[item.name]

        if item_amount > 1:
            self.__db.child(guid).child('user-stats').child(uuid).child('inventario').update({item.name: item_amount - 1})

        else:
            self.__db.child(guid).child('user-stats').child(uuid).child('inventario').child(item.name).remove()

    def increase_prob(self, guid, uuid, price, increase=1):

        current_chance = self.__db.child(guid).child('user-stats').child(uuid).child('prob').get()

        try:
            self.consume_pc(guid, uuid, price)
            self.__db.child(guid).child('user-stats').child(uuid).update({'prob': current_chance.val() + increase})

        except TypeError:
            self.__db.child(guid).child('user-stats').child(uuid).update({'prob': increase})


if __name__ == '__main__':
    db = Database()





