import pytest
from recycling_data_engineer.reporting_engineer import (
    clean_time_string,
    convert_time_format,
    parse_opening_hours,
    match_materials,
    generate_sql_statements
)

def test_clean_time_string():
    """Test if clean_time_string properly cleans time strings"""
    assert clean_time_string("9:00 AM AM") == "9:00 AM"
    assert clean_time_string("9:00PM PM") == "9:00 PM"
    assert clean_time_string("9:00  AM") == "9:00 AM"

def test_convert_time_format():
    """Test if convert_time_format properly converts time formats"""
    assert convert_time_format("9:00 AM") == "09:00:00"
    assert convert_time_format("1:00 PM") == "13:00:00"
    assert convert_time_format("12:00 PM") == "12:00:00"
    assert convert_time_format("12:00 AM") == "00:00:00"

def test_parse_opening_hours():
    """Test if parse_opening_hours correctly parses opening hours"""
    test_hours = [
        "Monday: 9:00 AM - 5:00 PM",
        "Tuesday: Closed",
        "Wednesday: 9:00 AM - 5:00 PM"
    ]
    parsed_hours = parse_opening_hours(test_hours)
    assert isinstance(parsed_hours, list)
    assert len(parsed_hours) == 3
    assert all(len(hour) == 4 for hour in parsed_hours)  # Each tuple should have 4 elements

def test_match_materials():
    """Test if match_materials correctly matches materials"""
    test_materials = ["metal", "plastic"]
    test_website_materials = {
        "metal": ["steel", "aluminum"],
        "plastic": ["PET", "HDPE"]
    }
    test_existing_materials = [
        {"CategoryName": "metal", "Description": "Mixed Metals"},
        {"CategoryName": "plastic", "Description": "Mixed Plastics"}
    ]
    
    matched = match_materials(test_materials, test_website_materials, test_existing_materials)
    assert isinstance(matched, list)
    assert all(isinstance(match, tuple) for match in matched) 