import pytest
from utils import calculate_forecast, check_counterfeit
from datetime import datetime, timedelta

def test_calculate_forecast():
    # Test basic forecast with no last_updated
    assert calculate_forecast("Aspirin", 100, 20, None, 100) == 100
    
    # Test with malaria drug (should apply 1.2 multiplier)
    last_week = (datetime.now() - timedelta(days=7)).isoformat()
    assert calculate_forecast("Malaria Pills", 50, 20, last_week, 100) > 50

def test_check_counterfeit():
    assert check_counterfeit("ABC123") == True
    assert check_counterfeit("FAKE123") == False