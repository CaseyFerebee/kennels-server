import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from views import (get_all_animals, get_single_animal, get_all_locations,
                   get_single_location, get_single_employee, get_all_employees,
                   get_single_customer, get_all_customers, get_customer_by_email, create_animal,
                   create_location, create_employee, create_customer, get_animal_by_status,
                   delete_animal, delete_customer, delete_employee,
                   delete_location, update_animal, update_customer,
                   update_location, update_employee, get_animal_by_location, get_employee_by_location)


class HandleRequests(BaseHTTPRequestHandler):
    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()

            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()

            elif resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customer_by_email(query['email'][0])

            if query.get('location_id') and resource == 'animals':
                response = get_animal_by_location(query['location_id'][0])

            if query.get('location_id') and resource == 'employees':
                response = get_employee_by_location(query['location_id'][0])

            if query.get('status') and resource == 'animals':
                response = get_animal_by_status(query['status'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        new_animal = None
        new_location = None
        new_employee = None
        new_customer = None

        if resource == "animals":
            if "name" in post_body and "species" in post_body and "breeds" in post_body and "location_id" in post_body and "customer_id" in post_body and "employee" in post_body and "status" in post_body:
                self._set_headers(201)
                new_animal = create_animal(post_body)
                response = new_animal
            else:
                self._set_headers(400)
                error_message = ""
                if "name" not in post_body:
                    error_message += "WARNING: name is required. "
                if "breeds" not in post_body:
                    error_message += "WARNING: breeds is required. "
                if "customer_id" not in post_body:
                    error_message += "WARNING: customer_id is required. "
                if "employee" not in post_body:
                    error_message += "WARNING: employee is required. "
                if "status" not in post_body:
                    error_message += "WARNING: status is required. "
                if "location_id" not in post_body:
                    error_message += "WARNING: location_id is required. "
                    new_animal = error_message
                    response = new_animal

        elif resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create_location(post_body)
                response = new_location
            else:
                self._set_headers(400)
                error_message = ""
                if "name" not in post_body:
                    error_message += "WARNING: name is required"
                if "address" not in post_body:
                    error_message += "WARNING: address is required"
                new_location = error_message
                response = new_location

        elif resource == "employees":
            if "name" in post_body and "address" in post_body and "location_id" in post_body:
                self._set_headers(201)
                new_employee = create_employee(post_body)
                response = new_employee
            else:
                self._set_headers(400)
                error_message = ""
                if "name" not in post_body:
                    error_message += "WARNING: name is required. "
                if "address" not in post_body:
                    error_message += "WARNING: address is required. "
                if "location_id" not in post_body:
                    error_message += "WARNING: location_id is required. "
                    new_employee = error_message
                    response = new_employee

        elif resource == "customers":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_customer = create_customer(post_body)
                response = new_customer
            else:
                self._set_headers(400)
                error_message = ""
                if "name" not in post_body:
                    error_message += "WARNING: fullName is required. "
                if "address" not in post_body:
                    error_message += "WARNING: address is required. "
                    new_customer = error_message
                    response = new_customer

        self.wfile.write(json.dumps(response).encode())
    # A method that handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False
    # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)

        if resource == "customers":
            update_customer(id, post_body)

        if resource == "employees":
            update_employee(id, post_body)

        if resource == "locations":
            update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
    # Encode the new animal and send in response
        self.wfile.write("".encode())

        self.do_PUT()

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        if resource == "customers":
            delete_customer(id)

        if resource == "employees":
            delete_employee(id)

        if resource == "locations":
            delete_location(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
