#!/usr/bin/env python
from datetime import datetime, timedelta
import json
import random

import faker


faker = faker.Faker()

discount_count = 5
product_category_count = 10
product_count = 100


def generate_time(end_time=None):
    start = datetime.now()
    end = end_time or (datetime.now() - timedelta(days=365))
    return not_naive(start + (end - start) * random.random())


def not_naive(time):
    return str(time).replace(" ", "T")[:-3] + "Z"


def generate_product():
    fixture = []
    for i in range(1, product_count + 1):
        name = faker.word()
        fixture.append(
            {
                'model': 'core.Product',
                'pk': i,
                'fields': {
                    'name': name,
                    'desc': faker.text(max_nb_chars=100),
                    'SKU': f'{i}{name[:2]}{faker.random_number(5)}',
                    'category':
                        random.randrange(1, product_category_count + 1),
                    'inventory': i,
                    'price': round(random.uniform(0, 100), 2),
                    'discount': random.choice(
                        [None, random.randrange(1, discount_count + 1)]),
                    'created_at': generate_time()
                }
            }
        )
    with open('./fixtures/product.json', 'w') as outfile:
        json.dump(fixture, outfile)


def generate_product_category():
    fixture = []
    for i in range(1, product_count + 1):
        fixture.append(
            {
                'model': 'core.ProductCategory',
                'pk': i,
                'fields': {
                    'name': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'created_at': generate_time()
                }
            }
        )
    with open('./fixtures/product_category.json', 'w') as outfile:
        json.dump(fixture, outfile)


def generate_product_inventory():
    fixture = []
    for i in range(1, product_count + 1):
        fixture.append(
            {
                'model': 'core.ProductInventory',
                'pk': i,
                'fields': {
                    'quantity': random.randrange(1000),
                    'created_at': generate_time()
                }
            }
        )
    with open('./fixtures/product_inventory.json', 'w') as outfile:
        json.dump(fixture, outfile)


def generate_discount():
    fixture = []
    for i in range(1, discount_count + 1):
        fixture.append(
            {
                'model': 'core.Discount',
                'pk': i,
                'fields': {
                    'name': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'discount_percent': random.randrange(1, 101),
                    'is_active': bool(random.getrandbits(1)),
                    'created_at': generate_time()
                }
            }
        )
    with open('./fixtures/discount.json', 'w') as outfile:
        json.dump(fixture, outfile)


generate_product()
generate_product_category()
generate_product_inventory()
generate_discount()
