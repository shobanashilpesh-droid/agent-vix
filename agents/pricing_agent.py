
from dotenv import load_dotenv
from langfuse import get_client

# Load Langfuse credentials
load_dotenv()

langfuse = get_client()


def run_pricing_agent(df):

    with langfuse.start_as_current_observation(
        as_type="span",
        name="Pricing Intelligence Agent",
        input={"total_subscriptions": len(df)}
    ) as span:

        print("Pricing Intelligence Agent started...")

        # Demo rule:
        # Flag high-value subscriptions with low flex discounts
        opportunities = df[
            (df["annual_value_usd"] >= 5000) &
            (df["flex_discount_pct"] < 10)
        ].copy()

        # Assign opportunity priority
        def assign_priority(value, discount):
            if value >= 10000 and discount < 5:
                return "High"
            elif value >= 5000:
                return "Medium"
            return "Low"

        opportunities["priority"] = opportunities.apply(
            lambda row: assign_priority(
                row["annual_value_usd"],
                row["flex_discount_pct"]
            ),
            axis=1
        )

        # Recommend next action
        opportunities["recommended_action"] = (
            "Review flex discount eligibility and "
            "request an updated pricing preview"
        )

        opportunities = opportunities.sort_values(
            by="annual_value_usd",
            ascending=False
        )

        result = opportunities[
            [
                "customer_id",
                "customer_name",
                "reseller_name",
                "product",
                "annual_value_usd",
                "flex_discount_pct",
                "priority",
                "recommended_action"
            ]
        ]

        span.update(
            output={
                "pricing_opportunity_count": len(result),
                "opportunities": result.to_dict(
                    orient="records"
                )
            }
        )

        print("Pricing Intelligence Agent completed!")
        print("Pricing opportunities:", len(result))

        return result
