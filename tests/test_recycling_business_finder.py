import pytest
from recycling_business_finder.recycling_business_finder import RecyclingBusiness, EnhancedRecyclingFinder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@pytest.fixture
def recycling_business():
    """Create a sample recycling business for testing"""
    return RecyclingBusiness(
        name="Test Recycling Center",
        address="123 Test Street, Newcastle, UK"
    )

@pytest.fixture
def finder():
    """Create an instance of EnhancedRecyclingFinder"""
    api_key = os.getenv('GOOGLE_API_KEY')
    return EnhancedRecyclingFinder(api_key)

def test_recycling_business_initialization(recycling_business):
    """Test if RecyclingBusiness is initialized correctly"""
    assert recycling_business.name == "Test Recycling Center"
    assert recycling_business.address == "123 Test Street, Newcastle, UK"
    assert isinstance(recycling_business.materials, set)
    assert isinstance(recycling_business.website_materials, dict)

def test_recycling_business_to_dict(recycling_business):
    """Test if to_dict method works correctly"""
    business_dict = recycling_business.to_dict()
    assert isinstance(business_dict, dict)
    assert business_dict['name'] == "Test Recycling Center"
    assert business_dict['address'] == "123 Test Street, Newcastle, UK"

def test_finder_initialization(finder):
    """Test if EnhancedRecyclingFinder is initialized correctly"""
    assert finder.client is not None
    assert finder.search_radius == int(os.getenv('SEARCH_RADIUS', 5000))
    assert finder.max_results == int(os.getenv('MAX_RESULTS', 100))

def test_finder_search_businesses(finder):
    """Test if search_businesses method returns results"""
    results = finder.search_businesses("Newcastle, UK")
    assert isinstance(results, list)
    if results:  # If API returns results
        assert all(isinstance(business, RecyclingBusiness) for business in results)

def test_business_type_analysis(recycling_business):
    """Test business type analysis"""
    recycling_business.name = "Metal Recycling Center"
    recycling_business.analyze_business_type()
    assert "metal" in recycling_business.materials

def test_website_content_analysis(finder):
    """Test website content analysis"""
    test_url = "http://example.com"  # Use a mock website
    materials = finder.analyze_website_content(test_url)
    assert isinstance(materials, dict) 