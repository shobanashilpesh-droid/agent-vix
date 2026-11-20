
import pandas as pd
import random
from datetime import date, timedelta


def generate_adobe_data():

    random.seed(42)

    records = []

    resellers = {
        "RES-100": "Northstar Solutions",
        "RES-200": "BluePeak Technologies",
        "RES-300": "Vertex Systems"
    }

    products = [
        "Acrobat Pro",
        "Creative Cloud",
        "Acrobat Sign",
        "FrameMaker"
    ]

    for i in range(1, 101):

        reseller_id = random.choice(list(resellers.keys()))

        days_to_renewal = random.choice([
            5, 10, 15, 20, 30, 45, 60, 90, 120
        ])

        seats = random.choice([10, 25, 50, 100, 150, 200])

        utilization = round(random.uniform(0.40, 0.99), 2)

        churn_score = round(random.uniform(0.10, 0.95), 2)

        discount = random.choice([0, 5, 10, 15])

        annual_value = seats * random.choice([120, 180, 240])

        records.append({

            "customer_id": f"CUST-{i:04d}",

            "customer_name": f"Customer {i:03d}",

            "reseller_id": reseller_id,

            "reseller_name": resellers[reseller_id],

            "subscription_id": f"SUB-{10000+i}",

            "product": random.choice(products),

            "seats": seats,

            "seat_utilization": utilization,

            "churn_propensity": churn_score,

            "days_to_renewal": days_to_renewal,

            "renewal_date": str(
                date.today() +
                timedelta(days=days_to_renewal)
            ),

            "flex_discount_pct": discount,

            "annual_value_usd": annual_value

        })

    return pd.DataFrame(records)


if __name__ == "__main__":

    df = generate_adobe_data()

    print("Adobe synthetic data generated!")

    print("Total customers:", len(df))

    print(df.head(10))

    df.to_csv("data/adobe_subscriptions.csv", index=False)

    print("CSV file created successfully!")
