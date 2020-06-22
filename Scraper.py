from bs4 import BeautifulSoup
import requests
import re
import math


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
        return update[17:]

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


class ChampionData:
    """Esta clase contiene la información organizada del campeón que se le otorgó de la página champion.gg
    todo: runes, matchups, winrates"""

    def arr_builds(self):
        """Este metodo obtiene los arreglos de builds y objetos iniciales del champ, y retorna un diccionario con los
        items correspondientes según winrate, u objetos más comunes"""

        # Obtenemos los datos en bruto de la página web a la que se le hizo scraping
        raw_data = self.structure.find_all('div', class_="build-wrapper")

        # Preparamos un diccionario vacío que contendrá las 4 builds, organizadas como se ven en la documentacion
        builds = {
            1: None,  # Build completa más común
            2: None,  # Build completa con más winrate
            3: None,  # Items iniciales más comunes
            4: None  # Items iniciales con más winrate
        }

        cont = 1  # Contador externo para iterar el diccionario
        if len(raw_data) == 4:
            for dataset in raw_data:
                # Obtenemos los items de una de las 4 builds posibles
                items = dataset.find_all('a')
                build = []  # Lista que contendrá los items de la build
                for item in items:
                    # Agregamos el item a la lista build
                    build.append(item['href'][38:])  # Quitamos el texto inutil del principio

                builds[cont] = build  # Ponemos la build en el espacio correspondiente del dict
                cont += 1

        return builds

    def arr_runes(self):
        """Este método obtiene los árboles de runas más comunes y de mayor winrate del campeón dado y
        retorna un diccionario que los contiene"""
        # Seleccionamos la sección de la página web que contiene
        raw_data = self.structure.find_all('div', class_=re.compile("RuneBuilder__PathColumn"))

        # Creamos el diccionario que vamos a retornar
        runes = {
            1: None,
            2: None
        }

        # Variable que contiene en qué árbol estamos
        arbol = 1  # 1 == Más común, 2 == Mayor Winrate
        rune_tree = []  # Lista que contendrá un árbol completo de runas

        # Contador para las ramas que llevemos, en total, en la página hay 2 árboles == 4 ramas
        ramas = 0

        # Buscamos en cada espacio de árbol de runas
        for dataset in raw_data:
            # Seleccionamos las ramas
            runepaths = dataset.find_all('section', id=re.compile("path"))

            for path in runepaths:
                runes_in_path = []  # Esto guradará una tupla con las runas individuales de la rama
                choices = path.find_all('div', class_=re.compile('Description__Block'))

                # Para saber si vamos en el título del árbol o en las runas, usamos un contador
                cont = 1
                chosen_path = ""  # Título del árbol (Inspiración, precisión, etc)

                # Iteramos por cada selección de runa individual
                for choice in choices:
                    if cont == 1:
                        chosen_path = choice.get_text().strip()  # Obtiene el nombre del título sin los \n
                        cont += 1
                    else:
                        """Normalmente el nombre obtenido de la runa tiene un montón de whitespace, 
                        así que debemos quitarlo, además, viene con una descripción que sobra, entonces
                        tomamos solo el primer elemento de una lista al separarlo por \n"""
                        runes_in_path.append(choice.get_text().rstrip().lstrip().split('\n')[0])

                rune_tree.append((chosen_path, runes_in_path))  # Metemos el título y la lista de runas como tupla
                ramas += 1

                # Si ya llegamos a la segunda rama, quiere decir que tenemos un árbol completo
                if ramas == 2:
                    runes[arbol] = rune_tree
                    ramas = 0
                    arbol = 2
                    rune_tree = []
        return runes

    def get_champ_icon(self):
        img = self.structure.find('img', class_='champ-img')
        return f"https://{img['src'][2:]}"

    def get_champ_name(self):
        name = self.structure.find('h1')
        return name.get_text()

    def get_patch(self):
        analysis_holder = self.structure.find('div', class_='analysis-holder')
        return analysis_holder.find_next('strong').get_text()

    def __init__(self, champion):
        self.builds = None
        self.runes = None
        self.matchups = None
        self.winrates = None
        self.champion = None
        self.champ_icon = None
        self.patch = None
        self.url = f"https://champion.gg/champion/{champion}"
        html = requests.get(self.url)
        self.structure = BeautifulSoup(html.content, 'html.parser')
        if len(self.structure.find_all('div', class_="large-header")) != 0:
            print("Ese champiñón no existe")
        else:
            self.builds = self.arr_builds()
            self.runes = self.arr_runes()
            self.champ_icon = self.get_champ_icon()
            self.champion = self.get_champ_name()
            self.patch = self.get_patch()
