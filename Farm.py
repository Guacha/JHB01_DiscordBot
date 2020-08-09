import random
from FireHandler import Database


class Farm:

    def __init__(self, database=None):
        print("Cargando módulo de granja")

        self.database: Database = database

        self.common_species = {
            'Hormiga': ':ant:',
            'Mariposa': ':butterfly:',
            'Gusano de Seda': ':bug:',
            'Araña de Seda': ':spider:',
            'Abeja': ':bee:'
        }

        self.uncommon_species = {
            'Vaca': ':cow2:',
            'Cerdo': ':pig2:',
            'Oveja': ':sheep:',
            'Camarón': ':shrimp:',
            'Cabra': ':goat:',
            'Pollo': ':rooster:',
        }

        self.rare_species = {
            'Langosta': ':lobster:',
            'Caballo': ':horse:',
            'Calamar': ':squid:',
            'Rinocetonte': ':rhino:',
            'Elefante': ':elephant:'
        }

        self.epic_species = {
            'Pavo Real': ':peacock:',
            'Flamingo': ':flamingo:',
            'Cisne': ':swan:',
            'Cocodrilo': ':cocodrile:'
        }

        self.mythical_species = {
            'Dragon': ':dragon:',
            'T-Rex': ':t_rex:',
            'Unicornio': ':unicorn:',

        }

        self.upgrades = {
            'Mejora de Exploración': ':seedling:',
            'Resistencia al Fuego': ':fire_extinguisher:',
            'Resistencia a Inundaciones': ':ocean:',
            'Bunker Nuclear': ':radioactive:',
            'Mejora de PeneIngresos': ':moneybag:'
        }

        self.rarities = {
            'common': ':regional_indicator_d:',
            'uncommon': ':regional_indicator_c:',
            'rare': ':b:',
            'epic': ':a:',
            'mythical': ':u6709:',
        }

        print("Módulo de granja cargado exitosamente")

    def get_farm(self, guid, uuid):
        player_farm = self.database.get_player_farm(guid, uuid)

        classes = ['common', 'uncommon', 'rare', 'epic', 'mythical']

        if player_farm != {}:

            res = {
                'animals': {},
                'upgrades': {}
            }
            for rarity in classes:
                try:
                    res['animals'][rarity] = player_farm['animals'][rarity]

                except KeyError:
                    res['animals'][rarity] = {}

            for upgrade in self.upgrades:
                try:
                    res['upgrades'][upgrade] = player_farm['upgrades'][upgrade]

                except KeyError:
                    res['upgrades'][upgrade] = 0

            res['points'] = player_farm['points']

            return res

        else:
            self.database.initialize_player_farm(guid, uuid)

            return {
                'animals': {
                    'common': {},
                    'uncommon': {},
                    'rare': {},
                    'epic': {},
                    'mythical': {}
                },
                'upgrades': {
                    'Mejora de Exploración': 0,
                    'Resistencia al Fuego': 0,
                    'Resistencia a Inundaciones': 0,
                    'Bunker Nuclear': 0,
                    'Mejora de PeneIngresos': 0
                },
                'points': 0

            }

    def wild_hunt(self, guid, uuid):
        player_farm = self.get_farm(guid, uuid)

        exp_upgrade = player_farm['upgrades']['Mejora de Exploración']

        prob = (80, 60, 20*(exp_upgrade/4), 8*(exp_upgrade/4), 1*(exp_upgrade/4))

        opts = (
            ('common', self.common_species),
            ('uncommon', self.uncommon_species),
            ('rare', self.rare_species),
            ('epic', self.epic_species),
            ('mythical', self.mythical_species)
        )

        sel = random.choices(opts, weights=prob)

        return sel[0]

    def get_emoji(self, rarity, animal):

        if rarity == 'common':
            return self.common_species[animal]
        elif rarity == 'uncommon':
            return self.uncommon_species[animal]
        elif rarity == 'rare':
            return self.rare_species[animal]
        elif rarity == 'epic':
            return self.epic_species[animal]
        elif rarity == 'mythical':
            return self.mythical_species[animal]

    def get_species_amount(self, rarity):
        if rarity == 'common':
            return len(self.common_species)
        elif rarity == 'uncommon':
            return len(self.uncommon_species)
        elif rarity == 'rare':
            return len(self.rare_species)
        elif rarity == 'epic':
            return len(self.epic_species)
        elif rarity == 'mythical':
            return len(self.mythical_species)

    def grant_animal(self, guid, uuid, rarity, animal, amount):
        new_species = self.database.add_animal(guid, uuid, rarity, animal, amount)
        rarity_to_pts = {
            'common': 1,
            'uncommon': 2,
            'rare': 4,
            'epic': 16,
            'mythical': 256
        }
        self.database.give_farm_points(guid, uuid, rarity_to_pts[rarity], new_species=new_species)

    def upgrade_farm(self, guid, uuid, lvl, upgrade):
        self.database.upgrade_farm(guid, uuid, lvl, upgrade)


if __name__ == '__main__':
    farm = Farm(Database())

    print(farm.wild_hunt())
