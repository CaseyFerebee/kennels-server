import json
import sqlite3
from models import Animal
from .location_requests import get_single_location
from .customer_requests import get_single_customer

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "status": "Recreation",
        "breed": "Dalmation",
        "location_id": 4,
        "customer_id": 1,
    },
    {
        "id": 2,
        "name": "Jax",
        "status": "Treatment",
        "breed": "Beagle",
        "location_id": 1,
        "customer_id": 1,
    },
    {
        "id": 3,
        "name": "Falafel",
        "status": "Treatment",
        "breed": "Siamese",
        "location_id": 4,
        "customer_id": 2,
    },
    {
        "id": 4,
        "name": "Doodles",
        "status": "Kennel",
        "breed": "Poodle",
        "location_id": 3,
        "customer_id": 1,
    },
    {
        "id": 5,
        "name": "Daps",
        "status": "Kennel",
        "breed": "Boxer",
        "location_id": 2,
        "customer_id": 2,
    },
    {
        "id": 6,
        "name": "Cleo",
        "status": "Kennel",
        "breed": "Poodle",
        "location_id": 2,
        "customer_id": 2,
    },
    {
        "id": 7,
        "name": "Popcorn",
        "status": "Kennel",
        "breed": "Beagle",
        "location_id": 3,
        "customer_id": 2,
    },
    {
        "id": 8,
        "name": "Curly",
        "status": "Treatment",
        "breed": "Poodle",
        "location_id": 4,
        "customer_id": 2,
    }
]


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.location_id,
            a.customer_id
        FROM animal a
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['status'],
                            row['breed'], row['location_id'],
                            row['customer_id'])

            animals.append(animal.__dict__)

    return animals


# Function with a single parameter


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return animal.__dict__


def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal


def delete_animal(id):
    # Initial -1 value for animal index, in case one isn't found
    animal_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Store the current index.
            animal_index = index

    # If the animal was found, use pop(int) to remove it from list
    if animal_index >= 0:
        ANIMALS.pop(animal_index)


def update_animal(id, new_animal):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Update the value.
            ANIMALS[index] = new_animal
            break
