"""One-off script: insert a single realistic random Indian user into the DB."""
import os
import random
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash

from database.db import get_db

FIRST_NAMES = [
    "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Kavya",
    "Arjun", "Divya", "Karthik", "Meera", "Suresh", "Pooja", "Rajesh", "Isha",
    "Aditya", "Neha", "Sanjay", "Lakshmi", "Manoj", "Deepika", "Vivek", "Shreya",
    "Nikhil", "Anjali", "Ganesh", "Ritu", "Harish", "Swati",
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Gupta", "Singh",
    "Rao", "Menon", "Kulkarni", "Joshi", "Chatterjee", "Mukherjee", "Pillai",
    "Desai", "Agarwal", "Bose", "Naidu", "Krishnan",
]


def generate_user():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    suffix = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{suffix}@gmail.com"
    return name, email


def main():
    conn = get_db()
    try:
        name, email = generate_user()
        while conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone():
            name, email = generate_user()

        password_hash = generate_password_hash("password123")
        created_at = datetime.now().isoformat(timespec="seconds")

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, created_at),
        )
        conn.commit()
        user_id = cursor.lastrowid

        print("Seeded user:")
        print(f"  id:    {user_id}")
        print(f"  name:  {name}")
        print(f"  email: {email}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
