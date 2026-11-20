
from data.synthetic_data import generate_adobe_data
from agents.upsell_agent import run_upsell_agent
from langfuse import get_client

# Generate synthetic Adobe subscription data
df = generate_adobe_data()

# Execute Upsell and Cross-sell Agent
result = run_upsell_agent(df)

print("\nUPSELL AND CROSS-SELL OPPORTUNITIES")
print(result.to_string(index=False))

# Flush observations to Langfuse
get_client().flush()
