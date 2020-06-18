import os
import random
import discord
from FireHandler import Database

from Scraper import WinrateData, ChampionData, TournamentData
from discord.ext.commands import Bot
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

PREFIX = '/'  # Prefijo para los comandos del bot

client = Bot(command_prefix=PREFIX)  # Crear cliente de bot con el prefijo dado
client.remove_command('help')
database = Database()


def eliminar_penes():
    database.reset_all(393917904506191872)


@tasks.loop(minutes=1)
async def upd_cont_reset():
    """Esta función actualiza el contador de penes cada minuto que pasa, y realiza ciertos eventos cuando el tiempo
    pasa ciertos límites, esto es supremamente ineficiente y debe mejorar, pero está programado a las 3:35 am y ahora
    no tengo ni el tiempo ni la energía para terminar esto"""
    database.reset_countdown(393917904506191872)
    mins = database.get_reset_timer(393917904506191872)  # Actualmente la ID es única, pero esto debe cambiar

    if mins == 1440:  # 1440/60 == 24
        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    await channel.send("Queda 1 día para el reinicio de los penes!")

    elif mins == 720:  # 720/60 == 12
        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    await channel.send("Quedan 12 horas para el reinicio de los penes, @everyone")

    elif mins == 360:  # 360/60 == 6
        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    await channel.send("Quedan 6 horas para el reinicio de los penes!")

    elif mins == 180:  # 180/60 == 3
        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    await channel.send("Quedan 3 horas para el reinicio de los penes!")

    elif mins == 60:  # 60/60 == 1
        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    await channel.send("Queda 1 hora para el reinicio de los penes!")

    elif mins == 10:
        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    await channel.send("Quedan 10 minutos para el reinicio de los penes, @everyone!")

    elif mins == 0:  # Pasó una semana y se deben reiniciar los penes!

        # Iteramos entre todos los canales que tenga disponible el bot
        for channel in client.get_all_channels():

            # Revisamos si cada canal es un canal de texto
            if isinstance(channel, discord.TextChannel):

                # Si lo es, revisamos si tiene el nombre requerido
                if channel.name == 'general':
                    eliminar_penes()
                    print('---------------------------------------------------------------------')
                    print('Se borraron los penes')  # Debugging
                    print('---------------------------------------------------------------------')
                    await channel.send("Los penes han sido eliminados @everyone")


@client.command(name='LEC',
                description='Comando para obtener información de la liga profesional de Europa (LEC)',
                brief='Busca un jugador/equipo europeo',
                aliases=['Lec', 'lec', 'EU', 'eu', 'Eu'],
                usage='/LEC {jugador|equipo} {(Nombre de jugador/equipo)}',
                pass_context=True)
async def eu(context, searchtype, *, query):
    """Función que organiza la información de un jugador de la liga europea"""
    print('---------------------------------------------------------------------')
    print('Comando de EU')  # Debugging

    # Verificamos si el argumento no es nulo
    if searchtype:

        # Verificamos si la persona quiere mirar un jugador específico
        if searchtype.lower() == 'player' or searchtype.lower() == 'jugador':

            # Chiste contra rekkles, si el usuario escribe 'pecho frío' se reemplaza por rekkles
            # Si no, se reemplazan los espacios por underscores
            formatted = 'rekkles' if query == 'pecho frio' else query.replace(' ', '_')
            player = TournamentData(league='LEC', query=formatted)
            stats = player.get_player_stats()

            # Si stats es None, no se encontró el jugador buscado
            if stats:
                pic = player.get_picture()

                print(f"Jugador solicitado: {stats['player_name']}")  # Debugging

                # Obtenemos un markup hypertextual y lo enviamos
                markup = get_player_embed(stats, pic)
                await context.channel.send(content='Aquí tienes la información que encontré', embed=markup)
            else:
                await context.channel.send("Ese jugador no existe en la base de datos, revisa la ortografía o "
                                           "asegurate de que lo buscaste en la liga correcta")
        elif searchtype.lower() == 'equipo' or searchtype.lower() == 'team':
            print('Busqueda por equipos')  # Debugging
            await context.channel.send('Lo siento, aún no puedo buscar equipos :c')

        else:
            print('Referencia inválida')  # Debugging
            await help(context, 'LEC')

    print('---------------------------------------------------------------------')


@client.command(name='LCS',
                description='Comando para obtener información de la liga profesional de NA (LCS)',
                brief='Busca un jugador/equipo Norteamericano',
                aliases=['Lcs', 'lcs', 'NA', 'na', 'Na'],
                usage='/LCS {jugador|equipo} {(Nombre de jugador/equipo)}',
                pass_context=True)
async def na(context, searchtype, *, query):
    """Función que organiza la información de un jugador de la liga europea"""
    print('---------------------------------------------------------------------')
    print('Comando de NA')  # Debugging

    # Verificamos si el argumento no es nulo
    if searchtype:

        # Verificamos si la persona quiere mirar un jugador específico
        if searchtype.lower() == 'player' or searchtype.lower() == 'jugador':

            # Se reemplazan los espacios por underscores
            formatted = query.replace(' ', '_')
            player = TournamentData(league='LCS', query=formatted)
            stats = player.get_player_stats()

            # Si stats == None, no se encontró el jugador
            if stats:
                pic = player.get_picture()

                print(f"Jugador solicitado: {stats['player_name']}")  # Debugging

                # Obtenemos un markup hypertextual y lo enviamos
                markup = get_player_embed(stats, pic)
                await context.channel.send(content='Aquí tienes la información que encontré', embed=markup)

            else:
                await context.channel.send("Ese jugador no existe en la base de datos, revisa la ortografía o "
                                           "asegurate de que lo buscaste en la liga correcta")

        elif searchtype.lower() == 'equipo' or searchtype.lower() == 'team':
            print('Busqueda por equipos')  # Debugging
            await context.channel.send('Lo siento, aún no puedo buscar equipos :c')

        else:
            print('Referencia inválida')  # Debugging
            await help(context, 'LEC')

    print('---------------------------------------------------------------------')


@client.command(name='help',
                description='Comando para recibir ayuda del bot, o de un comando específico',
                brief='Recibe ayuda del bot!',
                aliases=['Help', 'h', 'ayuda', 'Ayuda', 'AYUDA'],
                usage='/help {comando (opcional)}',
                pass_context=True)
async def help(context, *args):
    """Comando que entraga un mensaje de ayuda"""
    print('---------------------------------------------------------------------')
    print('Comando de ayuda')  # Debugging
    all_commands = client.all_commands

    if len(args) == 0:  # Si no recibió ningún argumento y nada más quiere ver la ayuda general

        print('Ayuda general')  # Debugging

        # Usamos un ciclo para obtener todos los nombres únicos de los comandos
        command_names = []
        for command in all_commands:
            if command_names.count(all_commands[command].name) == 0:
                command_names.append(all_commands[command].name)

        # Formamos un embed para enviar
        markup = discord.Embed(title='Comandos', description='Todos los comandos que este bot puede realizar!')

        # Por cada comando, ponemos un campo en el embed
        for command in command_names:
            markup.add_field(name=f'/{command}', value=all_commands[command].description, inline=False)

        # Enviamos el embed
        await context.channel.send(content=None, embed=markup)

    elif len(args) == 1:  # Si el usuario necesita información sobre un comando específico, envió /help {comando}

        print(f'Ayuda con comando {args[0]}')

        # Verificamos si el comando existe
        if args[0] in all_commands:
            markup = discord.Embed(title=f'/{args[0]}')
            markup.add_field(name='Descripción', value=all_commands[args[0]].description)
            markup.add_field(name='Uso adecuado', value=all_commands[args[0]].usage)

            await context.channel.send(embed=markup, content=None)
        else:
            print('Comando inexistente')
            await context.channel.send('Malparido, ese comando no existe, así que te lo puedes meter por el asterisco')

    else:
        print('Sintáxis inválida, mostrando ayuda de ayuda')
        await help(context, help)

    print('---------------------------------------------------------------------')


@client.command(name='reset',
                description='Comando para saber cuanto falta para el reinicio de los penes',
                brief='Obtén el tiempo que falta para reset de la tierlist',
                aliases=['Reset', 'RESET'],
                usage='/reset',
                pass_context=True)
async def get_reset(context):
    # Obtenemos la información del tiempo de reinicio de Firebase
    mins_reinicio = database.get_reset_timer(context.guild.id)

    print('---------------------------------------------------------------------')
    print('Comando de Reset')  # Debugging
    print(f'Tiempo restatnte (mins): {mins_reinicio}')
    print('---------------------------------------------------------------------')
    # La pasamos al server
    await context.channel.send(f"Aún quedan {mins_reinicio // 60} horas, {mins_reinicio % 60} minutos para reiniciar")


@client.command(name='winrate',
                description='Comando que te deja saber el winrate de un campeón en una posición específica',
                brief='Obten un winrate específico',
                aliases=['Winrate', 'WINRATE', 'wr', 'Wr', 'WR'],
                usage='/winrate {campeón} {línea}',
                pass_context=True)
async def get_winrate(context, *args):
    """Función que obtiene un winrate de una linea o un campeón específico"""
    print('---------------------------------------------------------------------')
    lineas_validas = {
        'top': 'top',
        'jungle': 'jungle',
        'jungla': 'jungle',
        'mid': 'mid',
        'medio': 'mid',
        'middle': 'mid',
        'bot': 'adc',
        'adc': 'adc',
        'carry': 'adc',
        'sup': 'support',
        'support': 'support',
        'soporte': 'support'
    }

    if len(args) == 2:  # Si el usuario ingresó campeón + linea
        if args[1] in lineas_validas:
            winrate_scraper = WinrateData(champ=args[0], lane=[lineas_validas[args[1]]])
            stats = winrate_scraper.get_champ_stats()
            if stats:
                print(f'Winrate de {args[0]} de {lineas_validas[args[1]]}')
                markup = discord.Embed(
                    title=f'Winrate de {args[0].capitalize()} en {lineas_validas[args[1]].capitalize()}',
                    description='Información obtenida de op.gg'
                )
                markup.set_footer(text=stats['patch info'])
                markup.set_thumbnail(url=winrate_scraper.get_champ_icon())
                markup.add_field(name='Winrate', value=stats['winrate'], inline=True)
                markup.add_field(name='Playrate', value=stats['playrate'], inline=True)

                await context.channel.send(content=None, embed=markup)
                print(stats)
            else:
                print(f'El campeón {args[0]} no existe!')
                markup = discord.Embed(
                    title=f'Winrate de {args[0].capitalize()} en {lineas_validas[args[1]].capitalize()}',
                    description='Información obtenida de op.gg'
                )
                markup.add_field(name=f'El campeón {args[0].capitalize()} no existe',
                                 value='Así que te lo puedes meter por el asterisco')
        else:
            lineas = discord.Embed(title='Líneas válidas', description='Eres un imbécil')
            lineas.add_field(name='Puedes usar cualquiera de los siguientes valores para la linea: ',
                             value='\n'.join(lineas_validas.keys()))
            await context.channel.send("Balurdo ignorante, esas linea no es válida", embed=lineas)
    else:
        print("Comando de winrate, parametros inválidos")
        ayuda = discord.Embed(title='Ayuda de comando')
        ayuda.add_field(name='Para saber el winrate de un campeón en una linea específica',
                        value='/wr {Nombre de campeón} {Linea}')
        await context.channel.send("Eu, tu maldita madre, eres un incompetente, esa vaina está mal", embed=ayuda)
    print('---------------------------------------------------------------------')


@client.command(name='runas',
                description='Comando que te muestra las runas recomendadas de algún campeón de LoL',
                brief='Obtén las runas de un campeón!',
                aliases=['Runas', 'runes', 'Runes', 'RUNAS', 'RUNES'],
                usage='/runas {campeón}',
                pass_context=True)
async def get_builds(context, champ):
    print('---------------------------------------------------------------------')
    print('Comando de builds')  # Debugging
    print(f'Campeón seleccionado: {champ}')

    # Diccionario para hacer cadenas lindas
    noms = {
        1: f'Runas más comunes de {champ}',
        2: f'Runas con mayor winrate de {champ}'
    }

    # Creamos el objeto campeón para buscar la info
    champion = ChampionData(champ.lower())
    champ = champion.get_champ_name()
    # Usamos la funcion de ChampionData para obtener las runas y procesarlas
    runes = champion.runes

    # Verificamos si consiguió los datos
    if runes:
        markup = discord.Embed(title=f"Runas indicadas para {champ}", description="Obtenido de Champion.gg")
        markup.set_thumbnail(url=champion.get_champ_icon())
        for runeset in runes:
            if runeset == 1:
                markup.add_field(name=noms[1], value="-------------------------------------", inline=False)
            else:
                markup.add_field(name=noms[2], value=" ------------------------------------", inline=False)
            tree = runes[runeset]
            for path in tree:
                path_title = path[0]
                selecciones = '\n'.join(path[1])
                markup.add_field(name=path_title, value=selecciones, inline=True)

        markup.set_footer(text=f'Parche {champion.get_patch()}')
        await context.channel.send(content=None, embed=markup)
        print("Información enviada exitosamente")
        print('---------------------------------------------------------------------')
    else:
        await context.channel.send("Buena imbécil, escribiste mal el nombre del campeón, aprende a escribir")
        print("Campeón no existe")
        print('---------------------------------------------------------------------')


@client.command(name='build',
                description='Comando que te muestra las builds recomendadas de algún campeón de LoL',
                brief='Obtén la build de un campeón!',
                aliases=['Build', 'builds', 'BUILD', 'Builds', 'BUILDS'],
                usage='/build {campeón}',
                pass_context=True)
async def get_builds(context, champ):
    """Con esta funcion se obtienen las builds del scraper, y se entregan al usuario"""

    print('---------------------------------------------------------------------')
    print('Comando de builds')  # Debugging
    print(f'Campeón seleccionado: {champ}')

    # Creamos el objeto que contiene los datos del champ que se requiera
    champion_data = ChampionData(champ.lower())
    champ = champion_data.get_champ_name()

    # Tenemos un diccionario para relacionar cada build a un título y una cadena bien formada
    noms = {
        1: f'Build completa más común de {champ}',
        2: f'Build completa con mayor winrate de {champ}',
        3: f'Iniciales más comunes de {champ}',
        4: f'Iniciales con mayor winrate de {champ}'
    }

    # De este objeto, obtenemos la info de las builds
    build_data = champion_data.builds
    if build_data:  # Verificamos que hayamos conseguido los datos
        markup = discord.Embed(title=f"Items indicados para {champ}", description="Obtenido de Champion.gg")
        markup.set_thumbnail(url=champion_data.get_champ_icon())

        for build in build_data:
            itemlist = build_data[build]
            if itemlist:
                itemlist_markup = '\n'.join(itemlist)
            else:
                itemlist_markup = 'No hay una build aún para este campeón, intentalo más tarde :('

            # Odio discord.py
            # Los items inline se mostrarán en la misma linea, deben estar juntos
            if build > 2:  # Si vamos por los items iniciales, deben ir inline para que sea más entendible
                markup.add_field(name=noms[build], value=itemlist_markup, inline=True)

            else:  # Los primeros dos campos no van inline, tienen demasiada info
                markup.add_field(name=noms[build], value=itemlist_markup, inline=False)
        markup.set_footer(text=f'Parche {champion_data.get_patch()}')
        await context.channel.send(content=None, embed=markup)
        print("Información enviada exitosamente")
        print('---------------------------------------------------------------------')
    # Si no se consiguieron los datos, hay que avisar que el man es imbécil y escribió algo mal
    else:
        await context.channel.send("Buena imbécil, escribiste mal el nombre del campeón, aprende a escribir")
        print("Campeón no existe")
        print('---------------------------------------------------------------------')


# Comando Tierlist para dar la lista de tamaños de penes
@client.command(name='listapene',
                description='Comando que muestra una tierlist de penes, los mas grandes primero',
                brief='El bot te otorga un tamaño de pene!',
                aliases=['penetierlist', 'penetl'],
                usage='/listapene',
                pass_context=True)
async def tierlist(context):
    """Función que obtiene la lista de tamaños de penes, la organiza, y la envía"""
    server = context.guild
    lista = obtener_lista_penes(server.id)
    print('---------------------------------------------------------------------')
    print('Comando de tierlist de penes')  # Debugging

    # Ordenamos el diccionario por valor, de forma descendente
    lista_ordenada = sorted(lista.items(), key=lambda x: x[1], reverse=True)

    # Obtener diccionario que relacione nombres de usuario con su UUID
    rels = {}
    for user in server.members:
        if str(user.id) in lista:
            rels[str(user.id)] = user.mention

    # Mensaje enbebido
    markup = discord.Embed(title="Tierlist de penes!")

    # Iniciamos un contador externo para llevar las posiciones
    cont = 1

    #
    for entry in lista_ordenada:
        print(f'Posición: {cont}, Usuario: {entry[0]}, Tamaño: {entry[1]}')
        markup.add_field(name=f'{cont}°, con {entry[1]} cm', value=rels[entry[0]], inline=False)
        cont += 1

    print('---------------------------------------------------------------------')  # Debugging
    await context.channel.send(content=None, embed=markup)


# Comando Tierlist para dar la lista de tamaños de penes
@client.command(name='listapajas',
                description='Comando que muestra un ranking de los mas pajeros del servidor',
                brief='El bot te otorga un tamaño de pene!',
                aliases=['pajatierlist', 'pajatl'],
                usage='/listapajas',
                pass_context=True)
async def tierlist(context):
    """Función que obtiene la lista de cantidad de pajas, la organiza, y la envía"""
    server = context.guild
    lista = obtener_lista_pajas(server.id)
    print('---------------------------------------------------------------------')
    print('Comando de tierlist de pajas')  # Debugging

    # Ordenamos el diccionario por valor, de forma descendente
    lista_ordenada = sorted(lista.items(), key=lambda x: x[1], reverse=True)  # Retorna lista de tuplas ordenadas

    # Obtener diccionario que relacione nombres de usuario con su UUID
    rels = {}
    for user in server.members:
        if str(user.id) in lista:
            rels[str(user.id)] = user.mention

    # Mensaje enbebido
    markup = discord.Embed(title="Tierlist de pajas!")

    # Iniciamos un contador externo para llevar las posiciones
    cont = 1

    # Añadir los campos al mensaje embebido
    for entry in lista_ordenada:
        print(f'Posición: {cont}, Usuario: {entry[0]}, Pajas: {entry[1]}')
        markup.add_field(name=f'{cont}°, con {entry[1]} pajas', value=rels[entry[0]], inline=False)
        cont += 1

    print('---------------------------------------------------------------------')  # Debugging
    await context.channel.send(content=None, embed=markup)


# Comando cuentapajas para contar el total de pajas del servidor
@client.command(name='cuentapajas',
                description='Comando que muestra la cuenta total de pajas de todos los usuarios del servidor',
                brief='El bot te cuenta las pajas!',
                aliases=['CUENTAPAJAS', 'Cuentapajas'],
                usage='/cuentapajas',
                pass_context=True)
async def get_pajas(context):
    """Método que recorre toda la lista de pajas y suma las pajas de todos los que hayan usado el comando"""
    total = 0  # El número mínimo posible es 0

    # Usando el método para obtener diccionario de pajas
    lista = obtener_lista_pajas(context.guild.id)

    # Iteramos por las llaves del diccionario
    for persona in lista:
        total += int(lista[persona])  # Por cada persona, tomamos sus pajas y las sumamos al total

    await context.channel.send(f'El servidor en conjunto lleva un gran total de {total} pajas')


@commands.cooldown(1, 5, commands.BucketType.user)  # Fue necesario implementar un cooldown (Gracias Miguel)
@client.command(name='paja',
                description='Comando que añade una paja a tu cuenta de pajas en el servidor',
                brief='El bot te cuenta las pajas!',
                aliases=['pajas', 'PAJAS', 'PAJA', 'pajazo', 'PAJAZO'],
                usage='/paja',
                pass_context=True)
async def add_paja(context):
    usr = str(context.author.id)  # El ID único del usuario que usa el comando
    # Debe ser el ID porque el Username puede cambiar (Y lo hace frecuentemente)

    server = context.guild.id  # El ID único del servidor en el que se ejecuta el comando
    # Debe ser el ID porque el Guildname puede cambiar (Y lo hace frecuentemente)

    pajas = obtener_pajas(server, usr)  # obtiene un diccionario de la forma {(UUID): (UU Pajas)}

    if pajas:
        print('---------------------------------------------------------------------')
        print('Comando de pajas')
        print(f"Usuario existente: {usr}")  # Debugging
        print(f"Pajas de usuario: {pajas + 1}")
        print('---------------------------------------------------------------------')

        # Incrementamos las pajas en 1 y amendamos el archivo de pajas
        agregar_paja(server, usr)

        # Le hacemos saber al usuario cuantas pajas lleva
        await context.channel.send('Llevas {} pajas, {}!'.format(pajas + 1, context.author.mention))

    else:
        # Si el usuario no aparece en la lista, nunca ha usado el comando, debemos crear la entrada en la lista
        print('---------------------------------------------------------------------')
        print('Comando de pajas')
        print("Usuario Nuevo: {}".format(context.author.id))  # Debugging
        print('---------------------------------------------------------------------')

        # Incrementamos las pajas en 1 y amendamos el archivo de pajas
        agregar_paja(server, usr)

        # Le hacemos saber al usuario cuantas pajas lleva
        await context.channel.send(f'Llevas {1} paja, {context.author.mention}!')


# Comando para pedir el tamaño del nepe
@client.command(name='pene',
                description='Comando te otorga un tamaño de pene si no lo tienes, o te lo recuerda, si lo tienes',
                brief='El bot te otorga un tamaño de pene!',
                usage='/pene',
                aliases=['penecito', 'penesito', 'penezote', 'penesote'],

                pass_context=True)
async def penecito(context):
    """Función que obtiene el tamaño de la lista de penes del servidor"""
    usr = str(context.author.id)  # El ID único del usuario que usa el comando
    # Debe ser el ID porque el Username puede cambiar (Y lo hace frecuentemente)

    server = context.guild.id  # El ID único del servidor en el que se ejecuta el comando
    # Debe ser el ID porque el Guildname puede cambiar (Y lo hace frecuentemente)

    tam = obtener_size(server, usr)  # obtiene un diccionario de la forma {(UUID): (UU Size)}

    if tam:  # Buscamos si el usuario ya tiene un tamaño de pene registrado
        # Si ya ha usado el comando antes, debemos buscar el nombre en la lista

        print('---------------------------------------------------------------------')
        print('Comando de pene')
        print("Usuario existente: {}".format(context.author.id))  # Debugging
        print("Tamaño de usuario: {}".format(tam))
        print('---------------------------------------------------------------------')

        # Enviamos el mensaje resultado
        await context.channel.send(
            f'Según recuerdo, tu pene mide {tam} centímetros, {context.author.mention}')

    else:
        # Si el usuario no aparece en la lista, nunca ha usado el comando, debemos crear la entrada en la lista

        print('---------------------------------------------------------------------')
        print('Comando de penes')
        print("Usuario Nuevo: {}".format(context.author.id))  # Debugging
        print('---------------------------------------------------------------------')

        # Creamos un tamaño de pene aleatorio entre 3 y 48 cm
        sze = random.randrange(3, 48)

        # Usamos la función para escribir a la lista el UUID y el tamaño obtenido
        escribir_size(server, context.author.id, sze)

        # Enviamos el mensaje
        await context.channel.send(
            'Me imagino que tu pene mide {} centímetros, {}'.format(sze, context.author.mention))


# Manejo de errores
@eu.error
async def eu_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Careverga, esa vaina no se usa así")
        await help(ctx, 'LEC')


@na.error
async def na_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Careverga, esa vaina no se usa así")
        await help(ctx, 'LEC')


@add_paja.error
async def paja_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if ctx.message.author.id == 261303165150953472:  # Si es Miguel
            client.get_command('paja').reset_cooldown(ctx)
            await ctx.channel.send(content='Si te vas a poner con tu perro spam, puedes comer mierda, '
                                           'y te va a tocar esperar',
                                   embed=discord.Embed(title='Tiempo para siguiente paja',
                                                       description=f'{str(error.retry_after)} segundos'
                                                       )
                                   )
        else:
            await ctx.channel.send(content='Malparido ansiado de mierda, aguanta un poquito, se te va a caer la verga '
                                           'hijo de tu mil puta madre',
                                   embed=discord.Embed(title='Tiempo para siguiente paja',
                                                       description=f'{str(error.retry_after)} segundos'
                                                       )
                                   )


# Eventos
@client.event
async def on_ready():
    """Función de Debugging para el bot, nos confirma que no se explotó esta mondá"""
    print('---------------------------------------------------------------------')  # Debugging
    print('Bot conectado satisfactoriamente!')  # Debugging
    print(client.user.name)  # Debugging
    print(client.user.id)  # Debugging
    print('---------------------------------------------------------------------')  # debugging


def get_player_embed(stats: dict, pic: str):
    # Crear el embed
    markup = discord.Embed(title="Información de jugador")
    markup.set_thumbnail(url=pic)
    markup.set_footer(text='Información de: lol.gamepedia.com')

    # Añadir los campos
    markup.add_field(name='Nombre de Jugador', value=stats['player_name'], inline=False)
    markup.add_field(name='Equipo', value=stats['team_name'], inline=False)
    markup.add_field(name='N° de partidos jugados', value=stats['games_played'], inline=True)
    markup.add_field(name='Victorias', value=stats['wins'], inline=True)
    markup.add_field(name='Derrotas', value=stats['losses'], inline=True)
    markup.add_field(name='Asesinatos promedio por partida', value=stats['k/game'], inline=True)
    markup.add_field(name='Muertes promedio por partida', value=stats['d/game'], inline=True)
    markup.add_field(name='Asistencias promedio por partida', value=stats['a/game'], inline=True)
    markup.add_field(name='KDA promedio', value=stats['kda'], inline=False)
    markup.add_field(name='Oro promedio por partido', value=stats['gold/game'], inline=True)
    markup.add_field(name='Oro promedio por minuto', value=stats['gold/min'], inline=True)
    markup.add_field(name='% de oro promedio', value=stats['gold_share'], inline=True)
    markup.add_field(name='CS/Partido Promedio', value=stats['cs/game'], inline=True)
    markup.add_field(name='CS/Minuto Promedio', value=stats['cs/min'], inline=True)
    markup.add_field(name='Participación en asesinatos promedio', value=stats['kill_part'], inline=False)
    markup.add_field(name='% de asesinatos promedio', value=stats['kill_share'], inline=True)
    markup.add_field(name='Campeones jugados', value='\n'.join(stats['champs_played']), inline=False)

    return markup


def escribir_size(server, usr, tam):
    """Función que añade una entrada a una base da datos de los tamaños de penes de los usuarios"""

    database.set_pene(server, usr, tam)


def obtener_size(nom_server, uuid):
    """Función que lee un archivo que se usa como base de datos de los tamaños y se
    genera un diccionario a partir de el"""

    return database.get_pene(nom_server, uuid)


def obtener_pajas(nom_server, uuid):
    """Funcion que retorna el resultado btenido de la base de datos de pajas"""

    return database.get_pajas(nom_server, uuid)


def obtener_lista_pajas(nom_server):
    return database.get_all_pajas(nom_server)


def obtener_lista_penes(nom_server):
    return database.get_all_penes(nom_server)


def agregar_paja(nom_server, uuid):
    """Función que genera el archivo que es usado como base de datos para las pajas"""

    database.add_paja(nom_server, uuid)


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
    print('---------------------------------------------------------------------')
    return token


TOKEN = get_token(3)
upd_cont_reset.start()

client.run(TOKEN)
