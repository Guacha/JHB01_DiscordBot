import random


class Item:

    def __init__(self, item_name: str, item_description: str, item_cost: int, store_prob: float):
        self.name = item_name
        self.description = item_description
        self.cost = item_cost
        self.prob = store_prob

    @staticmethod
    def items_from_file(file_path):
        with open(file_path, 'r') as f:
            item_list = []
            for item in f.readlines():
                item_values = item.split(',')
                item_list.append(Item(item_values[0], item_values[1], int(item_values[2]), float(item_values[3])))

            return item_list

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}, Cost: {self.cost}, store probability: {self.prob}"


class Tienda:

    def __init__(self):
        self.__item_list = Item.items_from_file('./items.jhb')
        self.display_items: list[Item] = []
        self.reset_display_items()

    def reset_display_items(self):
        self.display_items = []
        for item in self.__item_list:
            if random.random() <= (item.prob/100):
                self.display_items.append(item)



if __name__ == '__main__':
    pass

