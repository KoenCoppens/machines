import random
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app import models


ACCOUNT_NAMES = [
    "Techniek Antwerpen",
    "Bruxelles Industriel",
    "Gent Machines",
    "Liège Solutions",
    "Namur Atelier",
    "Leuven Logistic",
    "Charleroi Systems",
    "Hasselt Energy",
    "Kortrijk Fabrication",
    "Mechelen Automation",
]
CITY_PAIRS = [
    ("Antwerpen", "BE"),
    ("Bruxelles", "BE"),
    ("Gent", "BE"),
    ("Liège", "BE"),
    ("Namur", "BE"),
    ("Leuven", "BE"),
    ("Charleroi", "BE"),
    ("Hasselt", "BE"),
    ("Kortrijk", "BE"),
    ("Mechelen", "BE"),
]
FIRST_NAMES = ["Jan", "Pieter", "Marie", "Sofie", "Lucas", "Amélie", "Louis", "Nina"]
LAST_NAMES = ["Peeters", "Dubois", "Janssens", "Lambert", "Claes", "De Smet", "Maes"]


DEF_RULE_OFFSETS = [-90, -30, -7, 0, 7]


def reset_tables(db: Session):
    db.query(models.Alert).delete()
    db.query(models.Machine).delete()
    db.query(models.Location).delete()
    db.query(models.Contact).delete()
    db.query(models.Account).delete()
    db.query(models.AlertRule).delete()
    db.commit()


def seed_alert_rules(db: Session):
    for offset in DEF_RULE_OFFSETS:
        rule = models.AlertRule(
            name=f"Warranty {offset}d",
            trigger="WARRANTY_END_DATE",
            offset_days=offset,
            enabled=True,
            channels="INAPP",
        )
        db.add(rule)
    db.commit()


def seed_accounts(db: Session, count: int = 30):
    accounts = []
    for i in range(count):
        name = random.choice(ACCOUNT_NAMES)
        city, country = random.choice(CITY_PAIRS)
        account = models.Account(
            account_number=f"ACC-{i+1000}",
            name=f"{name} {i+1}",
            phone=f"+32 2 555 {i:04d}",
            email=f"info{i}@example.be",
            website=f"https://{name.split()[0].lower()}{i}.be",
            language=random.choice(["NL", "FR"]),
            billing_street="Industrieweg",
            billing_house_number=str(10 + i),
            billing_postal_code=f"1{i:03d}",
            billing_city=city,
            billing_country=country,
        )
        db.add(account)
        accounts.append(account)
    db.commit()
    return accounts


def seed_locations(db: Session, accounts, count: int = 60):
    locations = []
    for i in range(count):
        account = random.choice(accounts)
        city, country = random.choice(CITY_PAIRS)
        location = models.Location(
            account_id=account.id,
            location_code=f"LOC-{i+2000}",
            name=f"{city} Depot {i+1}",
            street="Atelierstraat",
            house_number=str(20 + i),
            postal_code=f"2{i:03d}",
            city=city,
            country=country,
            geo_lat=50.85 + random.random(),
            geo_lng=4.35 + random.random(),
        )
        db.add(location)
        locations.append(location)
    db.commit()
    return locations


def seed_contacts(db: Session, accounts, count: int = 80):
    contacts = []
    for i in range(count):
        account = random.choice(accounts)
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        contact = models.Contact(
            account_id=account.id,
            first_name=first_name,
            last_name=last_name,
            display_name=f"{first_name} {last_name}",
            email=f"{first_name.lower()}.{last_name.lower()}{i}@example.be",
            phone=f"+32 3 700 {i:04d}",
            role=random.choice(["Manager", "Technician", "Buyer"]),
            is_primary=i % 10 == 0,
        )
        db.add(contact)
        contacts.append(contact)
    db.commit()
    return contacts


def seed_machines(db: Session, accounts, locations, count: int = 120):
    machines = []
    today = date.today()
    for i in range(count):
        account = random.choice(accounts)
        location = random.choice(locations)
        installation_date = today - timedelta(days=random.randint(30, 900))
        warranty_months = random.choice([12, 24, 36])
        warranty_end_date = installation_date + timedelta(days=warranty_months * 30)
        if i % 5 == 0:
            warranty_end_date = today - timedelta(days=random.randint(1, 30))
        elif i % 5 == 1:
            warranty_end_date = today + timedelta(days=random.randint(1, 7))
        elif i % 5 == 2:
            warranty_end_date = today + timedelta(days=random.randint(8, 30))
        elif i % 5 == 3:
            warranty_end_date = today + timedelta(days=random.randint(31, 90))
        machine = models.Machine(
            account_id=account.id,
            location_id=location.id,
            machine_name=f"Press {i+1}",
            machine_number=f"MCH-{i+3000}",
            status=random.choice(["ACTIVE", "MAINTENANCE", "INACTIVE"]),
            product_category=random.choice(["Compressor", "Conveyor", "Press"]),
            family_name=random.choice(["Atlas", "Lévrier", "Brabo"]),
            family_code=random.choice(["ATL", "LEV", "BRB"]),
            installation_date=installation_date,
            warranty_months=warranty_months,
            warranty_end_date=warranty_end_date,
            warranty_type=random.choice(["Standard", "Extended"]),
        )
        db.add(machine)
        machines.append(machine)
    db.commit()
    return machines


def seed():
    db = SessionLocal()
    try:
        reset_tables(db)
        seed_alert_rules(db)
        accounts = seed_accounts(db)
        locations = seed_locations(db, accounts)
        seed_contacts(db, accounts)
        seed_machines(db, accounts, locations)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
