#!/usr/bin/env python
from datetime import datetime, timedelta
import json
import random

from django.contrib.auth.hashers import PBKDF2PasswordHasher
import faker


hasher = PBKDF2PasswordHasher()
faker = faker.Faker()

fixture = []
discount_count = 5
product_category_count = 10
product_count = 100
user_count = 20
review_count = user_count * 50


def generate_time(end_time=None):
    start = datetime.now()
    end = end_time or (datetime.now() - timedelta(days=365))
    return not_naive(start + (end - start) * random.random())


def not_naive(time):
    return str(time).replace(" ", "T")[:-3] + "Z"


def pseudorandom(M, N, max):
    tups = []
    i = 1
    while (True):
        tup = (random.randrange(1, M), random.randrange(1, N))
        tups.append(tup)
        if i % max == 0:
            tups = list(set(tups))
            i = len(tups)
            print(i)
            if i == max:
                break
        i += 1
    return tups


def generate_product():
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


def generate_product_category():
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


def generate_product_inventory():
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


def generate_discount():
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


def generate_review():
    rand_id = pseudorandom(user_count, product_count, review_count)
    for i in range(1, review_count + 1):
        user, product = rand_id[i-1]
        fixture.append(
            {
                'model': 'users.Review',
                'pk': i,
                'fields': {
                    'user': user,
                    'product': product,
                    'title': faker.text(max_nb_chars=100),
                    'desc': faker.text(max_nb_chars=300),
                    'rating': random.randrange(1, 6),
                    'created_at': generate_time()
                }
            }
        )


def generate_user():
    for i in range(1, user_count + 1):
        fixture.append(
            {
                'model': 'users.ECommerceUser',
                'pk': i,
                'fields': {
                    'username': faker.user_name(),
                    'email': faker.email(),
                    'password': hasher.encode(faker.password(), str(i)),
                    'first_name': faker.first_name(),
                    'last_name': faker.last_name()
                }
            }
        )


def generate_useraddress():
    for i in range(1, user_count + 1):
        fixture.append(
            {
                'model': 'users.UserAddress',
                'pk': i,
                'fields': {
                    'user': i,
                    'address_line1': faker.address(),
                    'address_line2': faker.address(),
                    'city': faker.city(),
                    'postal_code': faker.postalcode(),
                    'country': faker.country(),
                    'telephone': faker.phone_number(),
                    'mobile': faker.phone_number()
                }
            }
        )


generate_product()
generate_product_category()
generate_product_inventory()
generate_discount()
generate_review()
generate_user()
generate_useraddress()

with open('./fixtures/fixture.json', 'w') as outfile:
    json.dump(fixture, outfile)
