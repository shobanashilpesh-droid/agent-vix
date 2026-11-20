
from data.synthetic_data import generate_adobe_data
from orchestrator import run_agent_vix
from langfuse import get_client

# Generate synthetic Adobe subscription data
df = generate_adobe_data()

print("Total subscriptions:", len(df))

# Execute Agent VIX
results = run_agent_vix(df)

# Display individual agent results
print("\n========== RENEWAL RESULTS ==========")
print(results["renewal_results"].to_string(index=False))

print("\n========== CHURN RESULTS ==========")
print(results["churn_results"].to_string(index=False))

print("\n========== PRICING RESULTS ==========")
print(results["pricing_results"].to_string(index=False))

print("\n========== UPSELL RESULTS ==========")
print(results["upsell_results"].to_string(index=False))

# Flush Langfuse traces
#get_client().flush()

#print("\nAgent VIX execution completed successfully!")

# Flush all pending Langfuse observations
langfuse = get_client()
langfuse.flush()

print("\nLangfuse traces flushed successfully!")
