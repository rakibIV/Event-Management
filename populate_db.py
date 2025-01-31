import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from event.models import Category, Event, Participant

# Initialize Faker
fake = Faker()

def populate_db():
    # Create Categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.text()
    ) for _ in range(5)]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = [Event.objects.create(
        name=fake.sentence(nb_words=4),
        description=fake.text(),
        date=fake.date_between(start_date="-30d", end_date="+30d"),
        time=fake.time(),
        location=fake.address(),
        category=random.choice(categories)
    ) for _ in range(10)]
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participant.events.set(random.sample(events, random.randint(1, 5)))
        participants.append(participant)
    print(f"Created {len(participants)} participants.")
    
    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
