# recycling_service_manager.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Optional
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recycling_business_finder.recycling_business_finder import EnhancedRecyclingFinder
from recycling_data_engineer.reporting_engineer import generate_sql_statements

# Load environment variables
load_dotenv()

# Check the API key
api_key = os.getenv('GOOGLE_API_KEY')
print(f"Using Google API Key: {api_key}")

class RecyclingServiceManager:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        self.json_data = None
        self.sql_statements = None
        self.json_filename = None
        self.sql_filename = None

    def generate_filenames(self, city: str, country: str) -> tuple:
        """Generate consistent filenames for both JSON and SQL files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"{city.replace(' ', '_').lower()}_{country.replace(' ', '_').lower()}"
        
        # Create output directory if it doesn't exist
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        self.json_filename = os.path.join(output_dir, f"{base_name}_{timestamp}.json")
        self.sql_filename = os.path.join(output_dir, f"{base_name}.sql")
        return self.json_filename, self.sql_filename

    def find_recycling_services(self, city: str, country: str) -> None:
        """Find recycling services and store the results."""
        try:
            location = f"{city}, {country}"
            print(f"Searching for recycling services in {location}...")
            
            finder = EnhancedRecyclingFinder(self.api_key)
            results = finder.search_businesses(location)
            
            # Debugging: Check the results
            print(f"Results from API: {results}")
            
            if not results:  # Check if results are empty
                print("No results found from the API.")
                self.json_data = []  # Initialize as empty list
                return
            
            self.json_data = [business.to_dict() for business in results]
            
            # Generate filenames
            self.generate_filenames(city, country)
            
            print(f"Found {len(self.json_data)} recycling businesses")
            
        except Exception as e:
            print(f"Error finding recycling services: {str(e)}")
            self.json_data = []  # Initialize as empty list in case of error
            raise

    def generate_sql(self) -> None:
        """Generate SQL statements from stored JSON data."""
        try:
            if not self.json_data:
                raise ValueError("No JSON data available. Run find_recycling_services first.")
                
            self.sql_statements = generate_sql_statements(self.json_data)
            
        except Exception as e:
            print(f"Error generating SQL statements: {str(e)}")
            raise

    def save_json_data(self) -> None:
        """Save JSON data to file."""
        if not self.json_data or not self.json_filename:
            raise ValueError("No JSON data or filename available")
        
        try:
            with open(self.json_filename, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)
            print(f"JSON data saved to: {self.json_filename}")
        except Exception as e:
            print(f"Error saving JSON data: {str(e)}")
            raise

    def save_sql_statements(self) -> None:
        """Save SQL statements to file."""
        if not self.sql_statements or not self.sql_filename:
            raise ValueError("No SQL statements or filename available")
        
        try:
            with open(self.sql_filename, 'w', encoding='utf-8') as f:
                f.write(self.sql_statements)
            print(f"SQL statements saved to: {self.sql_filename}")
        except Exception as e:
            print(f"Error saving SQL statements: {str(e)}")
            raise

    def process_location(self, city: str, country: str) -> tuple:
        """Main method to process a location and return filenames."""
        try:
            # Step 1: Find recycling services and generate filenames
            self.find_recycling_services(city, country)
            
            # Check if JSON data is available before processing
            if not self.json_data:  # Assuming json_data is the variable holding your JSON
                print("Error processing location: No JSON data available")
                return  # Exit the function if no data is available
            
            # Step 2: Save JSON data
            self.save_json_data()
            
            # Step 3: Generate SQL statements
            self.generate_sql()
            
            # Step 4: Save SQL statements
            self.save_sql_statements()
            
            print(f"\nProcess completed successfully!")
            print(f"JSON data saved to: {self.json_filename}")
            print(f"SQL statements saved to: {self.sql_filename}")
            
            return self.json_filename, self.sql_filename

        except Exception as e:
            print(f"Error processing location: {str(e)}")
            raise

def main():
    try:
        # Get city and country from command line arguments
        if len(sys.argv) != 3:
            print("Usage: python recycling_service_manager.py <city> <country>")
            sys.exit(1)
        
        city = sys.argv[1]
        country = sys.argv[2]
        
        # Initialize and run the manager
        manager = RecyclingServiceManager()
        json_file, sql_file = manager.process_location(city, country)
        
        print(f"\nProcess completed successfully!")
        print(f"JSON data saved to: {json_file}")
        print(f"SQL statements saved to: {sql_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    main()