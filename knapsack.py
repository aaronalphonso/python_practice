"""
Solutions to the Knapsack Problem (https://en.wikipedia.org/wiki/Knapsack_problem)

General Knapsack Problem:
    Given a list of items (having some weight and value) and a knapsack with a fixed capacity, the problem is to try to
    obtain the most valuable items without going over the knapsack weight limit.

Our Specific Knapsack Problem:
    We use calories instead of weight, the context of the problem is: You are at a restaurant trying to eat the best
    food that you can without going over your daily allotted calorie limit.
"""
from collections import namedtuple
from random import randrange
from typing import List


# Use a namedtuple to represent each item of the list
from utils import timed_block

Item = namedtuple('Item', ['name', 'calories', 'value'])


def generate_knapsack_data(items_count):
    """A helper function to generate a random list of items"""
    items = []
    for _ in range(items_count):
        item = Item(name=f"item{_}", calories=randrange(100, 1000, 50), value=randrange(1, 10))
        items.append(item)
    return items


def greedy(items, calorie_limit):
    """The greedy approach to filling the knapsack. Orders the items by value density (i.e. value/calorie), and then
    iterates through the entire list, adding each item to the knapsack if there is space available and moving on to the
    next item if no space available.

    :param items: The list of all available items
    :param calorie_limit: The max limit of calories within which items are to be selected

    :returns: The selected list of items
    """
    # Sort the items in descending order of density (values per calorie)
    items = sorted(items, key=lambda x: x.value/x.calories, reverse=True)

    # Maintain a list of selected items and the remaining_calorie_count so far
    selected = []
    remaining_calorie_count = calorie_limit

    # Iterate through the items and add the item to the knapsack if there is space available
    for item in items:
        if item.calories <= remaining_calorie_count:
            selected.append(item)
            remaining_calorie_count -= item.calories

    return selected


def display_items(items):
    """Prints the list of items with their calories and value along with a total at the end"""
    width = 49

    print("-" * width)
    header_template = "{:^10} - {:^10} - {:^10} - {:^10}"
    print(header_template.format("Name", "Calories", "Value", "Density"))
    print("-" * width)

    line_template = "{:^10} - {:^10} - {:^10} - {:^10.1%}"
    total_calories = 0
    total_value = 0
    for item in items:
        total_calories += item.calories
        total_value += item.value
        print(line_template.format(item.name, item.calories, item.value, item.value / item.calories))

    print("-" * width)
    print(line_template.format("Total", total_calories, total_value, total_value / total_calories))


def main():
    """Triggers the execution"""
    items = generate_knapsack_data(items_count=50)
    display_items(items)

    for algorithm in (greedy, ):
        print("\n\n")
        print("{} approach".format(algorithm.__name__))
        with timed_block(algorithm.__name__):
            selection = algorithm(items, calorie_limit=1500)
        display_items(selection)


if __name__ == '__main__':
    main()
