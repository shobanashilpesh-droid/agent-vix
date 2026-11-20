
from data.synthetic_data import generate_adobe_data
from smart_orchestrator import run_smart_agent_vix
from langfuse import get_client

# Generate synthetic Adobe subscription data
df = generate_adobe_data()

print("\nTotal subscriptions:", len(df))

# Execute Smart Agent VIX
results = run_smart_agent_vix(df)

# Display orchestration summary
print("\n========== AGENT VIX SUMMARY ==========")
print(results["summary"])

# Display results only for agents that were invoked
for agent_name, result_key in [
    ("Renewal Intelligence", "renewal_results"),
    ("Churn Prediction", "churn_results"),
    ("Pricing Intelligence", "pricing_results"),
    ("Upsell and Cross-sell", "upsell_results")
]:
    if result_key in results:
        print(f"\n========== {agent_name} RESULTS ==========")
        print(results[result_key].to_string(index=False))

# Flush Langfuse observations
get_client().flush()

print("\nSmart Agent VIX execution completed!")
