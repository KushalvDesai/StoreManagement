import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Check FIRST_RUN flag (defaults to true if not found)
first_run = os.getenv("FIRST_RUN", "true").lower() == "true"

# Run setup or main app based on flag
if first_run:
    os.system("python setup.py")
else:
    os.system("python main.py")