import os
from pathlib import Path

def load_env_file():
    """
    Load environment variables from .env file
    """
    env_file = Path(__file__).parent / '.env'

    if not env_file.exists():
        return

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                # Set environment variable
                os.environ[key] = value

# Load environment variables when this module is imported
load_env_file()
