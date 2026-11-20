
from data.synthetic_data import generate_adobe_data
from smart_orchestrator import run_smart_agent_vix
from langfuse import get_client

# Generate synthetic data
df = generate_adobe_data()

# Create a scenario with no high churn risk
df["churn_propensity"] = 0.30

print("\nTEST SCENARIO")
print("All customers have churn propensity of 30%")
print("Expected: Churn Prediction Agent should be skipped")

# Execute Agent VIX
results = run_smart_agent_vix(df)

# Display routing decisions
print("\nAGENT ROUTING RESULTS")

print("Invoked agents:")
for agent in results["summary"]["agents_invoked"]:
    print("-", agent)

print("\nSkipped agents:")
for agent in results["summary"]["agents_skipped"]:
    print("-", agent)

# Verify expected behavior
assert (
    "Churn Prediction Agent"
    in results["summary"]["agents_skipped"]
), "Churn Agent should have been skipped!"

assert (
    "Churn Prediction Agent"
    not in results["summary"]["agents_invoked"]
), "Churn Agent should not have been invoked!"

get_client().flush()

print("\nCONDITIONAL ROUTING TEST PASSED!")
