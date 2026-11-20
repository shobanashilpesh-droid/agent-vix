from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

langfuse = get_client()

with langfuse.start_as_current_observation(
    as_type="span",
    name="Agent VIX - Connection Test"
) as span:

    span.update(
        input={"message": "Testing Agent VIX connectivity"}
    )

    span.update(
        output={"status": "Langfuse connected successfully"}
    )

langfuse.flush()

print("Langfuse test completed!")