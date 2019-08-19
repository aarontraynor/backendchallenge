from django.test import TestCase
from django.test import Client

from rest_framework import status

from carmanagement_api.models import Branch, Driver, Car, BranchInventory, DriverInventory
from datetime import date

import requests

class CarViewSetTestCase(TestCase):
    """Tests for the Car ViewSet"""
    def setUp(self):
        """Set up objects to be used in testing the Car viewset"""
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

    def test_adding_car(self):
        c = Client()
        response = c.post("/api/cars/", {
            "make": "Reliant",
            "model": "Robin Mk2",
            "year_of_manufacture": 1990
        })

        self.assertEqual(response.json()), {
            "id": Car.objects.get(make="Reliant").id,
            "make": "Reliant",
            "model": "Robin Mk2",
            "year_of_manufacture": 1990
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_adding_car_with_invalid_year(self):
        c = Client()
        response = c.post("/api/cars/", {
            "make": "Tesla",
            "model": "Model Y",
            "year_of_manufacture": 2020
        })

        self.assertEqual(response.json(), {
            "year_of_manufacture": [
                f"Ensure this value is less than or equal to {datetime.now().year}."
            ]
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieving_specific_car(self):
        car = Car.objects.get(make="Ford")
        c = Client()
        response = c.get("/api/cars/1")

        self.assertEqual(response.json(), {
            "id": 1,
            "make": car.make,
            "model": car.model,
            "year_of_manufacture": car.year_of_manufacture,
            "currently_with": {
                "message": "Currently unassigned. Please assign this car to a Branch or Driver",
            }
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BranchViewSetTestCase(TestCase):
    """Tests for the Branch ViewSet"""
    def setUp(self):
        """Set up objects to be used in testing the Branch viewset"""
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
    """Tests for the Driver ViewSet"""
    def setUp(self):
        """Set up objects to be used in testing the Driver viewset"""
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

class BranchInventoryViewSetTestCase(TestCase):
    """Tests for the BranchInventory (returning a car) ViewSet"""
    def setUp(self):
        """Set up objects to be used in testing the BranchInventory viewset"""
        car1 = Car.objects.create(make="Ford", model="Fiesta", year_of_manufacture=2018)
        car2 = Car.objects.create(make="Tesla", model="Model S", year_of_manufacture=2016)
        branch1 = Branch.objects.create(city="London", postcode="WC2B 6ST")
        branch2 = Branch.objects.create(city="Welling", postcode="DA16 3RR", capacity=1)
        BranchInventory.objects.create(car=car1, branch=branch1)
        BranchInventory.objects.create(car=car2, branch=branch2)

    def test_branch_inventory_lists_correctly(self):
        car1 = Car.objects.get(make="Ford")
        car2 = Car.objects.get(make="Tesla")
        branch1 = Branch.objects.get(postcode="WC2B 6ST")
        branch2 = Branch.objects.get(postcode="DA16 3RR")

        c = Client()
        response = c.get("/api/return-car/")

        self.assertEqual(response.json(), [
            {
                "id": 1,
                "car": car1.id,
                "branch": branch1.id
            },
            {
                "id": 2,
                "car": car2.id,
                "branch": branch2.id
            }
        ])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DriverInventoryViewSetTestCase(TestCase):
    """Tests for DriverInventory (renting a car) ViewSet"""
    def setUp(self):
        """Set up objects to be used in testing the DriverInventory viewset"""
        car1 = Car.objects.create(make="Ford", model="Fiesta", year_of_manufacture=2018)
        car2 = Car.objects.create(make="Tesla", model="Model S", year_of_manufacture=2016)
        driver1 = Driver.objects.create(first_name="Aaron", middle_names="Toby", last_name="Traynor", date_of_birth="1997-11-07")
        driver2 = Driver.objects.create(first_name="Joe", last_name="Bloggs", date_of_birth="1990-01-01")
        DriverInventory.objects.create(car=car1, driver=driver1)
        DriverInventory.objects.create(car=car2, driver=driver2)

    def test_driver_inventory_lists_correctly(self):
        car1 = Car.objects.get(make="Ford")
        car2 = Car.objects.get(make="Tesla")
        driver1 = Driver.objects.get(first_name="Aaron")
        driver2 = Driver.objects.get(first_name="Joe")

        c = Client()
        response = c.get("/api/rent-car/")

        self.assertEqual(response.json(), [
            {
                "id": 1,
                "car": car1.id,
                "driver": driver1.id
            },
            {
                "id": 2,
                "car": car2.id,
                "driver": driver2.id
            }
        ])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
