import json
import sqlite3
from models import Animal, Location, Customer

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "status": "Recreation",
        "breed": "Dalmation",
        "location_id": 4,
        "customer_id": 1
    },
    {
        "id": 2,
        "name": "Jax",
        "status": "Treatment",
        "breed": "Beagle",
        "location_id": 1,
        "customer_id": 1
    },
    {
        "id": 3,
        "name": "Falafel",
        "status": "Treatment",
        "breed": "Siamese",
        "location_id": 4,
        "customer_id": 2
    },
    {
        "id": 4,
        "name": "Doodles",
        "status": "Kennel",
        "breed": "Poodle",
        "location_id": 3,
        "customer_id": 1
    },
    {
        "id": 5,
        "name": "Daps",
        "status": "Kennel",
        "breed": "Boxer",
        "location_id": 2,
        "customer_id": 2
    },
    {
        "id": 6,
        "name": "Cleo",
        "status": "Kennel",
        "breed": "Poodle",
        "location_id": 2,
        "customer_id": 2
    },
    {
        "id": 7,
        "name": "Popcorn",
        "status": "Kennel",
        "breed": "Beagle",
        "location_id": 3,
        "customer_id": 2
    },
    {
        "id": 8,
        "name": "Curly",
        "status": "Treatment",
        "breed": "Poodle",
        "location_id": 4,
        "customer_id": 2
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
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name AS location_name,
            l.address AS location_address,
            c.name AS customer_name,
            c.address AS customer_address,
            c.email AS customer_email,
            c.password AS customer_password
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id;
                """)

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['location_id'], row['customer_id'])

            # Create a Location instance from the current row
            location = Location(row['id'], row['location_name'], row['location_address'])

            customer = Customer(row['customer_id'], row['customer_name'], row['customer_address'], row['customer_email'], row['customer_password'])
            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__
            # Add the dictionary representation of the animal to the list
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
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name AS location_name,
            l.address AS location_address,
            c.name AS customer_name,
            c.address AS customer_address,
            c.email AS customer_email,
            c.password AS customer_password
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id
        WHERE a.id = ?;
        """, (id,))

        # Load the single result into memory
        data = db_cursor.fetchone()

        if data:
            # Create an animal instance from the current row
            animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

            # Add the location and customer details to the animal
            location = Location(data['location_id'], data['location_name'], data['location_address'])
            customer = Customer(data['customer_id'], data['customer_name'], data['customer_address'], data['customer_email'], data['customer_password'])
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            return animal.__dict__
        else:
            return None




def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id


    return new_animal


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
        """, (new_animal['name'], new_animal['status'],
              new_animal['breed'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

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
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name AS location_name,
            l.address AS location_address
        FROM Animal a
        JOIN Location l ON a.location_id = l.id
        WHERE a.location_id = ?
        """, (location_id,))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'], row['location_name'],
                            row['location_address'])
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
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM Animal a
        WHERE a.status = ?
        """, ( status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)
    return animals
