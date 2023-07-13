class Animal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, species, breed, status, location_id, customer_id, employee_id):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id
        self.employee_id = employee_id



