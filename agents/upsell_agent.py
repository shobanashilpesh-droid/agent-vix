
from dotenv import load_dotenv
from langfuse import get_client

# Load Langfuse credentials
load_dotenv()

langfuse = get_client()


def run_upsell_agent(df):

    with langfuse.start_as_current_observation(
        as_type="span",
        name="Upsell and Cross-sell Agent",
        input={
            "total_subscriptions": len(df)
        }
    ) as span:

        print("Upsell and Cross-sell Agent started...")

        # Identify customers with high seat utilization
        opportunities = df[
            df["seat_utilization"] >= 0.80
        ].copy()

        # Estimate additional seat opportunity
        opportunities["potential_additional_seats"] = (
            opportunities["seats"] * 0.20
        ).round().astype(int)

        # Estimate potential incremental annual value
        opportunities["potential_incremental_value_usd"] = (
            opportunities["annual_value_usd"] * 0.20
        ).round(2)

        # Assign opportunity priority
        def assign_priority(utilization):

            if utilization >= 0.95:
                return "High"

            elif utilization >= 0.85:
                return "Medium"

            return "Low"

        opportunities["priority"] = (
            opportunities["seat_utilization"]
            .apply(assign_priority)
        )

        opportunities["recommended_action"] = (
            "Review additional seat requirements and "
            "cross-sell opportunities with reseller"
        )

        # Sort by highest utilization
        opportunities = opportunities.sort_values(
            by="seat_utilization",
            ascending=False
        )

        result = opportunities[
            [
                "customer_id",
                "customer_name",
                "reseller_name",
                "product",
                "seats",
                "seat_utilization",
                "potential_additional_seats",
                "annual_value_usd",
                "potential_incremental_value_usd",
                "priority",
                "recommended_action"
            ]
        ]

        span.update(
            output={
                "upsell_opportunity_count": len(result),
                "opportunities": result.to_dict(
                    orient="records"
                )
            }
        )

        print("Upsell and Cross-sell Agent completed!")
        print("Upsell opportunities:", len(result))

        return result
