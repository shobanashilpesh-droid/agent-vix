
from dotenv import load_dotenv
from langfuse import get_client

from agents.renewal_agent import run_renewal_agent
from agents.churn_agent import run_churn_agent
from agents.pricing_agent import run_pricing_agent
from agents.upsell_agent import run_upsell_agent

# Load environment variables
load_dotenv()

langfuse = get_client()


def run_agent_vix(df):

    print("\n====================================")
    print("       AGENT VIX STARTED")
    print("====================================")

    with langfuse.start_as_current_observation(
        as_type="span",
        name="Agent VIX - Master Orchestrator",
        input={
            "total_subscriptions": len(df)
        }
    ) as span:

        # Shared context for all specialist agents
        business_context = df.copy()

        print("\nAgent VIX analyzing subscription data...")

        # 1. Renewal Intelligence
        print("\nInvoking Renewal Intelligence Agent...")
        renewal_results = run_renewal_agent(business_context)

        # 2. Churn Prediction
        print("\nInvoking Churn Prediction Agent...")
        churn_results = run_churn_agent(business_context)

        # 3. Pricing Intelligence
        print("\nInvoking Pricing Intelligence Agent...")
        pricing_results = run_pricing_agent(business_context)

        # 4. Upsell and Cross-sell
        print("\nInvoking Upsell and Cross-sell Agent...")
        upsell_results = run_upsell_agent(business_context)

        # Consolidate business intelligence
        summary = {
            "total_subscriptions": len(df),
            "renewal_opportunities": len(renewal_results),
            "churn_risk_customers": len(churn_results),
            "pricing_opportunities": len(pricing_results),
            "upsell_opportunities": len(upsell_results)
        }

        span.update(output=summary)

        print("\n====================================")
        print("  CONSOLIDATED BUSINESS INTELLIGENCE")
        print("====================================")

        for key, value in summary.items():
            print(f"{key}: {value}")

        print("\nAGENT VIX EXECUTION COMPLETED!")

        return {
            "summary": summary,
            "renewal_results": renewal_results,
            "churn_results": churn_results,
            "pricing_results": pricing_results,
            "upsell_results": upsell_results
        }
