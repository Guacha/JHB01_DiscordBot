import os
import random
import discord

from Scraper import ChampionData
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()

PREFIX = '/'  # Prefijo para los comandos del bot

client = Bot(command_prefix=PREFIX)  # Crear cliente de bot con el prefijo dado


@client.command(name='build',
                description='Comando que te deja saber la build de algún campeón de LoL',
                brief='Obtén la build de un campeón!',
                aliases=['Build', 'builds', 'BUILD', 'Builds', 'BUILDS'],
                pass_context=True)
async def get_builds(context, champ):
    """Con esta funcion se obtienen las builds del scraper, y se entregan al usuario"""

    print('-----------------------------------------------------------')
    print('Comando de builds')  # Debugging
    print(f'Campeón seleccionado: {champ}')

    # Tenemos un diccionario para relacionar cada build a un título y una cadena bien formada
    noms = {
        1: f'Build completa más común de {champ}',
        2: f'Build completa con mayor winrate de {champ}',
        3: f'Iniciales más comunes de {champ}',
        4: f'Iniciales con mayor winrate de {champ}'
    }

    # Creamos el objeto que contiene los datos del champ que se requiera
    champion_data = ChampionData(champ.lower())

    # De este objeto, obtenemos la info de las builds
    build_data = champion_data.builds
    if build_data:  # Verificamos que hayamos conseguido los datos
        markup = discord.Embed(title=f"Items indicados para {champ}", description="Obtenido de Champion.gg")

        for build in build_data:
            itemlist = build_data[build]
            if itemlist:
                itemlist_markup = ' -> '.join(itemlist)
            else:
                itemlist_markup = 'No hay una build aún para este campeón, intentalo más tarde :('

            # Odio discord.py
            # Los items inline se mostrarán en la misma linea, deben estar juntos
            if build > 2:  # Si vamos por los items iniciales, deben ir inline para que sea más entendible
                markup.add_field(name=noms[build], value=itemlist_markup, inline=True)

            else:  # Los primeros dos campos no van inline, tienen demasiada info
                markup.add_field(name=noms[build], value=itemlist_markup, inline=False)

        await context.channel.send(content=None, embed=markup)

    # Si no se consiguieron los datos, hay que avisar que el man es imbécil y escribió algo mal
    else:
        await context.channel.send("Buena imbécil, escribiste mal el nombre del campeón, aprende a escribir")
        print("Campeón no existe")
        print('-----------------------------------------------------------')


# Comando Tierlist para dar la lista de tamaños de penes todo: Hacer la lista y organizarla lindo
@client.command(name='tierlist',
                description='Comando que mantiene una base de datos de tu tamaño del pene',
                brief='El bot te otorga un tamaño de pene!',
                aliases=['list', 'tier', 'TIERLIST', 'listapene'],
                pass_context=True)
async def tierlist(context):
    """Función que obtiene la lista de tamaños de penes, la organiza, y la envía"""
    # todo everything!
    # Placeholder
    await context.channel.send('Tu maldita madre, esto todavía no funciona careverga, '
                               'métete tu comando por el asterisco')


# Comando cuentapajas para contar el total de pajas del servidor
@client.command(name='cuentapajas',
                description='Comando que mantiene una base de datos de la cantidad de pajas que se hace el servidor',
                brief='El bot te cuenta las pajas!',
                aliases=['CUENTAPAJAS', 'Cuentapajas'],
                pass_context=True)
async def get_pajas(context):
    """Método que recorre toda la lista de pajas y suma las pajas de todos los que hayan usado el comando"""
    total = 0  # El número mínimo posible es 0

    # Usando el método para obtener diccionario de pajas
    lista = obtener_pajas(context.guild.id)

    # Iteramos por las llaves del diccionario
    for persona in lista:
        total += int(lista[persona])  # Por cada persona, tomamos sus pajas y las sumamos al total

    await context.channel.send(f'El servidor en conjunto lleva un gran total de {total} pajas')


@client.command(name='paja',
                description='Comando que mantiene una base de datos de la cantidad de pajas que se hace el servidor',
                brief='El bot te cuenta las pajas!',
                aliases=['pajas', 'PAJAS', 'PAJA', 'pajazo', 'PAJAZO'],
                pass_context=True)
async def cuenta_pajas(context):
    usr = str(context.author.id)  # El ID único del usuario que usa el comando
    # Debe ser el ID porque el Username puede cambiar (Y lo hace frecuentemente)

    server = context.guild.id  # El ID único del servidor en el que se ejecuta el comando
    # Debe ser el ID porque el Guildname puede cambiar (Y lo hace frecuentemente)

    lista = obtener_pajas(server)  # obtiene un diccionario de la forma {(UUID): (UU Pajas)}

    if usr in lista:
        print('-----------------------------------------------------------')
        print('Comando de pajas')
        print(f"Usuario existente: {context.author.id}")  # Debugging
        print(f"Pajas de usuario: {lista[usr] + 1}")
        print('-----------------------------------------------------------')

        # Incrementamos las pajas en 1 y amendamos el archivo de pajas
        lista[usr] = lista[usr] + 1
        escribir_pajas(server, lista)

        # Le hacemos saber al usuario cuantas pajas lleva
        await context.channel.send('Llevas {} pajas, {}!'.format(lista[usr], context.author.mention))

    else:
        # Si el usuario no aparece en la lista, nunca ha usado el comando, debemos crear la entrada en la lista
        print('-----------------------------------------------------------')
        print('Comando de pajas')
        print("Usuario Nuevo: {}".format(context.author.id))  # Debugging
        print('-----------------------------------------------------------')

        # Incrementamos las pajas en 1 y amendamos el archivo de pajas
        lista[usr] = 1
        escribir_pajas(server, lista)

        # Le hacemos saber al usuario cuantas pajas lleva
        await context.channel.send('Llevas {} pajas, {}!'.format(lista[usr], context.author.mention))


# Comando para pedir el tamaño del nepe
@client.command(name='pene',
                description='Comando que mantiene una base de datos de tu tamaño del pene',
                brief='El bot te otorga un tamaño de pene!',
                aliases=['penecito', 'penesito', 'penezote', 'penesote'],
                pass_context=True)
async def penecito(context):
    """Función que obtiene el tamaño de la lista de penes del servidor"""
    usr = str(context.author.id)  # El ID único del usuario que usa el comando
    # Debe ser el ID porque el Username puede cambiar (Y lo hace frecuentemente)

    server = context.guild.id  # El ID único del servidor en el que se ejecuta el comando
    # Debe ser el ID porque el Guildname puede cambiar (Y lo hace frecuentemente)

    lista = obtener_sizes(server)  # obtiene un diccionario de la forma {(UUID): (UU Size)}

    if usr in lista:  # Buscamos si el usuario ya tiene un tamaño de pene registrado
        # Si ya ha usado el comando antes, debemos buscar el nombre en la lista

        print('-----------------------------------------------------------')
        print('Comando de pene')
        print("Usuario existente: {}".format(context.author.id))  # Debugging
        print("Tamaño de usuario: {}".format(lista[usr]))
        print('-----------------------------------------------------------')

        # Enviamos el mensaje resultado
        await context.channel.send(
            'Según recuerdo, tu pene mide {} centímetros, {}'.format(lista[usr], context.author.mention))

    else:
        # Si el usuario no aparece en la lista, nunca ha usado el comando, debemos crear la entrada en la lista

        print('-----------------------------------------------------------')
        print('Comando de penes')
        print("Usuario Nuevo: {}".format(context.author.id))  # Debugging
        print('-----------------------------------------------------------')

        # Creamos un tamaño de pene aleatorio entre 3 y 48 cm
        sze = random.randrange(3, 48)

        # Usamos la función para escribir a la lista el UUID y el tamaño obtenido
        escribir_sizes(server, context.author.id, sze)

        # Enviamos el mensaje
        await context.channel.send(
            'Me imagino que tu pene mide {} centímetros, {}'.format(sze, context.author.mention))


@client.event
async def on_ready():
    """Función de Debugging para el bot, nos confirma que no se explotó esta mondá"""
    print('-----------------------------------------------------------')  # Debugging
    print('Bot conectado satisfactoriamente!')  # Debugging
    print(client.user.name)  # Debugging
    print(client.user.id)  # Debugging
    print('-----------------------------------------------------------')  # debugging


def escribir_sizes(nom_server, usr, tam):
    """Función que añade una entrada a un archivo que es usado como base de datos"""

    # Bloque Try-Catch para asegurarnos que el directorio y el archivo existan
    try:
        bsd = '.\\tamaños_de_pene\\{}.bdp'.format(nom_server)  # Nombre de arch
        f = open(bsd, 'a+')  # Preparar para añadir al archivo
        f.write('{},{}\n'.format(usr, tam))  # Escribir al archivo

        # Para evitar errores, Cerramos esa verga para no editarlo mientras está abierto
        f.close()

    # Si el directorio o el archivo no existen, se crean
    except FileNotFoundError:
        os.makedirs('.\\tamaños_de_pene')

        bsd = '.\\tamaños_de_pene\\{}.bdp'.format(nom_server)  # Nombre de arch
        f = open(bsd, 'w+')  # Preparar para añadir al archivo
        f.write('{},{}\n'.format(usr, tam))  # Escribir al archivo

        # Para evitar errores, Cerramos esa verga para no editarlo mientras está abierto
        f.close()


def obtener_sizes(nom_server):
    """Función que lee un archivo que se usa como base de datos de los tamaños y se
    genera un diccionario a partir de el"""

    # El código debe estar dentro de un bloque Try-Catch, para asegurarnos de que el archivo exista en el directorio
    try:
        """Cabe aclarar, que los archivos tienen un nombre que es igual al GUID del Guild en el que está el bot
        Esto es porque cada Guild tiene una lista de usuarios distinta, esto permite al bot estar en varios 
        Guilds distintos y tener distintas bases de Datos con la lista de usuarios de cada Guild en particular"""

        # Si existe, abrimos el archivo correspondiente
        bsd = open('.\\tamaños_de_pene\\{}.bdp'.format(nom_server), 'r+')

        # Iniciamos con un diccionario vacío
        list_usrs = {}

        # Cada linea del archivo base de datos tiene el formato (UUID,Tamaño), luego cada linea es una entrada
        for linea in bsd:
            spl = linea.split(',')  # Obtenemos el texto de la linea y lo dividimos en una lista de dos posiciones
            list_usrs[spl[0]] = spl[1][0:-1]  # se añade esa entrada al diccionario, obviando el caracter \n

        # Para evitar errores, cerramos el archivo
        bsd.close()
        return list_usrs

    # En caso de que el archivo no exista, quiere decir que nadie nunca ha usado el comando, luego, la lista está vacia
    except FileNotFoundError:
        return {}  # Retornamos un diccionario vacío


def obtener_pajas(nom_server):
    """Función que lee un archivo que se usa como base de datos de la cantidad de pajas y se
    genera un diccionario a partir de el"""

    # El código debe estar dentro de un bloque Try-Catch, para asegurarnos de que el archivo exista en el directorio
    try:
        """Cabe aclarar, que los archivos tienen un nombre que es igual al GUID del Guild en el que está el bot
        Esto es porque cada Guild tiene una lista de usuarios distinta, esto permite al bot estar en varios 
        Guilds distintos y tener distintas bases de Datos con la lista de usuarios de cada Guild en particular"""

        # Si existe, abrimos el archivo correspondiente
        bsd = open('.\\cantidad_pajas\\{}.cdp'.format(nom_server), 'r+')

        # Iniciamos con un diccionario vacío
        list_usrs = {}

        # Cada linea del archivo base de datos tiene el formato (UUID,Tamaño), luego cada linea es una entrada
        for linea in bsd:
            spl = linea.split(',')  # Obtenemos el texto de la linea y lo dividimos en una lista de dos posiciones
            list_usrs[spl[0]] = int(spl[1][0:-1])  # se añade esa entrada al diccionario, obviando el caracter \n

        # Para evitar errores, cerramos el archivo
        bsd.close()
        return list_usrs

    # En caso de que el archivo no exista, quiere decir que nadie nunca ha usado el comando, luego, la lista está vacia
    except FileNotFoundError:
        return {}  # Retornamos un diccionario vacío


def escribir_pajas(nom_server, pajas):
    """Función que genera el archivo que es usado como base de datos para las pajas"""
    """ADVERTENCIA!: Actualmente esto está programado de forma super ineficiente porque
    reescribe el archivo caada vez que se requiera una nueva paja, hasta que se mejore
    esta advertencia seguirá activa"""

    # Bloque Try-Catch para asegurarnos que el directorio y el archivo existan
    try:
        bsd = '.\\cantidad_pajas\\{}.cdp'.format(nom_server)  # Nombre de arch
        f = open(bsd, 'w')  # Preparar para añadir al archivo
        for key in pajas:
            f.write('{},{}\n'.format(key, pajas[key]))  # Escribir al archivo

        # Para evitar errores, Cerramos esa verga para no editarlo mientras está abierto
        f.close()

    # Si el directorio o el archivo no existen, se crean
    except FileNotFoundError:
        os.makedirs('.\\cantidad_pajas')

        bsd = '.\\cantidad_pajas\\{}.cdp'.format(nom_server)  # Nombre de arch
        f = open(bsd, 'w')  # Preparar para añadir al archivo
        for key in pajas:
            f.write('{},{}\n'.format(key, pajas[key]))  # Escribir al archivo

        # Para evitar errores, Cerramos esa verga para no editarlo mientras está abierto
        f.close()


def get_token(particiones):
    """Funcion para descifrar el token a partir de N variables de conf (numero de particiones)"""

    """Esta sección está modificada para usar las config vars de Heroku, el servicio en el que el bot está
    Hosteado, si se desea correr localmente, debes generar tu archivo de environment"""

    print('Preparando el descifrado del token con {} variables...'.format(particiones))
    token = ""  # El token empieza en blanco
    for i in range(particiones):  # Iteramos para el número de particiones
        var = 'TOKEN_{}'.format(i)  # Obtenemos el nombre del archivo que se debe Descifrar
        part = os.environ.get(var, "nepe")  # Obtener la configuración de las config Vars de Heroku
        print('Variable {}: {}'.format(i, part))  # Debugging
        token = token + part  # Leer el texto del archivo y adicionarlo al token completo

    print('Token descifrado: {}'.format(token))
    print('-----------------------------------------------------------')
    return token


TOKEN = get_token(3)

client.run(TOKEN)
