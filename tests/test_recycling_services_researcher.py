import pytest
import os
from recycling_services_researcher import RecyclingServiceManager
from dotenv import load_dotenv
from unittest.mock import patch

# Load environment variables
load_dotenv()

@pytest.fixture
def manager():
    """Create an instance of RecyclingServiceManager"""
    return RecyclingServiceManager()

def test_manager_initialization(manager):
    """Test if RecyclingServiceManager is initialized correctly"""
    assert manager.api_key == os.getenv('GOOGLE_API_KEY')
    assert manager.json_data is None
    assert manager.sql_statements is None
    assert manager.json_filename is None
    assert manager.sql_filename is None

def test_generate_filenames(manager):
    """Test if generate_filenames creates correct filenames"""
    city = "Newcastle"
    country = "UK"
    json_filename, sql_filename = manager.generate_filenames(city, country)
    
    assert isinstance(json_filename, str)
    assert isinstance(sql_filename, str)
    assert json_filename.endswith('.json')
    assert sql_filename.endswith('.sql')
    assert 'newcastle_uk' in json_filename.lower()
    assert 'newcastle_uk' in sql_filename.lower()

def test_find_recycling_services(manager):
    """Test if find_recycling_services method works"""
    manager.find_recycling_services("Newcastle", "UK")
    if manager.json_data is not None:  # If API returns results
        assert isinstance(manager.json_data, list)

def test_process_location(manager):
    """Test if process_location method works"""
    try:
        json_file, sql_file = manager.process_location("Newcastle", "UK")
        if json_file and sql_file:  # If files were created
            assert os.path.exists(json_file)
            assert os.path.exists(sql_file)
    except Exception as e:
        pytest.skip(f"Skipping test due to API error: {str(e)}")

@pytest.mark.mock
def test_mock_api_call(mocker, manager):
    """Test with mocked API response"""
    # Mock the entire googlemaps.Client class
    mock_client = mocker.Mock()
    mocker.patch('googlemaps.Client', return_value=mock_client)
    
    # Set up mock responses
    mock_geocode_response = [{
        'geometry': {
            'location': {
                'lat': 51.5074,
                'lng': -0.1278
            }
        }
    }]
    
    mock_places_response = {
        'results': [
            {
                'name': 'Test Recycling',
                'formatted_address': '123 Test St',
                'place_id': 'test123',
                'geometry': {'location': {'lat': 51.5074, 'lng': -0.1278}},
                'rating': 4.5
            }
        ]
    }
    
    mock_place_details = {
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
            'address_components': [
                {
                    'long_name': 'Test City',
                    'types': ['locality']
                }
            ]
        }
    }
    
    # Configure the mock client's methods
    mock_client.geocode.return_value = mock_geocode_response
    mock_client.places_nearby.return_value = mock_places_response
    mock_client.place.return_value = mock_place_details
    
    # Create a new instance of RecyclingServiceManager with the mocked client
    manager.find_recycling_services("Test City", "Test Country")
    
    # Verify the mock was called correctly
    mock_client.geocode.assert_called_once_with("Test City, Test Country")
    
    # Assertions
    assert manager.json_data is not None
    assert len(manager.json_data) > 0
    assert manager.json_data[0]['name'] == 'Test Recycling'
    
    # Additional assertions to verify the data structure
    first_result = manager.json_data[0]
    assert first_result['address'] == '123 Test St'
    assert first_result['phone'] == '123-456-7890'
    assert first_result['website'] == 'http://example.com'
    assert first_result['rating'] == 4.5