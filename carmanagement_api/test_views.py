from django.test import TestCase
from django.test import Client

from rest_framework import status

from carmanagement_api.models import Branch, Driver, Car, BranchInventory, DriverInventory
from datetime import date

import requests

class CarViewSetTestCase(TestCase):
    def setUp(self):
        # TODO: Add setup and tests
        Car.objects.create(make="Ford", model="Fiesta", year_of_manufacture=2018)
        Car.objects.create(make="Tesla", model="Model S", year_of_manufacture=2016)

    def test_cars_list_correctly(self):
        c = Client()
        response = c.get("/api/cars/")

        self.assertEqual(response.json(), {
            "cars": [
                {
                    "id": Car.objects.get(make="Ford", model="Fiesta").id,
                    "make": "Ford",
                    "model": "Fiesta",
                    "year_of_manufacture": 2018,
                    "currently_with": {
                        "message": "Currently unassigned. Please assign this car to a Branch or Driver",
                    }
                },
                {
                    "id": Car.objects.get(make="Tesla", model="Model S").id,
                    "make": "Tesla",
                    "model": "Model S",
                    "year_of_manufacture": 2016,
                    "currently_with": {
                        "message": "Currently unassigned. Please assign this car to a Branch or Driver",
                    }
                }
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty_POST_returns_400(self):
        c = Client()
        response = c.post("/api/cars/")

        self.assertEqual(response.json(), {
            "make": [
                "This field is required."
            ],
            "model": [
                "This field is required."
            ],
            "year_of_manufacture": [
                "This field is required."
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BranchViewSetTestCase(TestCase):
    def setUp(self):
        Branch.objects.create(city="London", postcode="WC2B 6ST")
        Branch.objects.create(city="Welling", postcode="DA16 3RR", capacity=5)

    def test_branches_list_correctly(self):
        c = Client()
        response = c.get("/api/branches/")

        self.assertEqual(response.json(), [
            {
                "id": Branch.objects.get(postcode="WC2B 6ST").id,
                "city": "London",
                "postcode": "WC2B 6ST",
                "capacity": 10
            },
            {
                "id": Branch.objects.get(postcode="DA16 3RR").id,
                "city": "Welling",
                "postcode": "DA16 3RR",
                "capacity": 5
            }
        ])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty_POST_returns_400(self):
        c = Client()
        response = c.post("/api/branches/")

        self.assertEqual(response.json(), {
            "city": [
                "This field is required."
            ],
            "postcode": [
                "This field is required."
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DriverViewSetTestCase(TestCase):
    def setUp(self):
        Driver.objects.create(first_name="Aaron", middle_names="Toby", last_name="Traynor", date_of_birth="1997-11-07")
        Driver.objects.create(first_name="Joe", last_name="Bloggs", date_of_birth="1990-01-01")

    def test_drivers_list_correctly(self):
        c = Client()
        response = c.get("/api/drivers/")

        self.assertEqual(response.json(), [
            {
                "id": Driver.objects.get(first_name="Aaron", last_name="Traynor").id,
                "first_name": "Aaron",
                "middle_names": "Toby",
                "last_name": "Traynor",
                "date_of_birth": "1997-11-07"
            },
            {
                "id": Driver.objects.get(first_name="Joe", last_name="Bloggs").id,
                "first_name": "Joe",
                "middle_names": None,
                "last_name": "Bloggs",
                "date_of_birth": "1990-01-01"
            }
        ])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_empty_POST_returns_400(self):
        c = Client()
        response = c.post("/api/drivers/")

        self.assertEqual(response.json(), {
            "first_name": [
                "This field is required."
            ],
            "last_name": [
                "This field is required."
            ],
            "date_of_birth": [
                "This field is required."
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# class BranchInventoryViewSetTestCase(TestCase):
#     def setUp(self):
#         # TODO: Add setup and tests
#
#
# class DriverInventoryViewSetTestCase(TestCase):
#     def setUp(self):
#         # TODO: Add setup and tests
