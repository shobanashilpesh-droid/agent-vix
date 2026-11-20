
from data.synthetic_data import generate_adobe_data
from agents.churn_agent import run_churn_agent
from langfuse import get_client

# Generate synthetic Adobe subscription data
df = generate_adobe_data()

# Execute Churn Prediction Agent
result = run_churn_agent(df)

print("\nCHURN RISK CUSTOMERS")
print(result.to_string(index=False))

# Send observations to Langfuse
get_client().flush()
