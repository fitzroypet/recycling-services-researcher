import pytest
import time
from recycling_service_manager import RecyclingServiceManager

@pytest.mark.performance
def test_search_performance():
    """Test performance of search operation"""
    manager = RecyclingServiceManager()
    start_time = time.time()
    manager.find_recycling_services("Newcastle", "UK")
    end_time = time.time()
    
    execution_time = end_time - start_time
    assert execution_time < 10  # Should complete within 10 seconds 