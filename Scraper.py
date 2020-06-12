from bs4 import BeautifulSoup
import requests


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

    def __init__(self, champion):
        self.builds = None
        self.runes = None
        self.matchups = None
        self.winrates = None
        self.champion = champion
        self.url = f"https://champion.gg/champion/{champion}"
        html = requests.get(self.url)
        print(html)
        self.structure = BeautifulSoup(html.content, 'html.parser')
        if len(self.structure.find_all('div', class_="large-header")) != 0:
            print("Ese champiñón no existe")
        else:
            self.builds = self.arr_builds()
