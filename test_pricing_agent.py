
from data.synthetic_data import generate_adobe_data
from agents.pricing_agent import run_pricing_agent
from langfuse import get_client

# Generate synthetic Adobe subscription data
df = generate_adobe_data()

# Execute Pricing Intelligence Agent
result = run_pricing_agent(df)

print("\nPRICING OPPORTUNITIES")
print(result.to_string(index=False))

# Flush observations to Langfuse
get_client().flush()
