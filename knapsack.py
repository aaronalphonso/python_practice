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
from random import randrange, seed


# Use a namedtuple to represent each item of the list
from utils import timed_block

Item = namedtuple('Item', ['name', 'calories', 'value'])


def generate_knapsack_data(items_count):
    """A helper function to generate a random list of items"""
    items = []
    # Seed the data for reproducible results (Have chosen a seed where exhaustive tree is better than greedy, just to
    # illustrate that greedy can sometimes miss the globally optimal solution)
    seed(4)
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


def exhaustive_tree(items, calorie_limit):
    """The exhaustive approach to filling the knapsack. This approach calculates every possible combination of filling
    the knapsack and selects the most valuable combination.

    Approach: For every item in the list, diverge into two sub-trees, one in which the item is selected, and the other
    in which the item is discarded. Do this recursively to generate the exhaustive tree of all possible combinations.
    Then compare each of the two branches at every node and return the combination which has a higher value

    :param items: The list of all available items
    :param calorie_limit: The max limit of calories within which items are to be selected

    :returns: The selected list of items
    """
    # If there are no more items to consider, return an empty selection
    if not items:
        return []

    # Pick the first item from the list. This is the item we will consider.
    item = items[0]
    remaining_items = items[1:]

    # Diverge into two branches, one in which the item is selected and another in which the item is discarded.
    # Keep branching out recursively at each item. This will generate every possible combination.

    # Branch A - The branch in which the item is selected
    # We only want to calculate the branch recursively if adding the item, doesn't overflow the knapsack capacity
    if item.calories <= calorie_limit:
        # Assuming the item is selected, calculate the sub-problem solution
        choice_a = [item] + exhaustive_tree(items=remaining_items,
                                            calorie_limit=calorie_limit - item.calories)
    else:
        # If it does overflow, we skip the recursive calculations for the subtree.
        choice_a = []

    # Branch B - The branch in which the item is discarded
    choice_b = exhaustive_tree(items=remaining_items,
                               calorie_limit=calorie_limit)

    # Compare the selection from the two branches and return the more efficient solution.
    return max(choice_a, choice_b, key=lambda x: sum(i.value for i in x))


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

    for algorithm in (greedy, exhaustive_tree):
        print("\n\n")
        print("{} approach".format(algorithm.__name__))
        with timed_block(algorithm.__name__):
            selection = algorithm(items, calorie_limit=1500)
        display_items(selection)


if __name__ == '__main__':
    main()
