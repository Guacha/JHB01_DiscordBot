from bs4 import BeautifulSoup
import requests
import re


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

                builds[cont] = build # Ponemos la build en el espacio correspondiente del dict
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
                runes_in_path = [] # Esto guradará una tupla con las runas individuales de la rama
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
        print(html)
        self.structure = BeautifulSoup(html.content, 'html.parser')
        if len(self.structure.find_all('div', class_="large-header")) != 0:
            print("Ese champiñón no existe")
        else:
            self.builds = self.arr_builds()
            self.runes = self.arr_runes()
            self.champ_icon = self.get_champ_icon()
            self.champion = self.get_champ_name()
            self.patch = self.get_patch()

