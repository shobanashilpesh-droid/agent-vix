
import pandas as pd
from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

langfuse = get_client()


def run_renewal_agent(df):

    with langfuse.start_as_current_observation(
        as_type="span",
        name="Renewal Intelligence Agent",
        input={
            "total_subscriptions": len(df)
        }
    ) as span:

        print("Renewal Agent started...")

        # Identify subscriptions approaching renewal
        opportunities = df[
            (df["days_to_renewal"] >= 0) &
            (df["days_to_renewal"] <= 30)
        ].copy()

        # Assign priority
        def assign_priority(days):

            if days <= 7:
                return "Critical"

            elif days <= 15:
                return "High"

            else:
                return "Medium"

        opportunities["priority"] = (
            opportunities["days_to_renewal"]
            .apply(assign_priority)
        )

        # Sort by nearest renewal
        opportunities = opportunities.sort_values(
            by="days_to_renewal"
        )

        result = opportunities[
            [
                "customer_id",
                "customer_name",
                "reseller_name",
                "product",
                "renewal_date",
                "days_to_renewal",
                "annual_value_usd",
                "priority"
            ]
        ]

        output = result.to_dict(orient="records")

        # Record output in Langfuse
        span.update(
            output={
                "renewal_opportunity_count": len(output),
                "opportunities": output
            }
        )

        print("Renewal Agent completed!")
        print("Renewal opportunities:", len(output))

        return result
