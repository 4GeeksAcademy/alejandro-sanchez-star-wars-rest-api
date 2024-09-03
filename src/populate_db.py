from app import app, db
from models import Character, Planet, Vehicle

with app.app_context():
    # Poblar la tabla de Characters
    characters = [
        Character(name="Luke Skywalker", birth_year="19BBY", gender="male"),
        Character(name="Leia Organa", birth_year="19BBY", gender="female"),
        Character(name="Darth Vader", birth_year="41.9BBY", gender="male")
    ]
    
    # Poblar la tabla de Planets
    planets = [
        Planet(name="Tatooine", climate="arid", terrain="desert"),
        Planet(name="Alderaan", climate="temperate", terrain="grasslands, mountains"),
        Planet(name="Hoth", climate="frozen", terrain="tundra, ice caves")
    ]

    # Poblar la tabla de Vehicles
    vehicles = [
        Vehicle(name="X-wing", model="T-65 X-wing starfighter", price=150000),
        Vehicle(name="TIE Fighter", model="TIE/ln space superiority starfighter", price=75000),
        Vehicle(name="Millennium Falcon", model="YT-1300 light freighter", price=1000000)
    ]
    
    # Añadir los datos a la sesión
    db.session.add_all(characters)
    db.session.add_all(planets)
    db.session.add_all(vehicles)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    print("Database populated with sample characters, planets, and vehicles.")
