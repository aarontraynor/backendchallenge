Accessing the API
====================

The API can be accessed in 1 of 2 ways:
1. By using the hosted version of the application at http://ottocar.aarontraynor.uk:8080/api
2. By setting up and hosting your own version of the application locally using the guide below

Setup instructions
====================

The following instructions will guide you through how to get up and running with this project on your local machine.

## Prerequisites

Running this project requires the following software to be installed:

- VirtualBox (https://www.virtualbox.org/)
- Vagrant (https://www.vagrantup.com/downloads.html)
- Atom (https://atom.io/)
- Git (https://git-scm.com/downloads)

**PLEASE NOTE:** Installing git on Windows requires some additional setup. To run this project on Windows, please follow the "Git on Windows" steps below before continuing. For Unix-based systems, git can be installed as normal without any custom setup.

#### Git on Windows
In order to follow the instructions below, we must install both git and git bash.
1. Download the installer from https://git-scm.com/downloads.
2. Click next until you reach the "Adjusting your PATH environment" window.
3. Select the option "Git from the command line and also from 3rd party software".
4. Select the "Use the OpenSSL library" option.
5. Click next until the installation is complete.
6. Check that the "Git Bash" desktop app has been installed. This will be used in the instructions below.

#### Setting up the workspace
**Windows Users:** These instructions will refer to the terminal window from time to time. On Windows, this is substituted for the "Git Bash" desktop app that was installed as part of the git install process.

1. Create a new folder where you would like the project to reside. For this example, we will use a folder called "workspace" in the home directory ```~/workspace```
2. In a terminal window, type ```cd ~/workspace```, remembering to replace the path with your own path if you are working in a different location.
3. Type ```git clone https://github.com/aarontraynor/backendchallenge.git``` to copy the GitHub repo into your local folder.
4. To confirm that the files have cloned correctly, type ```ls```. You should see that a folder named "backendchallenge" has now appeared.
5. Type ```cd backendchallenge``` to enter the repository.
6. Type ```vagrant up``` in the terminal window to set up and run the Vagrant virtual environment.
7. Connect to the Vagrant environment by typing ```vagrant ssh``` in the terminal window.
8. In the Vagrant ssh window, type ```cd /vagrant```.
9. Type ```ls```. You should see that the files mirror the repository. This folder in the vagrant environment is synchronised with the local copy of the repo. Any changes made to the local copy will reflect in the Vagrant environment.
10. Set up a Python virtual environment (venv) by typing ```python -m venv ~/env``` in the ssh window.
11. Enable the Python venv by typing ```source ~/env/bin/activate```.
12. In the Python venv, type ```pip install -r requirements.txt```. This will install all the Python requirements for this project.
13. Type ```python manage.py migrate``` in the Python venv to set up the database.
13. Type ```python manage.py runserver 0.0.0.0:8000``` to enable the server.

The project is now running locally on your machine. You can access the browsable API at http://localhost:8000/api/

## 3rd Party Integrations

UK Postcode Validation: https://postcodes.io/
- Available under the MIT Licence
- Requests for information using postcodes within Great Britain may be used under the OS OpenData licence
- Requests for information using postcodes in Northern Ireland require a licence from NI Land & Property Services if used commercially

How to use the API
==================

The browsable API at http://localhost:8000/api provides an easy way to navigate the system and try out the available features. If you are using a browser and wish to receive the raw JSON response from the server, append `?format=json` (or `&format=json` if your request already contains a search parameter) to your API request.

## Cars

A car has the following JSON format:
```
{
  "id": Integer,
  "make": String,
  "model": String,
  "year_of_manufacture": Integer,
  "currently_with": {
      JSON representation of either a Branch or Driver, depending on who the car is currently with
  }
}
```

- The `make`, `model` and `year_of_manufacture` fields can be set by the user.
- Cars can be searched on by the `make`, `model` and `year_of_manufacture` fields.

**GET** Requests
- List all cars: `GET /api/cars/`
- Retrieve a specific car: `GET /api/cars/<id>`
- Search cars: `GET /api/cars/?search=<search_string>`

**POST/PUT/PATCH** Requests
- Add a new car: `POST /api/cars/`
- Update a car's information: `PUT /api/cars/<id>`
- Update some attributes of a car: `PATCH /api/cars/<id>`

## Branches

A branch has the following JSON format:
```
{
    "id": Integer,
    "city": String,
    "postcode": String,
    "capacity": Integer
}
```

- The `city`, `postcode` and `capacity` fields can be set by the user.
- Branches can be searched on the `city` and `postcode` fields.

**GET** Requests
- List all branches: `GET /api/branches/`
- Retrieve a specific branch: `GET /api/branches/<id>`
- Search branches: `GET /api/branches/?search=<search_string>`

**POST/PUT/PATCH** Requests
- Add a new branch: `POST /api/branches/`
- Update a branch's information: `PUT /api/branches/<id>`
- Update some attributes of a branch: `PATCH /api/branches/<id>`

## Drivers

A driver has the following JSON format:
```
{
    "id": Integer,
    "first_name": String,
    "middle_names": String (can be null),
    "last_name": String,
    "date_of_birth": Date
}
```

- The `first_name`, `middle_names`, `last_name` and `date_of_birth` fields can be set by the user.
- Drivers can be searched on the `first_name`, `middle_names`, `last_name` and `date_of_birth` fields.

**GET** Requests
- List all drivers: `GET /api/drivers/`
- Retrieve a specific driver: `GET /api/drivers/<id>`
- Search branches: `GET /api/branches/?search=<search_string>`

**POST/PUT/PATCH** Requests
- Add a new driver: `POST /api/drivers/`
- Update a driver's information: `PUT /api/drivers/<id>`
- Update some attributes of a driver: `PATCH /api/drivers/<id>`

## Car Rental

A car rental has the following JSON format:
```
{
    "id": Integer,
    "car": Foreign Key,
    "driver": Foreign Key
}
```

- The `car` and `driver` fields can be set by the user.
- Renting a car will update the Car's `currently_with` field.
- Renting a car will remove any links between a car and a branch.
- Car rentals can only be added using `POST` requests - they cannot be updated once created.
- Car rentals cannot be created for cars that are already rented to another driver.

**GET** Requests
- List all car rentals: `GET /api/rent-car/`
- Retrieve a specific car rental: `GET /api/rent-car/<id>`

**POST/PUT/PATCH** Requests
- Add a new rental: `POST /api/rent-car/`

## Branch Inventory

A vehicle in a branch's inventory has the following JSON format:
```
{
    "id": Integer,
    "car": Foreign Key,
    "branch": Foreign Key
}
```

- The `car` and `branch` fields can be set by the user.
- Returning a car to a branch will update the Car's `currently_with` field.
- Returning a car to a branch will remove any links between that car and other branches or drivers.
- Car/Branch associations can only be added using `POST` requests - they cannot be updated once created.

**GET** Requests
- List all cars at branches: `GET /api/return-car/`
- Retrieve a specific car/branch association: `GET /api/return-car/<id>`

**POST/PUT/PATCH** Requests
- Return a car to a branch: `POST /api/return-car/`

--------------------

Back End Challenge
====================

This code challenge allows you to demonstrate your ability to build a simple web server, but gives us a chance to see how you code and how you use version control.

## Things we're looking for
- Clean & readable code is super important, as it means it's easier for people to read, reuse, and refactor your work.
- Good use of version control means it's easy for people to check and review your code.
- [Using a testing framework](https://medium.com/javascript-scene/tdd-changed-my-life-5af0ce099f80) (where applicable) means you're more likely to deliver robust code.

## The Challenge

We deal with lots and lots of cars on a day-to-day basis, so naturally this will be related to automotives.

Imagine you have a car rental business. You have multiple **Branches**. A car can either be at a **Branch** or with a **Driver**.

## Your task

Your task is to develop one (or more, feel free) RESTful service(s) to:

- Create a Car
- Update a Car information
- Retrieve a Car by parameters
- Create a Branch
- Retrieve a Branch by parameters
- Create a Driver
- Retrieve a Driver by parameters
- Assign a Car to a Driver (i.e. the car is being rented out)
- Assign a Car to a Branch (i.e. the car has been returned)
- Fork this repository and submit your code with commits.

This is the information we store about each car:
- Make (e.g. Tesla)
- Model (e.g. Model 3)
- Year (e.g. 2019)
- Currently_With (options: \[Garage\], \[Driver\])

This is the information we store about each Branch:
- City (e.g. London)
- Postcode (e.g. W6 9EA)

This is the information we store about each Driver:
- Name (e.g. Kevin Hart)
- Date of Birth (e.g. 02/12/1990)

Before you get started, make sure to read through all the levels below.

#### Base Requirements For All Levels
-------
- Clean, readable, maintainable codebase
- Source code on Github
- Your service(s) must be resilient, fault tolerant, responsive. You should prepare it/them to be highly scalable as possible.

#### Levels of Awesome

Choose one of the following routes for your journey.

-------
### Novice

*"Hey! Look! Listen!"*

**TASKS**
* All of the base requirements
+ Using a database service (e.g. PostgreSQL or MySQL)
+ Show us your work through your commit history

-------
### Intermediate

*"I know Kung Fu."*

**TASKS**
* All of the base, and novice requirements
+ Asynchronous processing
+ Host the application online (we enjoy hosting services like AWS, Azure, Heroku and DigitalOcean but you're welcome to use a different hosting provider)

-------
### Expert

*"Watch and learn Grasshopper."*

**TASKS**
* All of the base, novice, and intermediate requirements
+ Provide clear written instructions on running the application locally in the README
+ Add a Capacity field to the Branch and only allow it to store up to that number of cars (e.g. if Branch has a capacity of 2, it can't have more than 2 cars in stock).

-------
### Bonus Round

*"All is fair in love and bonus rounds"*

**TASKS**
+ Surprise us! Add a feature that you think would work well here; for instance, advanced search, integration with other API, a "Favourite" functionality
