from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()
langfuse = get_client()


def run_churn_agent(df):

    with langfuse.start_as_current_observation(
        as_type="span",
        name="Churn Prediction Agent",
        input={
            "total_subscriptions": len(df)
        }
    ) as span:

        print("Churn Prediction Agent started...")

        # Identify customers with high churn propensity
        at_risk = df[
            df["churn_propensity"] >= 0.70
        ].copy()

        # Assign risk levels
        def assign_risk(score):

            if score >= 0.85:
                return "Critical"

            elif score >= 0.70:
                return "High"

            return "Medium"

        at_risk["risk_level"] = (
            at_risk["churn_propensity"].apply(assign_risk)
        )

        # Sort by highest churn propensity
        at_risk = at_risk.sort_values(
            by="churn_propensity",
            ascending=False
        )

        result = at_risk[
            [
                "customer_id",
                "customer_name",
                "reseller_name",
                "product",
                "seat_utilization",
                "churn_propensity",
                "days_to_renewal",
                "annual_value_usd",
                "risk_level"
            ]
        ]

        output = result.to_dict(orient="records")

        span.update(
            output={
                "at_risk_customer_count": len(output),
                "at_risk_customers": output
            }
        )

        print("Churn Prediction Agent completed!")
        print("At-risk customers:", len(output))

        return result
