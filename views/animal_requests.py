import json
import sqlite3
from models import Animal

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

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:

            animal = Animal(row['id'], row['name'], row['status'],
                            row['breed'], row['location_id'],
                            row['customer_id'])

            animals.append(animal.__dict__)

    return animals


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
            a.status,
            a.breed,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['status'],
                            data['breed'], data['location_id'],
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
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))



def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_animal_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
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
        FROM Animal a
        WHERE a.location_id = ?
        """, ( location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['status'],
                            row['breed'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)
    return animals

def get_animal_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
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
        FROM Animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['status'],
                            row['breed'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)
    return animals
