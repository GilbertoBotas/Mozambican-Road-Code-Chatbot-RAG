import os
from dotenv import load_dotenv

load_dotenv()

def validate_and_load_environment():
    """Validate that all required environment variables are set."""
    required_vars = [
        'GOOGLE_API_KEY'
    ]
    missing = []
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)

    if missing:
        error_msg = "Missing required environment variables: " + ", ".join(missing)
        raise EnvironmentError(error_msg)
    
    print("All required environment variables are set.")