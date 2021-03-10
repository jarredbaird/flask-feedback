"""Seed file to make sample data for Users db."""
from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
one = User.register(username='sonic88',
                    email="sonic@hedgehog.com",
                    pwd="emerald",
                    first='Sonic',
                    last='Hedgehog')

db.session.add(one)

# Commit--otherwise, this never gets saved!
db.session.commit()