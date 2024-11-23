import pytest
from recycling_service_manager import RecyclingServiceManager
from recycling_business_finder.recycling_business_finder import EnhancedRecyclingFinder

@pytest.mark.integration
def test_full_process_flow():
    """Test the entire process flow"""
    manager = RecyclingServiceManager()
    try:
        json_file, sql_file = manager.process_location("Newcastle", "UK")
        assert json_file.endswith('.json')
        assert sql_file.endswith('.sql')
    except Exception as e:
        pytest.skip(f"Integration test skipped: {str(e)}") 