from data.synthetic_data import generate_adobe_data
from agents.renewal_agent import run_renewal_agent

# Generate synthetic Adobe data
df = generate_adobe_data()

# Execute Renewal Agent
result = run_renewal_agent(df)

print("\nRENEWAL OPPORTUNITIES")
print(result.to_string(index=False))

from langfuse import get_client

get_client().flush()