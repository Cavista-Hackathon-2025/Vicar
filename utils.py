try:
    from twilio.rest import Client
except ImportError:
    print("Twilio package not installed. Run: pip install twilio")
    raise

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Run: pip install python-dotenv")
    raise

from datetime import datetime
from typing import Optional, List, Dict, Any
import os

# Load environment variables
load_dotenv()

# Server configuration
PORT = int(os.getenv('PORT', 5000))
USE_NGROK = os.getenv('USE_NGROK', 'False').lower() == 'true'
NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')

# Base URL configuration
BASE_URL = f"http://127.0.0.1:{PORT}"

# Twilio configuration with error messages
TWILIO_SID = os.getenv('TWILIO_ACCOUNT_SID')
if not TWILIO_SID:
    raise ValueError("TWILIO_ACCOUNT_SID not found in environment variables")

TWILIO_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_PHONE_NUMBER')
TWILIO_TO = os.getenv('RECIPIENT_PHONE')

# Validate required environment variables
if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM, TWILIO_TO]):
    raise ValueError("Missing required Twilio credentials")

# Validate ngrok configuration f enabled
if USE_NGROK and not NGROK_AUTH_TOKEN:
    raise ValueError("NGROK_AUTH_TOKEN is required when USE_NGROK is True")

client = Client(TWILIO_SID, TWILIO_TOKEN)

VALID_BATCHES: List[str] = ['ABC123', 'XYZ789', 'MNO456']

def calculate_forecast(drug: str, 
                      units_left: int, 
                      restock_at: int,
                      last_updated: Optional[str], 
                      initial_units: int) -> int:
    """
    Calculate restock forecast based on usage patterns.
    
    Args:
        drug: Name of the medication
        units_left: Current quantity in stock
        restock_at: Minimum threshold for reordering
        last_updated: ISO format datetime string of last update
        initial_units: Starting quantity
        
    Returns:
        int: Forecasted units needed for next week
    """
    if not last_updated:
        return units_left
        
    last_time = datetime.fromisoformat(last_updated)
    days_passed = (datetime.now() - last_time).days or 1
    
    # Calculate weekly usage based on the difference over days passed
    usage_rate = ((initial_units - units_left) / days_passed) 
    base_forecast = usage_rate * 7
    
    # Apply seasonal multiplier for malaria drugs
    seasonal_multiplier = 1.2 if "malaria" in drug.lower() else 1.0
    
    # Calculate final forecast
    forecast = int(base_forecast * seasonal_multiplier)
    
    return max(forecast, 0)

def check_counterfeit(batch_number: str) -> bool:
    """
    Check if batch number is in list of valid batches.
    
    Args:
        batch_number: The batch number to validate
        
    Returns:
        bool: True if batch is valid, False otherwise
    """
    return batch_number in VALID_BATCHES

def send_sms(message: str) -> bool:
    """
    Send SMS notification using Twilio.
    
    Args:
        message: The message to send
        
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        return True
    except Exception as e:
        print(f"SMS failed: {e}")
        return False

def get_server_url() -> str:
    """
    Get the current server URL (local or ngrok)
    
    Returns:
        str: The base URL for the server
    """
    return os.getenv('NGROK_URL', BASE_URL)

def format_api_url(endpoint: str) -> str:
    """
    Format a complete API URL
    
    Args:
        endpoint: The API endpoint path
        
    Returns:
        str: The complete URL
    """
    base = get_server_url()
    return f"{base}/api/{endpoint.lstrip('/')}"
