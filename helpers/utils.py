import random

def generate_unique_email():
    return f"user{random.randint(100000, 999999)}@test.com"