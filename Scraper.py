from bs4 import BeautifulSoup
import requests
import re


class TournamentData:
    """Esta clase contendrá los queries de torneo que se necesiten de jugadores o posiciones"""
    YEAR = ""
    SPLIT = ""
    LEAGUE = ""

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



