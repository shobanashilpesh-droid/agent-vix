
from dotenv import load_dotenv
from langfuse import get_client

from agents.renewal_agent import run_renewal_agent
from agents.churn_agent import run_churn_agent
from agents.pricing_agent import run_pricing_agent
from agents.upsell_agent import run_upsell_agent

load_dotenv()
langfuse = get_client()


def run_smart_agent_vix(df):

    print("\n====================================")
    print(" AGENT VIX - SMART ORCHESTRATOR")
    print("====================================")

    results = {}
    invoked_agents = []
    skipped_agents = []

    with langfuse.start_as_current_observation(
        as_type="span",
        name="Agent VIX - Smart Orchestrator",
        input={"total_subscriptions": len(df)}
    ) as span:

        # ---------------------------------
        # 1. Renewal Intelligence Routing
        # ---------------------------------

        if (
            (df["days_to_renewal"] >= 0) &
            (df["days_to_renewal"] <= 30)
        ).any():

            print("\nRouting to Renewal Intelligence Agent...")

            results["renewal_results"] = run_renewal_agent(df)
            invoked_agents.append("Renewal Intelligence Agent")

        else:
            print("\nSkipping Renewal Agent - No upcoming renewals")
            skipped_agents.append("Renewal Intelligence Agent")

        # ---------------------------------
        # 2. Churn Prediction Routing
        # ---------------------------------

        if (df["churn_propensity"] >= 0.70).any():

            print("\nRouting to Churn Prediction Agent...")

            results["churn_results"] = run_churn_agent(df)
            invoked_agents.append("Churn Prediction Agent")

        else:
            print("\nSkipping Churn Agent - No high-risk customers")
            skipped_agents.append("Churn Prediction Agent")

        # ---------------------------------
        # 3. Pricing Intelligence Routing
        # ---------------------------------

        pricing_condition = (
            (df["flex_discount_pct"] < 10) &
            (df["annual_value_usd"] >= 5000) &
            (df["days_to_renewal"] >= 0) &
            (df["days_to_renewal"] <= 60)
        )

        if pricing_condition.any():

            print("\nRouting to Pricing Intelligence Agent...")

            results["pricing_results"] = run_pricing_agent(df)
            invoked_agents.append("Pricing Intelligence Agent")

        else:
            print("\nSkipping Pricing Agent - No pricing opportunities")
            skipped_agents.append("Pricing Intelligence Agent")

        # ---------------------------------
        # 4. Upsell and Cross-sell Routing
        # ---------------------------------

        if (df["seat_utilization"] >= 0.80).any():

            print("\nRouting to Upsell and Cross-sell Agent...")

            results["upsell_results"] = run_upsell_agent(df)
            invoked_agents.append("Upsell and Cross-sell Agent")

        else:
            print("\nSkipping Upsell Agent - No expansion opportunities")
            skipped_agents.append("Upsell and Cross-sell Agent")

        # ---------------------------------
        # 5. Consolidate Results
        # ---------------------------------

        summary = {
            "total_subscriptions": len(df),
            "agents_invoked": invoked_agents,
            "agents_skipped": skipped_agents,
            "renewal_opportunities": len(
                results.get("renewal_results", [])
            ),
            "churn_risk_customers": len(
                results.get("churn_results", [])
            ),
            "pricing_opportunities": len(
                results.get("pricing_results", [])
            ),
            "upsell_opportunities": len(
                results.get("upsell_results", [])
            )
        }

        span.update(output=summary)

        results["summary"] = summary

        print("\n====================================")
        print(" SMART ORCHESTRATION SUMMARY")
        print("====================================")

        for key, value in summary.items():
            print(f"{key}: {value}")

        print("\nAGENT VIX SMART ORCHESTRATION COMPLETED!")

        return results
