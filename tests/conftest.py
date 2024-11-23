import pytest
from unittest.mock import Mock
import os
from dotenv import load_dotenv
from recycling_services_researcher import RecyclingServiceManager
from recycling_business_finder.recycling_business_finder import EnhancedRecyclingFinder

# Load environment variables
load_dotenv()

@pytest.fixture
def api_key():
    """Provide API key for tests"""
    return os.getenv('GOOGLE_API_KEY')

@pytest.fixture
def mock_google_client(mocker):
    """Provide a mock Google Maps client"""
    mock_client = Mock()
    mocker.patch('googlemaps.Client', return_value=mock_client)
    return mock_client

@pytest.fixture
def manager(mock_google_client):
    """Create a RecyclingServiceManager instance with mocked dependencies"""
    return RecyclingServiceManager()

@pytest.fixture
def mock_geocode_response():
    """Provide mock geocode response"""
    return [{
        'geometry': {
            'location': {
                'lat': 51.5074,
                'lng': -0.1278
            }
        }
    }]

@pytest.fixture
def mock_places_response():
    """Provide mock places response"""
    return {
        'results': [{
            'name': 'Test Recycling',
            'formatted_address': '123 Test St',
            'place_id': 'test123',
            'geometry': {
                'location': {
                    'lat': 51.5074,
                    'lng': -0.1278
                }
            },
            'rating': 4.5
        }]
    }

@pytest.fixture
def mock_place_details():
    """Provide mock place details response"""
    return {
        'result': {
            'formatted_address': '123 Test St',
            'formatted_phone_number': '123-456-7890',
            'website': 'http://example.com',
            'opening_hours': {
                'weekday_text': [
                    'Monday: 9:00 AM - 5:00 PM',
                    'Tuesday: 9:00 AM - 5:00 PM'
                ]
            },
            'address_components': [{
                'long_name': 'Test City',
                'types': ['locality']
            }]
        }
    } 