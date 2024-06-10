#!/usr/bin/env python
import argparse
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
wishlist_count = user_count * 10


def generate_time(end_time=None):
    start = datetime.now()
    end = end_time or (datetime.now() - timedelta(days=365))
    return not_naive(start + (end - start) * random.random())


def not_naive(time):
    return str(time).replace(" ", "T")[:-3] + "Z"


def pseudorandom(M, N, max):
    tups = set()
    while (len(tups) <= max):
        tup = (random.randrange(1, M), random.randrange(1, N))
        tups.add(tup)
    return list(tups)


def generate_product(test: bool):
    for i in range(1, product_count + 1):
        name = faker.word()
        fixture.append(
            {
                'model': 'core.Product',
                'pk': i,
                'fields': {
                    'name': f'test{i}',
                    'desc': f'testtesttest{i}',
                    'SKU': f'{i}te{faker.random_number(5)}',
                    'category':
                        random.randrange(1, product_category_count + 1),
                    'inventory': i,
                    'price': round(random.uniform(0, 100), 2),
                    'discount': random.choice(
                        [None, random.randrange(1, discount_count + 1)]),
                    'created_at': generate_time()
                } if test else {
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


def generate_product_category(test: bool):
    for i in range(1, product_category_count + 1):
        fixture.append(
            {
                'model': 'core.ProductCategory',
                'pk': i,
                'fields': {
                    'name': f'test{i}',
                    'desc': f'testtesttest{i}',
                    'created_at': generate_time()
                } if test else {
                    'name': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'created_at': generate_time()
                }
            }
        )


def generate_product_inventory(test: bool):
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


def generate_discount(test: bool):
    for i in range(1, discount_count + 1):
        fixture.append(
            {
                'model': 'core.Discount',
                'pk': i,
                'fields': {
                    'name': f'test{i}',
                    'desc': f'testtesttest{i}',
                    'discount_percent': random.randrange(1, 101),
                    'is_active': bool(random.getrandbits(1)),
                    'created_at': generate_time()
                } if test else {
                    'name': faker.word(),
                    'desc': faker.text(max_nb_chars=100),
                    'discount_percent': random.randrange(1, 101),
                    'is_active': bool(random.getrandbits(1)),
                    'created_at': generate_time()
                }
            }
        )


def generate_user(test: bool):
    for i in range(1, user_count + 1):
        fixture.append(
            {
                'model': 'users.ECommerceUser',
                'pk': i,
                'fields': {
                    'username': f'test{i}',
                    'email': f'test{i}@email.com',
                    'password': hasher.encode(f'TestTest{i}', str(i)),
                    'first_name': f'Test{i}',
                    'last_name': f'Test{i}'
                } if test else {
                    'username': faker.user_name(),
                    'email': faker.email(),
                    'password': hasher.encode(faker.password(), str(i)),
                    'first_name': faker.first_name(),
                    'last_name': faker.last_name()
                }
            }
        )


def generate_useraddress(test: bool):
    for i in range(1, user_count + 1):
        fixture.append(
            {
                'model': 'users.UserAddress',
                'pk': i,
                'fields': {
                    'user': i,
                    'address_line1': f'test {i}',
                    'address_line2': f'test {i}',
                    'city': f'Test{i}',
                    'postal_code': i,
                    'country': f'Test{i}',
                    'telephone': faker.phone_number(),
                    'mobile': faker.phone_number()
                } if test else {
                    'user': i,
                    'address_line1': faker.address(),
                    'address_line2': faker.address(),
                    'city': faker.city(),
                    'postal_code': faker.postalcode(),
                    'country': faker.country_code(),
                    'telephone': faker.phone_number(),
                    'mobile': faker.phone_number()
                }
            }
        )


def generate_review(test: bool):
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
                    'title': f'test{1}',
                    'desc': f'testtesttesttesttest{1}',
                    'rating': random.randrange(1, 6),
                    'created_at': generate_time()
                } if test else {
                    'user': user,
                    'product': product,
                    'title': faker.text(max_nb_chars=100),
                    'desc': faker.text(max_nb_chars=300),
                    'rating': random.randrange(1, 6),
                    'created_at': generate_time()
                }
            }
        )


def generate_wishlist(test: bool):
    rand_id = pseudorandom(user_count, product_count, wishlist_count)
    for i in range(1, wishlist_count + 1):
        user, product = rand_id[i-1]
        fixture.append(
            {
                'model': 'users.Review',
                'pk': i,
                'fields': {
                    'user': user,
                    'product': product,
                    'created_at': generate_time()
                }
            }
        )


def run_generate(test: bool = False):
    path = ('./fixtures/test_fixture.json' if test
            else './fixtures/fixture.json')

    generate_product(test)
    generate_product_category(test)
    generate_product_inventory(test)
    generate_discount(test)
    generate_review(test)
    generate_user(test)
    generate_useraddress(test)

    with open(path, 'w') as outfile:
        json.dump(fixture, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate fixtures')
    parser.add_argument('--test', '-t', dest='test',
                        action='store_true', default=False)
    args = parser.parse_args()

    run_generate(args.test)
