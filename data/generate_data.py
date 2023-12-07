import json
import random
from faker import Faker

# Initialize Faker to generate fake data
fake = Faker()


# Function to generate a random company information data model
def generate_company_data():
    company_name = fake.company()
    return {
        "CIN": str(random.randint(10, 1000)),
        "company_name": company_name,
        "address": fake.address(),
        "registration_date": fake.date_between(start_date="-10y", end_date="today").isoformat(),
        "number_of_employees": random.randint(10, 1000),
        "raised_capital": random.randint(100000, 10000000),
        "turnover": random.randint(500000, 50000000),
        "net_profit": random.randint(100000, 10000000),
        "contact_number": fake.phone_number(),
        "contact_email": fake.company_email(),
        "company_website": fake.url(),
        "loan_amount": random.randint(50000, 5000000),
        "loan_interest_percentage": round(random.uniform(2, 10), 2),
        "account_status": random.choice(["Active", "Inactive", "Pending"]),
    }


# Generate 20 entries of company data
company_data_list = [generate_company_data() for _ in range(20)]

# Convert to JSON
json_data = json.dumps(company_data_list, indent=4)

with open("company_data.json", "w+") as file:
    file.write(json_data)
