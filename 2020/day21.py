from functools import reduce
from collections import Counter


def parse_food(line):
    a, b = line.split(" (contains ")
    ingredients = a.split(" ")
    allergens = b[:-1].split(", ")
    return ingredients, allergens


with open("day21.txt") as f:
    foods = [parse_food(line.strip()) for line in f.readlines()]


ingredients_by_allergen = {}
for ingredients, allergens in foods:
    for allergen in allergens:
        try:
            ingredients_by_allergen[allergen].append(set(ingredients))
        except KeyError:
            ingredients_by_allergen[allergen] = [set(ingredients)]


possible_ingredients_by_allergen =  {
    allergen: reduce(set.intersection, ingredients)
    for allergen, ingredients in ingredients_by_allergen.items()
}

matched_ingredients = reduce(set.union, possible_ingredients_by_allergen.values())
ingredient_by_allergen = {}

while possible_ingredients_by_allergen:
    matches = {
        allergen: list(ingredients)[0]
        for allergen, ingredients in possible_ingredients_by_allergen.items()
        if len(ingredients) == 1
    }
    for allergen, ingredient in matches.items():
        ingredient_by_allergen[allergen] = ingredient
        possible_ingredients_by_allergen = {
            allergen: ingredients - {ingredient}
            for allergen, ingredients in possible_ingredients_by_allergen.items()
            if len(ingredients) != 1
        }

all_ingredients = [ingredient for food in foods for ingredient in food[0]]
left_ingredients = set(all_ingredients) - matched_ingredients

print(sum(
    count
    for ingredient, count in Counter(all_ingredients).items()
    if ingredient in left_ingredients
))

print(",".join([
    ingredient
    for _, ingredient in sorted(ingredient_by_allergen.items(), key=lambda x: x[0])
]))
