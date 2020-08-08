import os
import random
from math import pow

import discord
import math
import Scraper as miner
import Economia
import Casino
import asyncio

from FireHandler import Database
from discord.ext.commands import Bot
from discord.ext import tasks, commands
from dotenv import load_dotenv
# from StockMarket import StockMarket
from Farm import Farm

load_dotenv()

PREFIX = '/'  # Prefijo para los comandos del bot

client = Bot(command_prefix=PREFIX)  # Crear cliente de bot con el prefijo dado
client.remove_command('help')
print('---------------------------------------------------------------------')
print("Inicializando módulo: Pyrebase Database administrator...")
database = Database()
print("Módulo: Pyrebase Database administrator Inicializado con éxito")
print('---------------------------------------------------------------------')
print('---------------------------------------------------------------------')
print("Inicializando módulo: Penetienda...")
tienda = Economia.Tienda()
print("Módulo: Penetienda Inicializado con éxito")
print('---------------------------------------------------------------------')
print('---------------------------------------------------------------------')
print("Inicializando módulo: PeneAcciones...")
# stock_market = StockMarket(database)
print('---------------------------------------------------------------------')
print('---------------------------------------------------------------------')
farm_module = Farm(database)
print('---------------------------------------------------------------------')
print('---------------------------------------------------------------------')

ansiados = {}

compras_actuales = {}
using_item = {}
confirmation = {}
target_selection = {}
betting = {}
blackjack_games = {}
buying_stock = {}
upgrading_farm = {}


def eliminar_penes(guild_id):
    database.reset_all(guild_id)

"""@tasks.loop(minutes=10)
async def cont_stocks():
    Función para administrar el temporizador del mercadod e acciones, esta función se asegura que cada
    media hora se hace una actualización de los datos

    for guild in client.guilds:

        timer = database.countdown_stock_timer(guild.id)

        if timer == 0:
            stock_market.advance_rng(guild.id)
"""

@tasks.loop(hours=1)
async def farm_rewards():
    for guild in client.guilds:
        guild_users = database.get_all_users_uuid(guild.id)
        for uuid in guild_users:
            farm = farm_module.get_farm(guild.id, uuid)

            points = farm['points']
            modifier = farm['upgrades']['Mejora de PeneIngresos']

            database.give_penecreditos(guild.id, uuid, int(points*(modifier/4)))


@tasks.loop(minutes=5)
async def upd_cont_reset():
    """Esta función actualiza el contador de penes cada minuto que pasa, y realiza ciertos eventos cuando el tiempo
    pasa ciertos límites, esto es supremamente ineficiente y debe mejorar, pero está programado a las 3:35 am y ahora
    no tengo ni el tiempo ni la energía para terminar esto"""
    for guild in client.guilds:
        database.reset_countdown(guild.id)
        mins = database.get_reset_timer(guild.id)  # Actualmente la ID es única, pero esto debe cambiar

        if mins == 1440:  # 1440/60 == 24
            # Iteramos entre todos los canales que tenga disponible el bot
            for channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if channel.name == 'general':
                        await channel.send("Queda 1 día para el reinicio de los penes!")

        elif mins == 720:  # 720/60 == 12
            # Iteramos entre todos los canales que tenga disponible el bot
            for channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if channel.name == 'general':
                        await channel.send("Quedan 12 horas para el reinicio de los penes, @everyone")

        elif mins == 360:  # 360/60 == 6
            # Iteramos entre todos los canales que tenga disponible el bot
            for channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if channel.name == 'general':
                        await channel.send("Quedan 6 horas para el reinicio de los penes!")

        elif mins == 180:  # 180/60 == 3
            # Iteramos entre todos los canales que tenga disponible el bot
            for channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if channel.name == 'general':
                        await channel.send("Quedan 3 horas para el reinicio de los penes!")

        elif mins == 60:  # 60/60 == 1
            # Iteramos entre todos los canales que tenga disponible el bot
            for channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if channel.name == 'general':
                        await channel.send("Queda 1 hora para el reinicio de los penes!")

        elif mins == 10:
            # Iteramos entre todos los canales que tenga disponible el bot
            for guild_channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(guild_channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if guild_channel.name == 'general':
                        channel = guild_channel
                        break

            await guild_channel.send("Quedan 10 minutos para el reinicio de los penes, Recuerden que los"
                                     " que estén en la cima de la tabla recibirán premios @everyone!")

        elif mins == 0:  # Pasó una semana y se deben reiniciar los penes!

            # Además de que se reinician los penes, también debemos otorgar los PeneCréditos a los ganadores
            ganancias = discord.Embed(title="Felicidades a los ganadores!")

            # Otorgamos PeneCréditos a los admins
            for admin in database.get_admins(guild.id):
                database.give_penecreditos(393917904506191872, admin, 120)
                user = await client.fetch_user(admin)
                ganancias.add_field(name="Ganador por ser admin! (+120 PC)", value=user.mention, inline=False)

            # Otorgamos PeneCréditos a los más pajilleros
            ganadores_paja = database.get_all_pajas(guild.id)

            for pajero in ganadores_paja:
                database.give_penecreditos(guild.id, pajero, int(2.5 * ganadores_paja[pajero]))
                user = await client.fetch_user(pajero)
                ganancias.add_field(name=f"Ganador por pajillero (+{int(2.5 * ganadores_paja[pajero])}PC)",
                                    value=user.mention,
                                    inline=False)

            # Iteramos entre todos los canales que tenga disponible el bot
            for channel in guild.channels:

                # Revisamos si cada canal es un canal de texto
                if isinstance(channel, discord.TextChannel):

                    # Si lo es, revisamos si tiene el nombre requerido
                    if channel.name == 'general':
                        eliminar_penes(guild.id)
                        print('---------------------------------------------------------------------')
                        print('Se borraron los penes')  # Debugging
                        print('---------------------------------------------------------------------')
                        await channel.send("Los penes han sido eliminados @everyone", embed=ganancias)

                        break


@commands.cooldown(1, 120, commands.BucketType.user)
@client.command(name="penebusqueda",
                usage='/penebúsqueda',
                description='Comando para explorar el mundo y encontrar animales para la PeneGranja™',
                brief='Añade animales a tu PeneGranja™!',
                aliases=['pb', 'PB', 'peneb', 'Peneb'],
                pass_context=True)
async def penebusqueda(ctx):

    if database.get_penecreditos(ctx.guild.id, ctx.author.id) >= 1:
        database.consume_pc(ctx.guild.id, ctx.author.id, 1)

        hunt = farm_module.wild_hunt(ctx.guild.id, ctx.author.id)

        anuncio = discord.Embed(title=f"{ctx.author.name} ha gastado 1 pc y ha salido a explorar!")

        found_animal = random.choice(list(hunt[1].keys()))

        farm_module.grant_animal(ctx.guild.id, ctx.author.id, hunt[0], found_animal, 1)

        anuncio.add_field(name=f"{ctx.author.name} ha encontrado un animal de clase {farm_module.rarities[hunt[0]]}",
                          value=f"Animal encontrado: {farm_module.get_emoji(hunt[0], found_animal)}")

        await ctx.send(embed=anuncio)

    else:
        await ctx.send(f"No tienes suficientes Penecréditos para salir a explorar {ctx.author.mention}!")


@client.command(name="penegranja",
                usage='/penegranja {ver(v)|mejorar(m)}',
                description='Comando para explorar tu PeneGranja™',
                brief='Revisa o mejora tu PeneGranja™!',
                aliases=['pg', 'pichagorda', 'Pg', 'PG', 'peneg', 'Peneg'],
                pass_context=True)
async def penegranja(ctx, opt: str = 'ver'):

    print('---------------------------------------------------------------------')
    print("Comando de Penegranja")
    async with ctx.typing():

        granja = farm_module.get_farm(ctx.guild.id, ctx.author.id)

        if opt.lower() == 'ver' or opt.lower() == 'v':
            farm_embed = discord.Embed(title=f':man_farmer: Granja de {ctx.author.name}')
            superscript = {
                '1': '¹',
                '2': '²',
                '3': '³',
                '4': '⁴',
                '5': '⁵',
                '6': '⁶',
                '7': '⁷',
                '8': '⁸',
                '9': '⁹',
                '0': '⁰'
            }
            for rarity, animals in granja['animals'].items():

                string = f"{farm_module.rarities[rarity]}: "
                for animal in animals:
                    string += f"{farm_module.get_emoji(rarity, animal)}" \
                              f"{''.join([superscript[num] for num in str(animals[animal])])}"
                    string += f"{''.join([' ' for _ in range(4-len(str(animals[animal])))])}"

                for _ in range(farm_module.get_species_amount(rarity) - len(animals)):
                    string += ':question:⁰⁰'
                    string += "  "

                farm_embed.add_field(name=string, value='\u200b', inline=False)

            farm_embed.add_field(name=f"Puntos de Granja: {granja['points']}",
                                 value=f"Genera {granja['points']*(granja['upgrades']['Mejora de PeneIngresos']/4)} PC/h")

            farm_embed.add_field(name="Mejoras:", value="\u200b", inline=False)

            for upgrade, lvl in granja['upgrades'].items():
                lvl_string = ''
                for x in range(5):
                    if x+1 > lvl:
                        lvl_string += ':white_small_square: '

                    else:
                        lvl_string += f'{farm_module.upgrades[upgrade]} '

                farm_embed.add_field(name=upgrade, value=lvl_string, inline=False)

            await ctx.send(embed=farm_embed)

        elif opt.lower() == 'mejorar' or opt.lower() == 'm':
            farm_embed = discord.Embed(title=f':man_farmer: Granja de {ctx.author.name}')

            for upgrade, lvl in granja['upgrades'].items():
                lvl_string = ''
                for x in range(5):
                    if x+1 > lvl:
                        lvl_string += ':white_small_square: '

                    else:
                        lvl_string += f'{farm_module.upgrades[upgrade]} '

                farm_embed.add_field(name=f"{upgrade}", value=lvl_string, inline=False)

            emojis = []

            for upgrade, lvl in granja['upgrades'].items():
                if lvl < 5:
                    farm_embed.add_field(name=f"{farm_module.upgrades[upgrade]}: Mejorar {upgrade}", value=f"Costo: {pow(10, lvl)} PC",
                                         inline=False)
                    emojis.append(True)

                else:
                    emojis.append(True)

            msg = await ctx.send(embed=farm_embed)

            reactions = ["🧯", "💰", "🌱", "🌊", "☢️"]

            for x in range(len(reactions)):
                if emojis[x]:
                    await msg.add_reaction(reactions[x])

            await msg.add_reaction('❌')

            upgrading_farm[msg.id] = ctx.author.id


"""@client.command(name="penemercado",
                usage='/penemercado {comprar|vender|ver} {Symbolo de Accion} {cantidad}',
                pass_context=True)"""
async def penemercado(ctx: commands.Context, action='ver', stock=None, amount=None):
    valid_actions = ['ver', 'comprar', 'vender', 'watch', 'buy', 'sell', 'w', 'b', 's']

    query_embed = discord.Embed()

    async with ctx.typing():
        if action.lower() in valid_actions:
            if action.lower() == 'ver' or action.lower() == 'w':

                if stock is None:
                    query_embed.title = "Aquí están todas las acciones del mercado!"
                    query_embed.description = "Tiempo para cambio de precios: " \
                                              f"{stock_market.get_stock_timer(ctx.guild.id)} minutos"

                    for stock in stock_market.get_available_stocks(ctx.guild.id):

                        stock_info = stock_market.get_stock_info(ctx.guild.id, stock)

                        if stock_info['last change'] < 0:
                            query_embed.add_field(name=f"{stock_info['name']}({stock})",
                                                  value=f"📉 {stock_info['last change']}%", inline=False)

                        else:
                            query_embed.add_field(name=f"{stock_info['name']}({stock})",
                                                  value=f"📈 {stock_info['last change']}", inline=False)

                    await ctx.send(embed=query_embed)


@client.command(name="peneblackjack",
                description='Comando para jugar blackjack',
                brief='Juega blackjack en el PeneCasino™!',
                aliases=['Peneblackjack', 'pbj', 'PBJ', 'PENEBLACKJACK', 'PeneBlackJack', 'penebj', 'Penebj'],
                usage='/peneblackjack',
                pass_context=True)
async def blackjack(ctx):
    if ctx.author.id not in blackjack_games:
        # Obtener PC del usuario
        user_pc = database.get_penecreditos(ctx.guild.id, ctx.author.id)

        # Generamos el menú de apuestas
        bet_menu = discord.Embed(title="Bienvenido al PeneCasino™! Juego: PeneBlackjack™/Pénis-Vingt-et-Un™",
                                 description=f"Decide cuanto apostarás. Tienes {user_pc} PeneCréditos™")

        # Añadimos todas las opciones
        bet_menu.add_field(name=":one: : 1 PeneCréditos™",
                           value="O eres un Pussy, o estás pobre, de ambas formas vales pito",
                           inline=False)
        bet_menu.add_field(name=":two: : 5 PeneCréditos™",
                           value="Al menos ya te vas bajando del bus",
                           inline=False)
        bet_menu.add_field(name=":three: : 10 PeneCréditos™",
                           value="Ahora si papi",
                           inline=False)
        bet_menu.add_field(name=":four: : 25 PeneCréditos™",
                           value="El que no arriesga, no gana",
                           inline=False)
        bet_menu.add_field(name=":five: : 50 PeneCréditos™",
                           value="Que belcebú proteja tu billetera",
                           inline=False)
        bet_menu.add_field(name=":six: : 100 PeneCréditos™",
                           value="Confirmo que no tomas buenas decisiones",
                           inline=False)
        bet_menu.add_field(name=":seven: : 250 PeneCréditos™",
                           value="weird flex but ok",
                           inline=False)

        menu: discord.Message = await ctx.send(embed=bet_menu)

        await menu.add_reaction('1️⃣')
        await menu.add_reaction('2️⃣')
        await menu.add_reaction('3️⃣')
        await menu.add_reaction('4️⃣')
        await menu.add_reaction('5️⃣')
        await menu.add_reaction('6️⃣')
        await menu.add_reaction('7️⃣')
        await menu.add_reaction('❌')

        betting[menu.id] = ctx.author.id

    else:
        await ctx.send("Ya tienes una partida de PeneBlackjack™ activa, terminala para comenzar una nueva!")


@client.command(name='usaritem',
                description='Comando para usar alguno de los items en tu inventario',
                brief='Usa un item!',
                aliases=['Usar', 'Usaritem', 'USAR', 'UsarItem', 'USARITEM'],
                usage='/usaritem',
                pass_context=True)
async def use(ctx):
    # Debugging
    print('---------------------------------------------------------------------')
    print('Comando de usar item')
    print(f"Usuario que lo solicita: {ctx.author}")

    # Obtenemos el inventario del usuario
    inv = database.get_inventory(ctx.message.guild.id, ctx.author.id)

    # Más debugging
    print(f"inventario de {ctx.author}: {dict(inv)}")

    # Creamos el embed que contendrá la información del usuario
    inventory_embed = discord.Embed(title="Aquí tienes tu inventario, elige el item que quieres usar")

    # Si el usuario tiene al menos 1 item
    if inv != {}:

        # Ponemos todos los items en el embed
        cont = 1
        for item in inv:
            inventory_embed.add_field(name=f"{cont}️⃣: {item}", value=f"Tienes: {inv[item]}", inline=False)
            cont += 1

        # Enviamos el mensaje que contiene el menú
        msg = await ctx.send(embed=inventory_embed)

        # Insertamos los botones que funcionarán como reacciones
        for x in range(1, len(inv) + 1):
            await msg.add_reaction(f'{x}️⃣')

        # Insertamos un botón de cancelar
        await msg.add_reaction('❌')

        # Metemos al usuario en la lista de queries para usar items
        using_item[msg.id] = ctx.author.id

    # Si no tiene items, lo mandamos a la vrg
    else:
        inventory_embed.add_field(name="No tienes items en tu inventario!",
                                  value="Usa el comando **/penetienda** para comprar algunos items")

        await ctx.send(embed=inventory_embed)

    print('---------------------------------------------------------------------')


@client.command(name='penecreditos',
                description='Comando para ver los PeneCréditos™ que tienes actualmente',
                brief='Mira tus PeneCréditos!',
                aliases=['Penecreditos', 'PENECREDITOS', 'pc', 'Pc', 'PC'],
                usage='/penecreditos',
                pass_context=True)
async def penecreditos(ctx):
    # Header para debug
    print('---------------------------------------------------------------------')
    print("Comando de penecreditos")

    # Obtenemos los PC del usuario
    pc = database.get_penecreditos(ctx.message.guild.id, ctx.author.id)

    # Más debugging
    print(f"Usuario: {ctx.author}, Penecreditos: {pc}")

    # Mostramos información
    await ctx.send(embed=discord.Embed(title=f"Actualmente tienes {pc} PeneCréditos"))


@client.command(name='penetienda',
                description='Comando para gastar los PeneCréditos™ que tienes actualmente en la PeneTienda™',
                brief='Gasta tus PeneCréditos en la PenTienda™!',
                aliases=['Penetienda', 'PENETIENDA'],
                usage='/penetienda',
                pass_context=True)
async def penetienda(ctx):
    # Header para debugging
    print('---------------------------------------------------------------------')
    print("Comando de penetienda")
    print(f"Usuario: {ctx.author}")
    print(f"Items en tienda: {[item.name for item in tienda.display_items]}")
    # Obtenemos los pc actuales del usuario
    current_penecreditos = database.get_penecreditos(ctx.guild.id, ctx.author.id)

    # Embed que contendrá la "vitrina" de la tienda
    vitrina = discord.Embed(
        title="Bienvenido a la PeneTienda!",
        description=f"Este es el mejor lugar para venir a gastar tus PeneCréditos! "
                    f"Tienes {current_penecreditos} PeneCréditos")

    # Ponemos los items en display en la vitrina
    cont = 1
    for item in tienda.display_items:
        vitrina.add_field(name=f"{cont}️⃣ {item.name} ({item.cost} PC)", value=item.description, inline=False)
        cont += 1

    # Enviamos el menú con la vitrina
    msg = await ctx.send(embed=vitrina)

    # Agregamos los botones de opciones
    for x in range(1, len(tienda.display_items) + 1):
        await msg.add_reaction(f"{x}⃣")

    # Agregamos un botón de cancelar
    await msg.add_reaction('❌')

    # Agregamos al usuario a la lista de compradores actuales
    compras_actuales[msg.id] = ctx.author.id

    print('---------------------------------------------------------------------')


@client.command(name='anuncioAdmin', hidden=True, pass_context=True)
async def anuncio_master(ctx, type, *args):
    if ctx.author.id == 301155670793781248:  # UUID De Guacha
        embed = discord.Embed(title=type.capitalize(), description=' '.join(args))
        await ctx.message.delete()
        await ctx.send("Un Anuncio importante con respecto al bot @everyone!", embed=embed)

    else:
        print(f"Usuario inválido usó comando admin: {ctx.author.id}")


@client.command(name='poll',
                description='Comando para generar una encuesta en el servidor',
                brief='Genera una encuesta!',
                aliases=['Poll', 'POLL', 'encuesta', 'Encuesta', 'ENCUESTA'],
                usage='/poll {(comando) crear|votar} {nombre} {titulo} {tipo (yn|ynm|num)}',
                pass_context=True)
async def poll(ctx, type, title, *args):
    """Función que maneja todas las opciones del comando de encuestas"""
    print('---------------------------------------------------------------------')
    print('Comando poll')  # Debugging

    # Solo el admin debería poder usar las encuestas, luego nececitamos el UUID del admin
    admins = database.get_admins(ctx.guild.id)

    # Verificamos que el admin sea quien usó el comando
    if str(ctx.author.id) in admins:

        if type.lower() == 'yn' or type.lower() == 'sn':
            embed = discord.Embed(title=title)
            embed.set_footer(text='Vota usando los botones de aquí abajo')
            embed.add_field(name='Si', value=':+1:')
            embed.add_field(name='No', value=':-1:')

            message = await ctx.guild.text_channels[0].send('@everyone Respondan a la siguiente encuesta: ',
                                                            embed=embed)
            await message.add_reaction('👍')
            await message.add_reaction('👎')

            print('Encuesta tipo YES/NO Creada exitosamente')
            print(f'Título de la encuesta: {title}')

    else:  # Para los plebeyos
        admin_embed = discord.Embed(title="Admins del servidor", description=f"Para ser admin, debes tener el pene más "
                                                                             f"grande del servidor")

        for admin in admins:
            admin_user = await client.fetch_user(admin)
            admin_embed.add_field(name=admin_user.mention, value="\u200b", inline=False)
        await ctx.send(f"No eres admin, tu pene es inferior", embed=admin_embed)
        print(f"Encuesta no creada: {ctx.author} no es admin")

    print('---------------------------------------------------------------------')


@client.command(name='GG',
                description='Comando para buscar un jugador en OP.GG',
                aliases=['gg', 'Gg'],
                usage='/GG {Nombre de invocador} {Región (Opcional)}',
                pass_context=True)
async def gg(ctx, summ, *args):
    async with ctx.typing():
        if len(args) == 0:
            player = miner.PlayerData(summ)
            ign = player.get_summoner_name()
            if ign is not None:
                player_stats = discord.Embed(title=f'Estadísticas de {ign}', url=player.get_url(),
                                             description=f'Última actualización: {player.get_last_update()}')
                player_stats.set_footer(text="Información obtenida de OP.GG")
                player_stats.set_thumbnail(url=player.get_summoner_icon())

                # Campos de rango
                solo_rank, flex_rank = player.get_summoner_rank()

                player_stats.add_field(name='Rango Solo/Dúo',
                                       value=f'{solo_rank[0]}, {solo_rank[1]} (Winrate: {solo_rank[2]})',
                                       inline=True)
                player_stats.add_field(name='Rango Flex Queue',
                                       value=f'{flex_rank[0]}, {flex_rank[1]} (Winrate: {flex_rank[2]})',
                                       inline=True)

                # Spacer
                player_stats.add_field(name='\u200b', value='\u200b', inline=False)

                # Campos de campeones preferidos
                champos = player.get_most_played()

                # Esta linea la hizo @AndicsMG y no tengo ni puta idea de lo que hace,
                # hasta donde entiendo es un for loop inline, este lenguaje está OP
                string = "\n\n".join(
                    [f'{champ[0]}: {champ[1]} de WR en {champ[3]} partidas ({champ[2]} KDA)' for champ in champos]
                )
                player_stats.add_field(name='Campeones más jugados', value=string)

                # Campo para campeones recientemente jugados

                # De nuevo, grax @AndicsMG, ni me voy a molestar en explicar lo que hace porque ni lo entiendo
                string = "\n\n".join(
                    [f'{champ[0]}: {champ[1]} Winrate ({champ[2]}W/{champ[3]}L)' for champ in player.get_recent_plays()]
                )

                player_stats.add_field(name='Campeones jugados en los últimos 7 días', value=string)

                await ctx.send('Aquí tienes la información que he encontrado: ', embed=player_stats)


@client.command(name='LEC',
                description='Comando para obtener información de la liga profesional de Europa (LEC)',
                brief='Busca un jugador/equipo europeo',
                aliases=['Lec', 'lec', 'EU', 'eu', 'Eu'],
                usage='/LEC {jugador|equipo|partidos} {(Nombre de jugador/equipo) (opcional)}',
                pass_context=True)
async def eu(context, searchtype, *args):
    """Función que organiza la información de un jugador de la liga europea"""
    print('---------------------------------------------------------------------')
    print('Comando de EU')  # Debugging

    # Verificamos si el argumento no es nulo
    if searchtype:
        """Creamos listas con opciones para los tipos de búsquedas (No entiendo por qué mierda, pero en Python
        aparentemente es más eficiente iterar por listas en vez de hacer comparaciones directas (????), no sé si
        lo que leí es correcto, seguramente no, pero de esta forma es más fácil añadir keywords así que así se queda"""
        # todo: investigate if method is efficient
        # Julián del futuro, da lo mismo, pero el comentario se queda, me da pereza reescribirlo
        opt_player = ['player', 'jugador', 'jug', 'ply']
        opt_team = ['team', 'equipo', 'tm', 'eq']
        opt_schedule = ['schedule', 'partidos', 'cronograma', 'matchups', 'sch', 'part', 'matches', 'mat']

        # Verificamos si la persona quiere mirar un jugador específico
        if searchtype.lower() in opt_player:
            async with context.typing():
                # Chiste contra rekkles, si el usuario escribe 'pecho frío' se reemplaza por rekkles
                # Si no, se reemplazan los espacios por underscores
                formatted = 'rekkles' if ' '.join(args) == 'pecho frio' else '_'.join(args)
                player = miner.TournamentData(league='LEC', query=formatted)
                stats = player.get_player_stats()

                # Si stats es None, no se encontró el jugador buscado
                if stats:
                    pic = player.get_picture()

                    print(f"Jugador solicitado: {stats['player_name']}")  # Debugging

                    # Obtenemos un markup hypertextual y lo enviamos
                    markup = get_player_embed(stats, pic)
                    await context.channel.send(content='Aquí tienes la información que encontré', embed=markup)
                else:
                    print('Jugador solicitado: Inválido')
                    await context.channel.send("Ese jugador no existe en la base de datos, revisa la ortografía o "
                                               "asegurate de que lo buscaste en la liga correcta")
        elif searchtype.lower() in opt_team:
            print('Busqueda por equipos')  # Debugging
            async with context.typing():
                # Diccionario de equipos válidos y sus posibles apodos
                valid_teams = {
                    'G2_Esports': ['g2', 'g2 esports', ' g2esports'],
                    'Fnatic': ['fnc', 'fnatic', 'equipo del pecho frio'],
                    'Origen': ['og', 'origen'],
                    'MAD_Lions': ['mad', 'mad lions', 'lions', 'madlions'],
                    'Excel_Esports': ['xl', 'excel', 'excel esports', 'excelesports'],
                    'FC_Schalke_04': ['s04', 'schalke', 'schalke 04', 'shalke', 'shalque', 'schalke04'],
                    'Misfits_Gaming': ['msf', 'misfits', 'misfits gaming', 'misfitsgaming'],
                    'Rogue': ['rge', 'rogue', 'steve aoki'],
                    'SK_Gaming': ['sk', 'skg', 'sk gaming', 'skgaming'],
                    'Team_Vitality': ['vit', 'vitality', 'team vitality', 'teamvitality']
                }

                # Buscamos el nombre del equipo en la lista de nombres y apodos
                chosen_team = None
                arg = ' '.join(args).lower()
                for team in valid_teams:
                    if arg in valid_teams[team]:
                        chosen_team = team
                        break  # Si encuentra el equipo, no debemos buscar mas, rompemos el ciclo

                # Si la variable no es None, quiere decir que encontramos un equipo válido
                if chosen_team:
                    print(f'Equipo elegido: {chosen_team}')  # Debugging

                    # Creamos el objeto buscador de información
                    team_data = miner.TournamentData('LEC', chosen_team)
                    roster = team_data.get_players_in_team()

                    # Markup hypertextual
                    markup = discord.Embed(title=chosen_team.replace('_', ' '))
                    markup.set_thumbnail(url=team_data.get_picture())

                    # Diccionario para relacionar un número de iteración con una posición
                    pos = {
                        1: 'Top',
                        2: 'Jungla',
                        3: 'Mid',
                        4: 'AD Carry',
                        5: 'Soporte'
                    }
                    cont = 1
                    for position in roster:
                        # Añadimos un divisor que inicia la sección de posición
                        markup.add_field(name=f'\nPosición: {pos[cont]}', value='-----------------------------',
                                         inline=False)

                        for player in position:
                            # Agregamos el jugador de la posición (si hay suplentes, se añaden también)
                            markup.add_field(
                                name=player['name'],
                                value=f"Partidos jugados con el equipo esta temporada: {player['games_played']}\n",
                                inline=False
                            )

                        markup.add_field(name='\u200b', value='\u200b')
                        cont += 1

                    await context.channel.send('Aquí tienes la información que encontré', embed=markup)
                else:
                    await context.channel.send("Lo siento, el equipo que ingresaste no es válido, revisa que estés "
                                               "buscando en la liga correcta, o revisa tu ortografía, es recomendable "
                                               "que utilices la denominación de nomenclatura del equipo. "
                                               "(Ej: 'FNC', 'G2')")
        elif searchtype.lower() in opt_schedule:
            async with context.typing():
                print('Solicitud de partidos')  # Debugging
                tournament = miner.TournamentData('LEC', None)
                week = tournament.get_current_week()
                matches = tournament.get_schedule()
                markup = discord.Embed(title='Próximos partidos de la LEC', description='Verano 2020')
                markup.set_footer(text=f'Semana de partidos: Semana {week}')

                cont = 1
                dias = {
                    1: 'Viernes',
                    2: 'Sábado',
                    3: 'Domingo'
                }
                markup.add_field(name=f"Día {math.ceil(cont / 5)} ({(dias[math.ceil(cont / 5)])})",
                                 value='---------------------------------------------'
                                 )
                for match in matches:
                    markup.add_field(name=f'Partida {cont}:', value=f'{match[0]} Vs. {match[1]}', inline=False)
                    if cont % 5 == 0 and cont != len(matches):
                        markup.add_field(name='\u200b', value='\u200b', inline=False)
                        markup.add_field(name=f"Día {math.ceil(cont / 5) + 1} ({(dias[math.ceil(cont / 5) + 1])})",
                                         value='---------------------------------------------'
                                         )

                    cont += 1
                await context.channel.send(content='Aquí tienes la información que encontré', embed=markup)

        else:
            print('Referencia inválida')  # Debugging
            await help(context, 'LEC')

    print('---------------------------------------------------------------------')


@client.command(name='LCS',
                description='Comando para obtener información de la liga profesional de NA (LCS)',
                brief='Busca un jugador/equipo Norteamericano',
                aliases=['Lcs', 'lcs', 'NA', 'na', 'Na'],
                usage='/LCS {jugador|equipo|partidos} {(Nombre de jugador/equipo)(opcional)}',
                pass_context=True)
async def na(context, searchtype, *args):
    """Función que organiza la información de un jugador de la liga Americana"""
    print('---------------------------------------------------------------------')
    print('Comando de NA')  # Debugging
    async with context.typing():
        # Verificamos si el argumento no es nulo
        if searchtype:
            """Creamos listas con opciones para los tipos de búsquedas (No entiendo por qué mierda, pero en Python
            aparentemente es más eficiente iterar por listas en vez de hacer comparaciones directas (????), no sé si
            lo que leí es correcto, seguramente no, pero de esta forma es más fácil añadir keywords así que así se queda"""
            # todo: investigate if method is efficient
            # Julián del futuro, da lo mismo, pero el comentario se queda, me da pereza reescribirlo
            opt_player = ['player', 'jugador', 'jug', 'ply']
            opt_team = ['team', 'equipo', 'tm', 'eq']
            opt_schedule = ['schedule', 'partidos', 'cronograma', 'matchups', 'sch', 'part', 'matches', 'mat']

            # Verificamos si la persona quiere mirar un jugador específico
            if searchtype.lower() in opt_player:

                # Chiste contra rekkles, si el usuario escribe 'pecho frío' se reemplaza por rekkles
                # Si no, se reemplazan los espacios por underscores
                formatted = 'bjergsen' if ' '.join(args) == 'pecho frio' else '_'.join(args)
                player = miner.TournamentData(league='LCS', query=formatted)
                stats = player.get_player_stats()

                # Si stats es None, no se encontró el jugador buscado
                if stats:
                    pic = player.get_picture()

                    print(f"Jugador solicitado: {stats['player_name']}")  # Debugging

                    # Obtenemos un markup hypertextual y lo enviamos
                    markup = get_player_embed(stats, pic)
                    await context.channel.send(content='Aquí tienes la información que encontré', embed=markup)
                else:
                    print('Jugador solicitado: Inválido')
                    await context.channel.send("Ese jugador no existe en la base de datos, revisa la ortografía o "
                                               "asegurate de que lo buscaste en la liga correcta")
            elif searchtype.lower() in opt_team:
                print('Busqueda por equipos')  # Debugging
                # Diccionario de equipos válidos y sus posibles apodos
                valid_teams = {
                    '100_Thieves': ['100', '100 thieves', '100thieves', 'hundred thieves', 'hundredthieves'],
                    'Cloud9': ['c9', 'cloud9', 'cloud 9', 'best team world'],
                    'Counter_Logic_Gaming': ['clg', 'counter logic gaming', 'counter logic', 'counterlogic'],
                    'Dignitas': ['dig', 'dignitas'],
                    'Evil_Geniuses': ['eg', 'evil genius', 'evil geniuses', 'evilgenius', 'evilgeniuses'],
                    'FlyQuest': ['fly', 'flyquest', 'treequest'],
                    'Golden_Guardians': ['gg', 'ggs', 'golden guardians', 'goldenguardians'],
                    'Immortals': ['imt', 'immortals'],
                    'Team_Liquid': ['tl', 'team liquid', 'teamliquid'],
                    'Team_SoloMid': ['tsm', 'tee es em', 'team solo mid', 'teamsolomid', 'team solomid',
                                     'bjergsen y el resto']
                }

                # Buscamos el nombre del equipo en la lista de nombres y apodos
                chosen_team = None
                arg = ' '.join(args).lower()
                for team in valid_teams:
                    if arg in valid_teams[team]:
                        chosen_team = team
                        break  # Si encuentra el equipo, no debemos buscar mas, rompemos el ciclo

                # Si la variable no es None, quiere decir que encontramos un equipo válido
                if chosen_team:
                    print(f'Equipo elegido: {chosen_team}')  # Debugging

                    # Creamos el objeto buscador de información
                    team_data = miner.TournamentData('LCS', chosen_team)
                    roster = team_data.get_players_in_team()

                    # Markup hypertextual
                    markup = discord.Embed(title=chosen_team.replace('_', ' '))
                    markup.set_thumbnail(url=team_data.get_picture())

                    # Diccionario para relacionar un número de iteración con una posición
                    pos = {
                        1: 'Top',
                        2: 'Jungla',
                        3: 'Mid',
                        4: 'AD Carry',
                        5: 'Soporte'
                    }
                    cont = 1
                    for position in roster:
                        # Añadimos un divisor que inicia la sección de posición
                        markup.add_field(name=f'\nPosición: {pos[cont]}', value='-----------------------------',
                                         inline=False)

                        for player in position:
                            # Agregamos el jugador de la posición (si hay suplentes, se añaden también)
                            markup.add_field(
                                name=player['name'],
                                value=f"Partidos jugados con el equipo esta temporada: {player['games_played']}\n",
                                inline=False
                            )

                        markup.add_field(name='\u200b', value='\u200b', inline=False)
                        cont += 1

                    await context.channel.send('Aquí tienes la información que encontré', embed=markup)
                else:
                    await context.channel.send("Lo siento, el equipo que ingresaste no es válido, revisa que estés "
                                               "buscando en la liga correcta, o revisa tu ortografía, es recomendable "
                                               "que utilices la denominación de nomenclatura del equipo. "
                                               "(Ej: 'FNC', 'G2')")
            elif searchtype.lower() in opt_schedule:
                print('Solicitud de partidos')
                tournament = miner.TournamentData('LCS', None)
                week = tournament.get_current_week()
                matches = tournament.get_schedule()
                markup = discord.Embed(title='Próximos partidos de la LCS', description='Verano 2020')
                markup.set_footer(text=f'Semana de partidos: Semana {week}')

                cont = 3
                dias = {
                    1: 'Viernes',
                    2: 'Sábado',
                    3: 'Domingo'
                }
                markup.add_field(name=f"Día {1} ({(dias[1])})",
                                 value='---------------------------------------------'
                                 )
                for match in matches:
                    markup.add_field(name=f'Partida {cont - 2}:', value=f'{match[0]} Vs. {match[1]}', inline=False)
                    if cont % 4 == 0 and cont - 2 != len(matches):
                        markup.add_field(name='\u200b', value='\u200b', inline=False)
                        markup.add_field(name=f"Día {math.ceil(cont / 4) + 1} ({(dias[math.ceil(cont / 4) + 1])})",
                                         value='---------------------------------------------'
                                         )

                    cont += 1
                await context.channel.send(content='Aquí tienes la información que encontré', embed=markup)

            else:
                print('Referencia inválida')  # Debugging
                await help(context, 'LCS')

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
            if not all_commands[command].hidden and command_names.count(all_commands[command].name) == 0:
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
        if args[0] in all_commands and not all_commands[args[0]].hidden:
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
        'bot': 'bot',
        'adc': 'bot',
        'carry': 'bot',
        'sup': 'support',
        'support': 'support',
        'soporte': 'support'
    }

    if len(args) == 2:  # Si el usuario ingresó campeón + linea
        if args[1] in lineas_validas:
            winrate_scraper = miner.WinrateData(champ=args[0], lane=[lineas_validas[args[1]]])
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
async def get_runes(context, champ, lane=None):
    print('---------------------------------------------------------------------')
    print('Comando de builds')  # Debugging
    print(f'Campeón seleccionado: {champ}')
    print(f"Rol seleccionado: {lane if lane else 'Ninguno'}")

    # Diccionario para traducir lineas válidas
    lineas_validas = {
        'top': 'top',
        'jungle': 'jungle',
        'jungla': 'jungle',
        'jg': 'jungle',
        'mid': 'middle',
        'medio': 'middle',
        'middle': 'middle',
        'bot': 'adc',
        'adc': 'adc',
        'carry': 'adc',
        'sup': 'support',
        'support': 'support',
        'soporte': 'support'
    }

    # Creamos el objeto campeón para buscar la info
    if lane is None:
        champion = miner.RuneData(champ.lower())

    else:
        champion = miner.RuneData(champ.lower(), lineas_validas[lane])

    # Usamos la funcion de RuneData para obtener las runas y procesarlas
    runes = champion.rune_data

    # Verificamos si consiguió los datos
    if runes:

        # Obtenemos datos importantes de campeón
        champ_name = champion.champ_name
        role = champion.role
        total_games = champion.total_matches
        played_games = champion.runeset_games
        wr = champion.winrate

        # Creamos el embed con la información válida
        markup = discord.Embed(title=f"Runas indicadas para {champ_name} {role}", description="Obtenido de U.GG")
        markup.set_thumbnail(url=champion.icon)

        # Revisamos si hay advertencia de pocas partidas
        if champion.low_sample_rate:
            markup.add_field(name=':warning:', value=f"Actualmente hay muy poca gente jugando {champ_name} en esa "
                                                     f"posición, Es posible que los datos calculados no sean los "
                                                     f"idóneos", inline=False)

        # Insertamos campos que servirán de título para los árboles de runas
        markup.add_field(name='Principal', value=runes[0][0])
        markup.add_field(name='Secundaria', value=runes[1][0])
        markup.add_field(name='\u200b', value='\u200b')

        markup.add_field(name=runes[0][1][0], value='\n'.join(runes[0][1][1:]))
        markup.add_field(name='Selección secundaria', value='\n'.join(runes[1][1]))
        markup.add_field(name='Selección terciaria', value='\n'.join(runes[2][1]))

        markup.set_footer(text=f'Parche {champion.patch}, Winrate: {wr} (en {played_games} partidas)')

        # Si el usuario no ingresó un rol
        if lane is None:
            await context.channel.send(f"El rol más común que encontré para {champ_name} es en {role}, he creado un "
                                       f"conjunto de runas ideal para ti después de revisar {total_games} partidas!",
                                       embed=markup)

        else:
            await context.channel.send(f"He creado un conjunto de runas ideal para ti después de revisar {total_games}"
                                       f" partidas!", embed=markup)

        print("Información enviada exitosamente")
        print('---------------------------------------------------------------------')
    else:
        await context.channel.send(f"Buena imbécil, escribiste mal algo, aprende a escribir "
                                   f"{context.message.author.mention}")
        print("Campeón no existe")
        print('---------------------------------------------------------------------')


@client.command(name='build',
                description='Comando que te muestra las builds recomendadas de algún campeón de LoL',
                brief='Obtén la build de un campeón!',
                aliases=['Build', 'builds', 'BUILD', 'Builds', 'BUILDS'],
                usage='/build {campeón}',
                pass_context=True)
async def get_builds(context, champ, lane=None):
    """Con esta funcion se obtienen las builds del scraper, y se entregan al usuario"""

    print('---------------------------------------------------------------------')
    print('Comando de builds')  # Debugging
    print(f'Campeón seleccionado: {champ}')
    print(f'Rol seleccionado: {lane}')

    # Diccionario para traducir lineas válidas
    lineas_validas = {
        'top': 'top',
        'jungle': 'jungle',
        'jungla': 'jungle',
        'jg': 'jungle',
        'mid': 'mid',
        'medio': 'mid',
        'middle': 'mid',
        'bot': 'bot',
        'adc': 'bot',
        'carry': 'bot',
        'sup': 'support',
        'support': 'support',
        'soporte': 'support'
    }

    # Creamos el objeto que contiene los datos del champ que se requiera
    if lane is not None:
        champion_data = miner.BuildData(champ.lower(), lineas_validas[lane])

    else:
        champion_data = miner.BuildData(champ.lower())

    # De este objeto, obtenemos la info de las builds
    starter = champion_data.starter_items
    core = champion_data.core_items
    boots = champion_data.boots

    if starter is not None and core is not None and boots is not None:  # Verificamos que hayamos conseguido los datos
        champ_name = champion_data.champ_name
        role = champion_data.role
        markup = discord.Embed(title=f"Items indicados para {champ_name} {role}",
                               description="Obtenido de Riot KR database by OP.GG"
                               )
        markup.url = champion_data.url
        markup.set_thumbnail(url=champion_data.icon)

        # Agregamos los campos de items iniciales
        markup.add_field(name="Items iniciales",
                         value=f"Aquí tienes varias opciones de items iniciales para {champ_name}",
                         inline=False)
        cont = 1
        for item_data in starter:
            # Cada dataset tiene una lista con los items, una cadena con el PR% y una cadena con el WR%
            markup.add_field(name=f"Set {cont} ({item_data[1]}% Pickrate - {item_data[2]}% Winrate)",
                             value='\n\t:arrow_down:\n'.join(item_data[0]))

            cont += 1

        # Whitespace spacer for next item sets
        markup.add_field(name="\u200b", value="\u200b", inline=False)

        # Agregamos los campos de items core
        markup.add_field(name="Core Builds",
                         value=f"Aquí tienes las core builds más comunes para {champ_name} {role}",
                         inline=False)

        cont = 1
        for item_data in core:
            # Cada dataset tiene una lista con los items, una cadena con el PR% y una cadena con el WR%
            markup.add_field(name=f"Set {cont} ({item_data[1]}% Pickrate - {item_data[2]}% Winrate)",
                             value='\n\t:arrow_down:     \n'.join(item_data[0]))

            cont += 1

        # Whitespace spacer for next item sets
        markup.add_field(name="\u200b", value="\u200b", inline=False)

        # Agregamos los campos de botas
        markup.add_field(name="Botas",
                         value=f"Aquí tienes opciones de botas comunes para {champ_name} {role}",
                         inline=False)

        cont = 1
        for item_data in boots:
            # Cada dataset tiene una lista con los items, una cadena con el PR% y una cadena con el WR%
            markup.add_field(name=f"Set {cont} ({item_data[1]}% Pickrate - {item_data[2]}% Winrate)",
                             value=item_data[0])

            cont += 1

        # Agregamos detalles y enviamos el embed
        markup.set_footer(text=f'Parche {champion_data.patch}')

        await context.send(embed=markup)

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


@commands.cooldown(1, 120, commands.BucketType.user)  # Fue necesario implementar un cooldown (Gracias Miguel)
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
        ansiados[context.author.id] = 0

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


@client.command(hidden=True)
async def anuncio(context, *args):
    """Comando para poder enviar anuncios, solo la persona con el pene más grande los puede enviar"""

    # Obtenemos los UUID de las personas con el pene más grande (el admin)
    admins = database.get_admins(context.guild.id)

    # Obtenemos el primer canal de la lista de canales de texto
    channel = context.guild.text_channels[0]

    # Debugging
    print('---------------------------------------------------------------------')
    print(f'Anuncio con información: {anuncio}')
    print(f"Usuario que lo pide: {context.author}")

    # Verificamos si el UUID del autor del comando es igual al del que deberia ser admin
    if str(context.author.id) in admins:
        await context.message.delete()
        msg = ' '.join(args)
        markup = discord.Embed(title=msg)

        await channel.send(f'SU ADMIN, {context.author.mention}, HA HABLADO @everyone!', embed=markup)

    else:
        admin_embed = discord.Embed(title="Admins del servidor", description=f"Para ser admin, debes tener el pene más "
                                                                             f"grande del servidor")
        admin_embed.add_field(name="Admins del servidor", value="\u200b")
        for admin in admins:
            admin_user = await client.fetch_user(admin)
            admin_embed.add_field(name=admin_user.name, value="\u200b", inline=False)
        await channel.send(f"No eres admin, tu pene es inferior", embed=admin_embed)

    print('---------------------------------------------------------------------')


# Manejo de errores
@eu.error
async def eu_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Careverga, esa vaina no se usa así")
        await help(ctx, 'LEC')
    else:
        print('Error interno del bot: ', error)
        print('---------------------------------------------------------------------')


@na.error
async def na_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Careverga, esa vaina no se usa así")
        await help(ctx, 'LCS')
    else:
        print('Error interno del bot:', error)
        print('---------------------------------------------------------------------')


@add_paja.error
async def paja_error(ctx: discord.ext.commands.Context, error):
    if isinstance(error, commands.CommandOnCooldown):
        print('---------------------------------------------------------------------')
        if ansiados.get(ctx.message.author.id) == 2:  # Si ya ha sido un ansiado por mucho tiempo
            print("Ansiado castigado")
            client.get_command('paja').reset_cooldown(ctx)
            ansiados[ctx.author.id] += 1
            await ctx.channel.send(content='Por marica, mereces un castigo',
                                   embed=discord.Embed(title='ANUNCIO DE TAMAÑO DE PENE',
                                                       description=f'{ctx.message.author.mention}: El tamaño de tu '
                                                                   f'pene ha sido reducido en 1 cm y tus pajas han sido '
                                                                   f'reducidas en 5'
                                                       )
                                   )
            size = database.get_pene(ctx.guild.id, ctx.message.author.id)
            pajas = database.get_pajas(ctx.guild.id, ctx.message.author.id)
            if size > 0:
                database.set_pene(ctx.guild.id, ctx.message.author.id, size - 1)

            database.set_pajas(ctx.guild.id, ctx.message.author.id, pajas - 5)

        elif ansiados.get(ctx.message.author.id) > 2:
            client.get_command('paja').reset_cooldown(ctx)
            print("Ansiado sigue insistiendo, por spammer no se le respondió")  # Debugging
            await ctx.message.delete()

        else:  # Si es un ansiado menos de 3 veces

            print(f"Paja ansiada, contador: {ansiados[ctx.author.id]}")  # Debugging

            ansiados[ctx.author.id] += 1

            markup = discord.Embed(title='Tiempo para siguiente paja', description=f'{str(error.retry_after)} segundos')
            markup.add_field(name='Contador de ansiedad', value=f'Has sido un ansiado {ansiados[ctx.author.id]} veces')
            await ctx.channel.send(content='Malparido ansiado de mierda, aguanta un poquito, se te va a caer la verga '
                                           'hijo de tu mil puta madre',
                                   embed=markup)

        print('---------------------------------------------------------------------')


# Eventos
@client.event
async def on_ready():
    """Función de Debugging para el bot, nos confirma que no se explotó esta mondá"""
    print('---------------------------------------------------------------------')  # Debugging
    print('Bot conectado satisfactoriamente!')  # Debugging
    print(client.user.name)  # Debugging
    print(client.user.id)  # Debugging
    print('---------------------------------------------------------------------')  # debugging

    # Iniciar contador de reseteo y de stocks
    upd_cont_reset.start()
    farm_rewards.start()
    # cont_stocks.start()


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if user.id != client.user.id:
        if reaction.message.id in compras_actuales:
            if user.id == compras_actuales[reaction.message.id]:

                valid_emojis = {
                    '1⃣': 1, '2⃣': 2, '3⃣': 3, '4⃣': 4, '5⃣': 5, '6⃣': 6, '7⃣': 7, '8⃣': 8, '9⃣': 9
                }

                if reaction.emoji in valid_emojis:
                    purchase_item = tienda.display_items[int(reaction.emoji[0]) - 1]

                    success = database.get_penecreditos(reaction.message.guild.id, user.id) >= purchase_item.cost

                    if success:

                        if 'prob+' in purchase_item.effect:
                            prob_increase = purchase_item.effect.split('+')[-1]

                            database.increase_prob(reaction.message.guild.id, user.id, purchase_item.cost,
                                                   increase=prob_increase)

                        else:

                            database.purchase(reaction.message.guild.id, user.id, purchase_item)

                        del compras_actuales[reaction.message.id]

                        await reaction.message.channel.send(f"{user.mention} ha comprado {purchase_item.name} "
                                                            f"por {purchase_item.cost} PeneCréditos")
                        await reaction.message.delete()

                        tienda.reset_display_items()

                    else:
                        await reaction.message.channel.send("No tienes PeneCréditos suficientes para comprar ese item!")

                        await reaction.remove(user)

                elif reaction.emoji == '❌':
                    await reaction.message.channel.send("Has cancelado tu compra")

                    del compras_actuales[reaction.message.id]

                    await reaction.message.delete()

        elif reaction.message.id in using_item:
            if user.id == using_item[reaction.message.id]:

                sel_emojis = {
                    '1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, '6️⃣': 6, '7️⃣': 7, '8️⃣': 8, '9️⃣': 9
                }

                if reaction.emoji in sel_emojis:

                    msg = reaction.message

                    channel = msg.channel

                    inv = database.get_inventory(msg.guild.id, user.id)

                    inv_items = list(inv.keys())

                    used_item = inv_items[int(reaction.emoji[0]) - 1]

                    item = tienda.item_from_string(used_item)

                    del using_item[msg.id]

                    await msg.delete()

                    msg = await channel.send(embed=discord.Embed(
                        title=f"Estás seguro que deseas usar {item.name}?",
                        description=f"Actualmente tienes {inv[item.name]}"
                    ))

                    await msg.add_reaction('⭕')
                    await msg.add_reaction('❌')

                    confirmation[msg.id] = (user.id, item)

                elif reaction.emoji == '❌':
                    await reaction.message.channel.send("Has cancelado el uso de tu item")
                    await reaction.message.delete()
                    del using_item[reaction.message.id]

        elif reaction.message.id in confirmation:
            if user.id == confirmation[reaction.message.id][0]:

                if reaction.emoji == '⭕':

                    item = confirmation[reaction.message.id][1]
                    user_id = confirmation[reaction.message.id][0]
                    channel: discord.TextChannel = reaction.message.channel
                    async with channel.typing():
                        await use_item(user_id, reaction.message.guild.id, item, channel)

                        await reaction.message.delete()

                        del confirmation[reaction.message.id]

                        database.consume_item(reaction.message.guild.id, user_id, item)

                elif reaction.emoji == '❌':

                    await reaction.message.channel.send("Has cancelado el uso de tu item")

                    await reaction.message.delete()

                    del confirmation[reaction.message.id]

        elif reaction.message.id in betting:
            if user.id == betting[reaction.message.id]:
                msg: discord.Message = reaction.message
                user_pc = database.get_penecreditos(msg.guild.id, user.id)

                betting_options = {
                    '1️⃣': 1,
                    '2️⃣': 5,
                    '3️⃣': 10,
                    '4️⃣': 25,
                    '5️⃣': 50,
                    '6️⃣': 100,
                    '7️⃣': 250,
                }

                if reaction.emoji in betting_options:
                    bet = betting_options[reaction.emoji]

                    if bet <= user_pc:
                        await msg.clear_reactions()

                        database.consume_pc(msg.guild.id, user.id, bet)

                        engine = Casino.Blackjack(Casino.Deck())
                        engine.set_player(user, bet)
                        engine.deal_hands()

                        game_embed = get_blackjack_embed(engine)

                        game_embed.set_footer(text="Decide qué harás ahora!")

                        await msg.edit(embed=game_embed)

                        await msg.add_reaction('✅')
                        await msg.add_reaction('🛑')

                        engine.set_ui(msg)

                        del betting[msg.id]

                        blackjack_games[user.id] = engine

                elif reaction.emoji == '❌':

                    await reaction.message.channel.send("Has salido del PeneCasino™")
                    del betting[reaction.message.id]
                    await reaction.message.delete()

        elif user.id in blackjack_games:
            if reaction.message.id == blackjack_games[user.id].message.id:

                actions = ['✅', '🛑']

                game: Casino.Blackjack = blackjack_games[user.id]

                msg = reaction.message

                if reaction.emoji in actions:

                    await msg.clear_reactions()

                    if reaction.emoji == '✅':

                        game.hit_player()

                        if game.player.get_numeric_value() > 21:

                            game_embed = get_blackjack_embed(game, show_dealer_hand=True)
                            game_embed.colour = discord.Colour.red()
                            game_embed.set_footer(text="Vaya! Te has pasado de 21, Perdiste!")

                            await msg.edit(embed=game_embed)

                            del blackjack_games[user.id]

                        else:

                            game_embed = get_blackjack_embed(game)

                            game_embed.set_footer(text="Decide qué harás ahora!")

                            await msg.edit(embed=game_embed)

                            await msg.add_reaction('✅')
                            await msg.add_reaction('🛑')

                    else:

                        game_embed = get_blackjack_embed(game, show_dealer_hand=True)
                        game_embed.set_footer(text="Turno del Dealer")

                        await msg.edit(embed=game_embed)

                        while game.get_dealer_hit():
                            await asyncio.sleep(2)
                            game.dealer_hand.append(game.deck.draw_card())

                            game_embed = get_blackjack_embed(game, show_dealer_hand=True)
                            game_embed.set_footer(text="El Dealer está jugando")
                            await msg.edit(embed=game_embed)

                        winner, mult = game.get_winners()

                        if winner:

                            earnings = int(mult * game.player.bet)

                            game_embed = get_blackjack_embed(game, show_dealer_hand=True)
                            game_embed.set_footer(text=f"Has ganado, conseguiste {mult}x tu apuesta "
                                                       f"({earnings} PC)")
                            game_embed.colour = discord.Colour.green()

                            database.give_penecreditos(msg.guild.id, user.id, earnings)

                        else:
                            game_embed = get_blackjack_embed(game, show_dealer_hand=True)
                            game_embed.set_footer(text=f"Has perdido, el dealer tiene una mejor mano que tú")
                            game_embed.colour = discord.Colour.red()

                        await msg.edit(embed=game_embed)
                        del blackjack_games[user.id]

        elif reaction.message.id in upgrading_farm:
            if user.id == upgrading_farm[reaction.message.id]:
                msg: discord.Message = reaction.message
                user_pc = database.get_penecreditos(msg.guild.id, user.id)
                user_farm = farm_module.get_farm(msg.guild.id, user.id)

                upg_emojis = ["🧯", "💰", "🌱", "🌊", "☢️"]

                if reaction.emoji in upg_emojis:

                    if reaction.emoji == "🧯":
                        lvl = user_farm['upgrades']['Resistencia al Fuego']
                        if user_pc >= pow(10, lvl):
                            farm_module.upgrade_farm(msg.guild.id, user.id, lvl, 'Resistencia al Fuego')
                            database.consume_pc(reaction.message.guild.id, user.id, int(pow(10, lvl)))
                            await reaction.message.channel.send("Has mejorado tu granja con éxito!")


                        else:
                            await reaction.remove(user)

                    if reaction.emoji == "💰":
                        lvl = user_farm['upgrades']['Mejora de PeneIngresos']
                        if user_pc >= pow(10, lvl):
                            farm_module.upgrade_farm(msg.guild.id, user.id, lvl, 'Mejora de PeneIngresos')
                            database.consume_pc(reaction.message.guild.id, user.id, int(pow(10, lvl)))
                            await reaction.message.channel.send("Has mejorado tu granja con éxito!")
                            await reaction.message.delete()

                        else:
                            await reaction.remove(user)

                    if reaction.emoji == "🌱":
                        lvl = user_farm['upgrades']['Mejora de Exploración']
                        if user_pc >= pow(10, lvl):
                            farm_module.upgrade_farm(msg.guild.id, user.id, lvl, 'Mejora de Exploración')
                            database.consume_pc(reaction.message.guild.id, user.id, int(pow(10, lvl)))
                            await reaction.message.channel.send("Has mejorado tu granja con éxito!")

                        else:
                            await reaction.remove(user)

                    if reaction.emoji == "🌊":
                        lvl = user_farm['upgrades']['Resistencia a Inundaciones']
                        if user_pc >= pow(10, lvl):
                            farm_module.upgrade_farm(msg.guild.id, user.id, lvl, 'Resistencia a Inundaciones')
                            database.consume_pc(reaction.message.guild.id, user.id, int(pow(10, lvl)))
                            await reaction.message.channel.send("Has mejorado tu granja con éxito!")

                        else:
                            await reaction.remove(user)

                    if reaction.emoji == "☢️":
                        lvl = user_farm['upgrades']['Bunker Nuclear']
                        if user_pc >= pow(10, lvl):
                            farm_module.upgrade_farm(msg.guild.id, user.id, lvl, 'Bunker Nuclear')
                            database.consume_pc(reaction.message.guild.id, user.id, int(pow(10, lvl)))
                            await reaction.message.channel.send("Has mejorado tu granja con éxito!")

                        else:
                            await reaction.remove(user)

                    del upgrading_farm[reaction.message.id]

                elif reaction.emoji == '❌':

                    del upgrading_farm[reaction.message.id]
                    await reaction.message.channel.send("Has cancelado la mejora")
                    await reaction.message.delete()


@client.event
async def on_message(message: discord.Message):
    if message.author.id != client.user.id:

        if message.content.startswith(client.command_prefix):
            await client.process_commands(message)
            return

        if message.author.id in target_selection:

            if len(message.mentions) == 1:

                item = target_selection[message.author.id]

                target: discord.User = message.mentions[0]

                if 'rival-' in item.effect:

                    guid = message.guild.id

                    try:

                        reduction = int(item.effect.split('-')[-1])

                        current_target_size = database.get_pene(guid, target.id)

                        database.set_pene(guid, target.id, current_target_size - reduction)

                        embed = discord.Embed(title="Se ha reducido el tamaño de un pene!")
                        embed.add_field(name=f"Pene de {target.display_name}",
                                        value=f"{current_target_size} :arrow_right: {current_target_size - reduction}")

                        await message.channel.send(f"{message.author.mention} ha usado {item.name} en "
                                                   f"{target.mention}!",
                                                   embed=embed)

                        del target_selection[message.author.id]

                        database.consume_item(guid, message.author.id, item)

                    except TypeError:
                        await message.channel.send("Tu objetivo aún no tiene tamaño de pene, no puedes reducirlo!")

                elif 'robar-' in item.effect:

                    guid = message.guild.id

                    steal_percentage = int(item.effect.split('-')[-1])

                    current_target_pc = database.get_penecreditos(guid, target.id)

                    stolen_pc = int(current_target_pc * (steal_percentage / 100))

                    database.consume_pc(guid, target.id, stolen_pc)

                    embed = discord.Embed(title=f"Has robado {stolen_pc} PeneCréditos™!")
                    embed.add_field(name=f"PC de {target.display_name}",
                                    value=f"{current_target_pc} :arrow_right: {current_target_pc - stolen_pc}")

                    # Verificación de si el ladrón fue leal
                    if random.random() < 0.5:
                        embed.description = "El ladrón ha sido fiel al contrato, recibes el 50% de lo que robó"

                        current_user_pc = database.get_penecreditos(guid, message.author.id)
                        database.give_penecreditos(guid, message.author.id, stolen_pc // 2)

                        embed.add_field(name=f"PC de {message.author.display_name}",
                                        value=f"{current_user_pc} :arrow_right: {current_user_pc + (stolen_pc // 2)}")

                    else:
                        embed.description = "Al ladrón le valió verga el contrato y se llevó todos los PC que robó"

                    await message.channel.send(f"{message.author.mention} ha usado {item.name} en "
                                               f"{target.mention}!",
                                               embed=embed)

                    del target_selection[message.author.id]


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


def get_blackjack_embed(blackjack: Casino.Blackjack, show_dealer_hand=False):
    game_embed = discord.Embed(title=f"Partida de blackjack de {blackjack.player.user.name}")

    game_embed.colour = discord.Colour.blue()

    game_embed.set_author(name=f"{blackjack.player.user.display_name} ha apostado {blackjack.player.bet} PC",
                          icon_url=blackjack.player.user.avatar_url)

    if show_dealer_hand:
        game_embed.add_field(name=f"Dealer [{blackjack.get_dealer_value()}]",
                             value=f"{' '.join([card.get_upper_emoji() for card in blackjack.dealer_hand])}\n"
                                   f"{' '.join([card.get_lower_emoji() for card in blackjack.dealer_hand])}")

    else:
        game_embed.add_field(name=f"Dealer [?]",
                             value=f"{blackjack.dealer_hand[0].get_upper_emoji()} {Casino.Card.back_top()}\n"
                                   f"{blackjack.dealer_hand[0].get_lower_emoji()} {Casino.Card.back_bottom()}")

    game_embed.add_field(name=f"{blackjack.player.user.name} [{blackjack.player.get_numeric_value()}]",
                         value=f"{' '.join([card.get_upper_emoji() for card in blackjack.player.hand])}\n"
                               f"{' '.join([card.get_lower_emoji() for card in blackjack.player.hand])}")

    return game_embed


async def use_item(uuid: int, guid: int, item: Economia.Item, channel: discord.TextChannel) -> bool:
    if 'pene+' in item.effect:
        increase_size = int(item.effect.split('+')[-1])

        current_size = database.get_pene(guid, uuid)

        if current_size is not None:

            database.set_pene(guid, uuid, current_size + increase_size)

            anuncio = discord.Embed(title="Felicidades! Tu tamaño de pene ha aumentado!",
                                    description=f"{current_size} :arrow_right: {current_size + increase_size}")

            user = await client.fetch_user(uuid)

            await channel.send(f"{user.mention} ha usado {item.name}", embed=anuncio)

            # Retorna falso porque ya no debemos esperar un objetivo
            return False

        else:
            await channel.send("Aún no tienes tamaño de pene! Primero obtén un tamaño y luego puedes usar este item")

    elif 'rival-' in item.effect:

        inst = discord.Embed(title="Envía un mensaje mencionando a la persona a la que quieres encogerle el pene",
                             description=f"Por ejemplo: {client.user.mention}")
        await channel.send(embed=inst)

        target_selection[uuid] = item

        return True

    elif 'pajas+' in item.effect:

        cant_pajas = int(item.effect.split('+')[-1])

        pajas_actuales = database.get_pajas(guid, uuid)

        for _ in range(cant_pajas):
            database.add_paja(guid, uuid)

        user = await client.fetch_user(uuid)
        anuncio = discord.Embed(title="Espero que lo hayas disfrutado!",
                                description=f"Pajas de {user.mention}: {pajas_actuales} :arrow_right: "
                                            f"{pajas_actuales + cant_pajas}")

        await channel.send(f"{user.mention} ha usado {item.name}", embed=anuncio)

        return False

    elif 'admin-' in item.effect:

        reduc = int(item.effect.split('-')[-1])

        admins = database.get_admins(guid)

        anuncio = discord.Embed(title="Has reducido el tamaño de los admins!")

        # COmo todos los admins tiene el mismo tamaño, da igual cual usemos para el tamaño de los admins
        admin_tam = database.get_pene(guid, admins[0])

        # Nos aseguramos que el tamaño no sea negativo
        if admin_tam - reduc < 0:
            new_tam = 0

        else:
            new_tam = admin_tam - reduc
        for admin_uuid in admins:
            admin_user = await client.fetch_user(admin_uuid)

            database.set_pene(guid, admin_uuid, new_tam)

            anuncio.add_field(name=f"{admin_tam} :arrow_right: {new_tam}",
                              value=f"Pene de {admin_user.mention}", inline=False)

        item_user = await client.fetch_user(uuid)
        await channel.send(f"{item_user.mention} ha usado {item.name}", embed=anuncio)

        return False

    elif 'todos-' in item.effect:

        reduc = int(item.effect.split('-')[-1])

        penes = database.get_all_penes(guid)

        anuncio = discord.Embed(title="Has reducido el tamaño de todos!")

        for target_uid in penes:

            if target_uid == uuid:
                continue

            user = await client.fetch_user(target_uid)

            curr_size = penes[target_uid]

            if curr_size - reduc < 0:
                new_tam = 0

            else:
                new_tam = curr_size - reduc

            anuncio.add_field(name=f"{curr_size} :arrow_right: {new_tam}",
                              value=f"Pene de {user.mention}",
                              inline=False)

            database.set_pene(guid, target_uid, new_tam)

        user = await client.fetch_user(uuid)
        await channel.send(f"{user.mention} ha usado {item.name} @everyone", embed=anuncio)

        return False

    elif 'robar-' in item.effect:

        inst = discord.Embed(title="Envía un mensaje mencionando a la persona a la que quieres robarle",
                             description=f"Por ejemplo: {client.user.mention}")
        await channel.send(embed=inst)

        target_selection[uuid] = item


if __name__ == '__main__':
    TOKEN = get_token(3)
    client.run(TOKEN)
