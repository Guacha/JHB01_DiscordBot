from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime, timedelta


class PlayerData:

    def get_url(self):
        return f'https://{self.region}.op.gg/summoner/userName={self.summoner}'

    def get_soup(self):
        url = f'https://{self.region}.op.gg/summoner/userName={self.summoner}'
        webpage = requests.get(url=url)
        return BeautifulSoup(webpage.content, 'html.parser')

    def __init__(self, summoner: str, region='lan'):
        self.region = region
        self.summoner = summoner
        self.soup = self.get_soup()

    def get_summoner_name(self):
        info_div = self.soup.find('div', class_='Information')
        try:
            return info_div.span.get_text()
        except AttributeError:
            return None

    def get_last_update(self):
        update = self.soup.find('div', class_='LastUpdate').get_text()

        split_date = update[17:-10].split('-')

        update_date = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]))

        days_ago = divmod((datetime.now() - update_date).total_seconds(), 86400)[0]

        # Es posible que la diferencia sea negativa, por las zonas horarias
        if days_ago < 0:
            days_ago += 1

        return f"{update_date.strftime('%x')} (Hace {int(days_ago)} días)"

    def get_summoner_rank(self):
        solo_info = self.soup.find('div', class_='SummonerRatingMedium')
        flex_info = self.soup.find('div', class_='sub-tier')

        # Obtener la división del jugador
        solo_rank = solo_info.find('div', class_='TierRank').string
        flex_rank = flex_info.div.find('div', class_='sub-tier__rank-tier').string.strip()

        # Obtener la medalla (Ícono de liga) del jugador
        solo_medal = f"https:{solo_info.div.img['src']}"
        flex_medal = f"https:{flex_info.img['src']}"

        # Obtener el LP del jugador
        solo_lp = solo_info.find('span', class_="LeaguePoints").string.strip()
        flex_lp = flex_info.find('div', class_='sub-tier__league-point').get_text()
        flex_lp = flex_lp[0:flex_lp.find('/')]  # Splicing para quitar texto innecesario

        # Obtener winrate del jugador
        solo_winrate = solo_info.find('span', class_='winratio').string[10:]
        flex_winrate = flex_info.find('div', class_='sub-tier__gray-text').string.strip()[9:]

        # Organizar la información en una tupla
        solo_player_data = (solo_rank, solo_lp, solo_winrate)
        flex_player_data = (flex_rank, flex_lp, flex_winrate)

        return solo_player_data, flex_player_data

    def get_summoner_icon(self):
        icon = self.soup.find('img', class_='ProfileImage')['src']
        return f'https:{icon}'

    def get_most_played(self):
        champs_data = self.soup.find_all('div', class_='ChampionBox Ranked')
        player_data = []
        for champ in champs_data:
            champ_name = champ.find('div', class_='ChampionName').a.get_text().strip()
            champ_winrate = champ.find('div', class_='WinRatio').get_text().strip()
            champ_kda = champ.find('span', class_='KDA').get_text()[:-2]
            champ_games = champ.find('div', class_='Title').get_text()
            champ_games = champ_games[0:champ_games.find(' ')]
            player_data.append((champ_name, champ_winrate, champ_kda, champ_games))

        return player_data

    def get_recent_plays(self):
        champs_data = self.soup.find_all('div', class_='ChampionWinRatioBox')

        player_data = []
        for champ in champs_data:
            champ_name = champ.find('div', class_='ChampionName').a.get_text().strip()
            champ_winrate = champ.find('div', class_='WinRatio').get_text().strip()

            wins = losses = 0
            for lobside in champ.find('div', class_='Graph').find_all('div'):
                if 'Text' in lobside['class']:
                    if 'Left' in lobside['class']:
                        wintext = lobside.get_text().strip()
                        wins = int(wintext[:wintext.find('W')])
                    elif 'Right' in lobside['class']:
                        losstext = lobside.get_text().strip()
                        losses = int(losstext[:losstext.find('L')])
            yield (champ_name, champ_winrate, wins, losses)


class TournamentData:
    """Esta clase contendrá los queries de torneo que se necesiten de jugadores o posiciones"""
    YEAR = ""
    SPLIT = ""
    LEAGUE = ""

    def get_schedule(self):
        """Obtiene los partidos de la semana pertinente"""

        global YEAR, SPLIT, LEAGUE
        # Formamos una URL con los valores de año, liga y split
        url = f'https://lol.gamepedia.com/{LEAGUE}/{YEAR}_Season/{SPLIT}_Season'

        # Buscamos la información de documento HTML en la página, y de ahí, lo que nos interesa
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        table = soup.find_all('tr', class_=re.compile('mdv-allweeks mdv-week'))

        # Lista que contendrá la información de la semana pertinente
        week = []
        for row in table:
            # print(f"{row['class']}") debugging

            # En la página, se muestran solamente los partidos de la semana activa, los demás se ocultan
            if 'toggle-section-hidden' in row['class']:
                continue
            else:
                if 'column-label-small' not in row['class']:  # Revisamos que no sea el header de la tabla
                    week.append(row)

        # Lista que contendrá las tuplas de equipos que tienen partido en la semana pertinente
        matches = []
        for row in week:
            teams = row.find_all('span', class_='teamname')  # Sacamos los nombres de equipo

            # For inline retorna lista tal que sus posiciones son dos equipos que se enfrentan, EJ: ['FNC', 'G2']
            matches.append([team.get_text() for team in teams])

        return matches

    def get_current_week(self):
        """Funciona casi igual que el método get_schedule, retorna el numero de la semana actual"""
        global YEAR, SPLIT, LEAGUE
        url = f'https://lol.gamepedia.com/{LEAGUE}/{YEAR}_Season/{SPLIT}_Season'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')

        # Buscamos entre todos los headers de tabla (Los headers contienen la semana)
        table = soup.find_all('tr', class_=re.compile('column-label-small mdv-allweeks mdv-week'))

        for week in table:

            # Si la lista con las clases es < 4, quiere decir que no tiene el tag de "hidden"
            if len(week['class']) < 4:
                # retorna el último caracter del último elemento de la lista de "class"
                return int(week['class'][-1][-1])

    def get_picture(self):
        url = f'https://lol.gamepedia.com/{self.query}'
        html = requests.get(url=url)
        soup = BeautifulSoup(html.content, 'html.parser')
        pic_container = soup.find('div', class_='floatnone')
        return pic_container.a.img['src']

    def get_player_stats(self):
        global YEAR, SPLIT, LEAGUE
        url = f'https://lol.gamepedia.com/index.php?pfRunQueryFormName=TournamentStatistics&title=Special%3ARunQuery' \
              f'%2FTournamentStatistics&TS%5Bpreload%5D=TournamentByPlayer&TS%5Btournament%5D={LEAGUE}%2F{YEAR}+' \
              f'Season%2F{SPLIT}+Season&TS%5Blink%5D={self.query}&TS%5Bchampion%5D=&TS%5Brole%5D=&TS%5Bteam%5D=&TS' \
              f'%5Bpatch%5D=&TS%5Byear%5D=&TS%5Bregion%5D=&TS%5Btournamentlevel%5D=&TS%5Bwhere%5D=&TS%5Bincludelink%5D' \
              f'%5Bis_checkbox%5D=true&TS%5Bshownet%5D%5Bis_checkbox%5D=true&wpRunQuery=Run+query&pf_free_text='

        html = requests.get(url=url)
        soup = BeautifulSoup(html.content, 'html.parser')

        table = soup.find('table')
        if len(table.find_all('tr')) == 6:
            # jugador encontrado
            player_raw_info = table.find_all('tr')[-1].find_all('td')
            player_stats = {
                'team_name': player_raw_info[0].a['title'],
                'team_logo': player_raw_info[0].a.img['src'],
                'player_name': player_raw_info[1].get_text(),
                'games_played': player_raw_info[2].get_text(),
                'wins': player_raw_info[3].get_text(),
                'losses': player_raw_info[4].get_text(),
                'winratio': player_raw_info[5].get_text(),
                'k/game': player_raw_info[6].get_text(),
                'd/game': player_raw_info[7].get_text(),
                'a/game': player_raw_info[8].get_text(),
                'kda': player_raw_info[9].get_text(),
                'cs/game': player_raw_info[10].get_text(),
                'cs/min': player_raw_info[11].get_text(),
                'gold/game': f'{player_raw_info[12].get_text()}K',
                'gold/min': player_raw_info[13].get_text(),
                'kill_part': player_raw_info[14].get_text(),
                'kill_share': player_raw_info[15].get_text(),
                'gold_share': player_raw_info[16].get_text(),
                'champs_played': []
            }
            for champ in player_raw_info[18].find_all('a'):
                player_stats['champs_played'].append(champ.span['title'])

            return player_stats
        else:
            return None

    def get_players_by_position(self, position):
        """Obtiene el jugador del equipo solicitado en la posición especificada"""

        global YEAR, SPLIT, LEAGUE

        # El procedimiento es el mismo que en la función get_player_stats
        url = f'https://lol.gamepedia.com/index.php?pfRunQueryFormName=TournamentStatistics' \
              f'&title=Special%3ARunQuery%2FTournamentStatistics&TS%5Bpreload%5D=ByPlayerRole' \
              f'&TS%5Btournament%5D={LEAGUE}+{YEAR}+{SPLIT}&TS%5Blink%5D=&TS%5Bchampion%5D=' \
              f'&TS%5Brole%5D={position}&TS%5Bteam%5D={self.query}&TS%5Bpatch%5D=' \
              f'&TS%5Byear%5D=2020&TS%5Bregion%5D=&TS%5Btournamentlevel%5D=&TS%5Bwhere%5D=' \
              f'&TS%5Bincludelink%5D%5Bis_checkbox%5D=true&TS%5Bshownet%5D%5Bis_checkbox%5D=true' \
              f'&wpRunQuery=Run+query&pf_free_text='

        html = requests.get(url=url)
        soup = BeautifulSoup(html.content, 'html.parser')

        table = soup.find('table')
        if len(table.find_all('tr')) > 3:
            # jugador(es) encontrado(s)
            query_data = table.find_all('tr')
            role = query_data[0].th.get_text()[6:query_data[0].th.get_text().find(';')]
            total_games = query_data[1].th.get_text()[20:query_data[1].th.get_text().find('To') - 1]
            all_players = query_data[3:]
            player_list = []
            for player in all_players:
                data = player.find_all('td')
                player_info = {
                    'name': data[1].get_text(),
                    'position': position,
                    'games_played': f'{data[2].get_text()}/{total_games}'
                }
                player_list.append(player_info)

            return player_list

    def get_players_in_team(self):
        """Retorna todos los jugadores de un equipo, incluidos suplentes"""

        positions = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
        roster = []
        for position in positions:
            roster.append(self.get_players_by_position(position))

        return roster

    def get_team_champions(self):
        url = ""

    def __init__(self, league, query):
        global LEAGUE, YEAR, SPLIT
        YEAR = '2020'  # Constante
        SPLIT = 'Summer'  # Constante
        LEAGUE = league
        self.query = query


class WinrateData:
    """Esta clase contendrá los datos de los winrates de los campeones"""

    def get_champ_icon(self):
        img = self.structure.find('div', class_='champion-stats-header-info__image').find('img')['src'][2:-32]
        return f"https://{img}"

    def get_champ_stats(self):
        patch = self.structure.find('div', class_="champion-stats-header-version")
        if patch:
            info = {'patch info': patch.get_text().strip()}
            raw_data = self.structure.find('div', class_='champion-box-content')
            champ_rates = raw_data.find_all('div', class_='champion-stats-trend-rate')
            info['winrate'] = champ_rates[0].get_text().strip()
            info['playrate'] = champ_rates[1].get_text().strip()
            return info

        else:
            return None

    def __init__(self, **kwargs):
        # Diccionario para saber a qué linea nos referimos, si es el caso

        if 'champ' in kwargs:
            # Si entra aquí, debemos buscar por campeón
            url = f"https://lan.op.gg/champion/{kwargs['champ']}/statistics/{kwargs['lane']}"
            html = requests.get(url=url)
            self.structure = BeautifulSoup(html.content, 'html.parser')
        else:
            # Si entra aquí, debemos buscar por línea
            url = 'https://lan.op.gg/champion/statistics'
            html = requests.get(url)
            self.structure = BeautifulSoup(html.content, 'html.parser')
            self.table = self.structure.find_all('div', class_='tabItems')
            print(self.table[1])


class RuneData:

    def __init__(self, champ_name, role=None):

        if role:
            self.url = f"https://u.gg/lol/champions/{champ_name}/build?role={role}"
        else:
            self.url = f"https://u.gg/lol/champions/{champ_name}/build"

        self.data = BeautifulSoup(requests.get(self.url).content, 'html.parser')

        # Verificar que lo que buscamos existe y tiene sentido
        # Intentamos buscar los datos

        try:
            # Si funciona bien, tendremos un objeto con todos los datos correctamente
            self.rune_data = self.get_runes()
            self.champ_name = self.get_champion_name()
            self.role = self.get_role()
            self.icon = self.get_champion_icon()
            self.patch = self.get_current_patch()
            self.total_matches = self.get_total_games()
            self.winrate = self.get_runeset_winrate()
            self.runeset_games = self.get_runeset_games()
            self.low_sample_rate = self.check_low_sample_rate()

        # Si no funciona (Campeón o rol incorrecto) obtendremos un NoneType, por lo cual nuestro objeto no servirá
        except AttributeError:
            self.rune_data = None
            print("Error durante la búsqueda de datos")

    def get_runes(self):

        # Obtenemos el divisor principal que contiene las runas
        rune_container = self.data.find('div', class_='grid-block runes')

        recommended_runes = []

        # Obtenemos el contenedor de los árboles de runas principal, secundario, y los shards
        rune_data = rune_container.find('div', class_='rune-trees-container')

        # Revisamos todas las ramas en el árbol
        for rune_tree in rune_data.find_all('div', class_='path-runes'):

            # Guardamos el nombre del árbol (Dominación, precisión, etc)
            chosen_path = rune_tree.find('div', class_='path-main').div.get_text()

            # Lista que contendrá las selecciones en el árbol
            runes_in_path = []

            # Buscamos entre las selecciones de la rama
            for rune in rune_tree.find_all('div', class_='perk perk-active'):
                runes_in_path.append(rune.img['alt'])

            # Metemos una tupla que contiene el nombre de la rama y las runas en la rama
            recommended_runes.append((chosen_path, runes_in_path))

        # Por último, debemos meter los fragmentos de runa en la lista

        # Necesitamos un diccionario para traducir imágenes a Texto de runas

        fragmentos_texto = {
            'AdaptiveForce': 'Fuerza Adaptiva',
            'AttackSpeed': 'Velocidad de Ataque',
            'CDRScaling': 'Reducción de Enfriamiento',
            'Armor': 'Armadura',
            'HealthScaling': 'Vida por Nivel',
            'MagicRes': 'Resistencia mágica'
        }

        # Lista que contendrá los fragmentos
        frags = []

        for shard in rune_data.find_all('div', class_='shard shard-active'):
            for key in fragmentos_texto:
                if key in shard.img['src']:
                    frags.append(fragmentos_texto[key])
                    break

        recommended_runes.append(('Fragmentos', frags))

        return recommended_runes

    def get_champion_name(self):
        name_holder = self.data.find('span', class_='champion-name')
        return name_holder.get_text()

    def get_role(self):
        role_holder = self.data.find('span', class_='champion-title')
        position = role_holder.get_text().split()[-1]
        return position

    def get_champion_icon(self):
        img_holder = self.data.find('img', class_='champion-image')
        return img_holder['src']

    def get_current_patch(self):
        patch_holder = self.data.find('span', class_='Select-value-label')

        return patch_holder.get_text()

    def get_total_games(self):
        match_holder = self.data.find('div', class_='matches')
        value = int(match_holder.div.get_text().replace(',', ''))
        return value

    def get_runeset_winrate(self):
        header = self.data.find('div', class_='grid-block runes').div
        percentage = header.find('span', class_='percentage').get_text()[:-1]

        return percentage

    def get_runeset_games(self):
        header = self.data.find('div', class_='grid-block runes').div
        games = header.find_all('span')[-1].get_text()

        game_num = games.split(' ')[0][1:]
        return game_num

    def check_low_sample_rate(self):
        warnings = self.data.find_all('div', class_='ugg-alert')

        return len(warnings) > 0


class BuildData:

    def __init__(self, champ_name, role=None):

        if role:
            self.url = f"https://lan.op.gg/champion/{champ_name}/statistics/{role}/item"
        else:
            self.url = f"https://lan.op.gg/champion/{champ_name}/statistics/redirection/item"

        self.data = BeautifulSoup(requests.get(self.url).content, 'html.parser')

        # Verificar que lo que buscamos existe y tiene sentido
        # Intentamos buscar los datos

        try:
            # Si funciona bien, tendremos un objeto con todos los datos correctamente
            self.champ_name = self.get_champion_name()
            self.role = self.get_role()
            self.icon = self.get_champion_icon()
            self.patch = self.get_current_patch()
            self.starter_items = self.get_starting_item_data()
            self.core_items = self.get_core_item_data()
            self.boots = self.get_boots_data()

        # Si no funciona (Campeón o rol incorrecto) obtendremos un NoneType, por lo cual nuestro objeto no servirá
        except AttributeError:

            self.starter_items = None
            self.core_items = None
            self.boots = None
            print("Error durante la búsqueda de datos")

    def get_starting_item_data(self):

        starting_item_container = self.data.find_all('div', class_='champion-box')[2].div

        # Lista que contendrá la información de las builds
        starter_builds = []
        """La lista estará formateada en elementos de truplas (thruples) tal que la primera posición será una lista, 
        la segunda una cadena (Pickrate%) y la tercera una cadena (Winrate%)"""

        for item_row in starting_item_container.find('tbody').find_all('tr')[:3]:
            item_list = item_row.td.ul
            build_items = []

            for item in item_list.find_all('li'):

                # Asumimos que el objeto es un item
                try:
                    build_items.append(self.find_item_in_string(item['title']))

                # De lo contrario, continuamos
                except KeyError:
                    continue

            # Hallamos y parseamos el pickrate y el winrate
            pickrate = item_row.find_all('td')[1].get_text().strip().split('%')[0]
            winrate = item_row.find_all('td')[2].get_text().strip().split('%')[0]

            starter_builds.append((build_items, pickrate, winrate))

        return starter_builds

    def get_core_item_data(self):
        core_item_container = self.data.find_all('div', class_='champion-box')[0].div

        # Lista que contendrá la información de las builds
        core_builds = []
        """La lista estará formateada en elementos de truplas (thruples) tal que la primera posición será una lista, 
        la segunda una cadena (Pickrate%) y la tercera una cadena (Winrate%)"""

        for item_row in core_item_container.find('tbody').find_all('tr')[:3]:
            item_list = item_row.td.ul
            build_items = []

            for item in item_list.find_all('li'):

                # Asumimos que el objeto es un item
                try:
                    build_items.append(self.find_item_in_string(item['title']))

                # De lo contrario, continuamos
                except KeyError:
                    continue

            # Hallamos y parseamos el pickrate y el winrate
            pickrate = item_row.find_all('td')[1].get_text().strip().split('%')[0]
            winrate = item_row.find_all('td')[2].get_text().strip().split('%')[0]

            core_builds.append((build_items, pickrate, winrate))

        return core_builds

    def get_champion_name(self):
        name_holder = self.data.find('h1', class_='champion-stats-header-info__name')
        return name_holder.get_text()

    def get_role(self):
        role_holder = self.data.find('li',
                                     class_='champion-stats-header__position champion-stats-header__position--active'
                                     )

        position = role_holder.find('span', class_='champion-stats-header__position__role').get_text()
        return position

    def get_champion_icon(self):
        img_holder = self.data.find('div', class_='champion-stats-header-info__image')
        return 'https:' + img_holder.img['src']

    def get_current_patch(self):
        patch_holder = self.data.find('div', class_='champion-stats-header-version')

        patch_data = patch_holder.get_text().strip()

        patch_number = patch_data.split(" : ")[-1]

        return patch_number

    def find_item_in_string(self, text):
        """En OP.GG los items están super convolucionados en una cadena larguísima con un montón de tags HTML que no
        sirven ni para lavarse el qlo, así que debemos hallar el nombre del item entre el desastre :V"""

        try:
            item_name = re.search('>([^<>+:]+?)<', text).group(1)

        except AttributeError:
            item_name = None

        return item_name

    def get_boots_data(self):
        boot_item_container = self.data.find_all('div', class_='champion-box')[1].div

        # Lista que contendrá la información de las builds
        boot_options = []
        """La lista estará formateada en elementos de truplas (thruples) tal que la primera posición será una lista, 
        la segunda una cadena (Pickrate%) y la tercera una cadena (Winrate%)"""

        for item_row in boot_item_container.find('tbody').find_all('tr')[:3]:

            boot = item_row.td.div.span.get_text()

            # Hallamos y parseamos el pickrate y el winrate
            pickrate = item_row.find_all('td')[1].get_text().strip().split('%')[0]
            winrate = item_row.find_all('td')[2].get_text().strip().split('%')[0]

            boot_options.append((boot, pickrate, winrate))

        return boot_options


# Debugging
if __name__ == '__main__':
    runes = BuildData('senna')
    print(runes.boots)

