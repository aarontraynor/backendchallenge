from django.test import TestCase
from carmanagement_api.models import Branch, Driver, Car, BranchInventory, DriverInventory


class BranchTestCase(TestCase):
    """Tests for the Branch model"""
    def setUp(self):
        """Set up objects to be used in testing the Branch model"""
        Branch.objects.create(city="London", postcode="WC2B 6ST")

    def test_branch_string_representation(self):
        """Test that the class returns the correct string representation of a Branch"""
        branch = Branch.objects.get(postcode="WC2B 6ST")
        self.assertEqual(branch.__str__(), 'London, WC2B 6ST')


class DriverTestCase(TestCase):
    """Tests for the Driver model"""
    def setUp(self):
        """Set up objects to be used in testing the Driver model"""
        Driver.objects.create(first_name="Aaron", middle_names="Toby", last_name="Traynor", date_of_birth="1997-11-07")

    def test_driver_string_representation(self):
        """Test that the class returns the correct string representation of a Driver"""
        driver = Driver.objects.get(first_name="Aaron", last_name="Traynor")
        self.assertEqual(driver.__str__(), 'Aaron Toby Traynor')


class CarTestCase(TestCase):
    """Tests for the Car model"""
    def setUp(self):
        """Set up objects to be used in testing the Car model"""
        Car.objects.create(make="Ford", model="Fiesta", year_of_manufacture="2018")

    def test_car_string_representation(self):
        """Test that the class returns the correct string representation of a Car"""
        car = Car.objects.get(make="Ford", model="Fiesta", year_of_manufacture="2018")
        self.assertEqual(car.__str__(), f'ID: {car.id} (Ford Fiesta, 2018)')


class BranchInventoryTestCase(TestCase):
    """Tests for the BranchInventory model"""
    def setUp(self):
        """Set up objects to be used in testing the BranchInventory model"""
        car = Car.objects.create(make="Ford", model="Fiesta", year_of_manufacture="2018")
        branch = Branch.objects.create(city="London", postcode="WC2B 6ST")
        BranchInventory.objects.create(car=car, branch=branch)

    def test_branch_inventory_string_representation(self):
        """Test that the class returns the correct string representation of a BranchInventory"""
        car = Car.objects.get(make="Ford", model="Fiesta", year_of_manufacture="2018")
        branch = Branch.objects.get(city="London", postcode="WC2B 6ST")
        branch_inventory = BranchInventory.objects.get(car=car, branch=branch)

        self.assertEqual(branch_inventory.__str__(), f'{car} is at {branch}')


class DriverInventoryTestCase(TestCase):
    """Tests for the DriverInventory model"""
    def setUp(self):
        """Set up objects to be used in testing the DriverInventory model"""
        car = Car.objects.create(make="Ford", model="Fiesta", year_of_manufacture="2018")
        driver = Driver.objects.create(first_name="Aaron", middle_names="Toby", last_name="Traynor", date_of_birth="1997-11-07")
        DriverInventory.objects.create(car=car, driver=driver)

    def test_driver_inventory_string_representation(self):
        """Test that the class returns the correct string representation of a DriverInventory"""
        car = Car.objects.get(make="Ford", model="Fiesta", year_of_manufacture="2018")
        driver = Driver.objects.get(first_name="Aaron", middle_names="Toby", last_name="Traynor", date_of_birth="1997-11-07")
        driver_inventory = DriverInventory.objects.get(car=car, driver=driver)

        self.assertEqual(driver_inventory.__str__(), f'{car} is with {driver}')
