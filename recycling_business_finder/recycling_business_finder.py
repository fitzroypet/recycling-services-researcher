import googlemaps
from typing import List, Dict
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
import os

class RecyclingBusiness:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.materials = set()
        self.website_materials = {}
        self.phone = None
        self.website = None
        self.rating = None
        self.opening_hours = []
        self.coordinates = {}
        self.place_id = None
        self.service_keywords = []  # For storing service keywords
        self.address_components = {}  # For storing detailed address components

    def analyze_business_type(self):
        """Analyze business name and description for material hints"""
        name_lower = self.name.lower()
        
        material_indicators = {
            'plastic': ['plastic', 'pet', 'polymer', 'hdpe', 'ldpe', 'pvc'],
            'metal': ['metal', 'scrap', 'aluminum', 'steel', 'copper', 'iron'],
            'paper': ['paper', 'cardboard', 'newspaper', 'magazine'],
            'glass': ['glass', 'bottles'],
            'electronics': ['electronic', 'e-waste', 'computer', 'phone', 'laptop'],
            'batteries': ['battery', 'batteries', 'accumulator'],
            'automotive': ['car', 'automotive', 'vehicle', 'auto parts'],
            'organic': ['organic', 'compost', 'food waste', 'green waste'],
            'textile': ['textile', 'clothing', 'fabric', 'clothes', 'garment'],
            'general': ['recycling center', 'waste management', 'collection center']
        }
        
        for material, indicators in material_indicators.items():
            if any(indicator in name_lower for indicator in indicators):
                self.materials.add(material)

    def to_dict(self) -> Dict:
        """Convert business object to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'address': self.address,
            'coordinates': self.coordinates,
            'place_id': self.place_id,
            'materials': list(self.materials),
            'website_materials': self.website_materials,
            'phone': self.phone,
            'website': self.website,
            'rating': self.rating,
            'opening_hours': self.opening_hours,
            'service_keywords': self.service_keywords,
            'address_components': self.address_components
        }

class EnhancedRecyclingFinder:
    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)  # This is likely how it's currently implemented
        self.search_radius = int(os.getenv('SEARCH_RADIUS', 5000))
        self.max_results = int(os.getenv('MAX_RESULTS', 100))
        # Define material keywords
        self.material_keywords = {
            'plastic': ['plastic', 'pet', 'hdpe', 'ldpe', 'pvc', 'pp', 'ps'],
            'metal': ['metal', 'scrap metal', 'iron', 'steel', 'copper', 'aluminum'],
            'paper': ['paper', 'cardboard', 'newspaper'],
            'glass': ['glass', 'bottles'],
            'electronics': ['electronic', 'e-waste', 'electronics'],
            'batteries': ['battery', 'batteries'],
            'automotive': ['car', 'vehicle', 'automotive'],
            'organic': ['organic waste', 'food waste', 'compost'],
            'textile': ['clothing', 'clothes', 'textile'],
            'hazardous': ['hazardous']
        }

    def extract_materials_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract material keywords from text."""
        materials = {}
        text = text.lower()
        
        for category, keywords in self.material_keywords.items():
            found_keywords = [kw for kw in keywords if kw in text]
            if found_keywords:
                materials[category] = found_keywords
                
        return materials

    def analyze_website_content(self, url: str) -> Dict:
        """Analyze business website for recycling materials information"""
        if not url:
            return {}
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            materials = {
                'plastic': ['plastic', 'PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS'],
                'metal': ['metal', 'aluminum', 'steel', 'copper', 'iron', 'scrap metal'],
                'paper': ['paper', 'cardboard', 'newspaper', 'magazine'],
                'glass': ['glass', 'bottles'],
                'electronics': ['electronics', 'e-waste', 'computers', 'phones', 'electronic waste'],
                'batteries': ['batteries', 'battery'],
                'automotive': ['automotive', 'car parts', 'vehicle'],
                'organic': ['organic waste', 'compost', 'food waste'],
                'textile': ['textile', 'clothing', 'fabric', 'clothes'],
                'hazardous': ['hazardous', 'chemical', 'paint', 'oil']
            }
            
            found_materials = {}
            text_content = soup.get_text().lower()
            
            for category, keywords in materials.items():
                matches = []
                for keyword in keywords:
                    if keyword.lower() in text_content:
                        matches.append(keyword)
                if matches:
                    found_materials[category] = matches
                    
            return found_materials
            
        except Exception as e:
            print(f"Error analyzing website {url}: {str(e)}")
            return {}

    def search_businesses(self, location: str) -> List[RecyclingBusiness]:
        """Search for recycling businesses with enhanced material analysis"""
        try:
            # Geocode the location
            geocode_result = self.client.geocode(location)
            
            if not geocode_result:
                print(f"Could not find location: {location}")
                return []
            
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            
            print(f"\nSearch center coordinates: {lat}, {lng}")
            
            businesses = []
            search_query = {
                'location': (lat, lng),
                'radius': self.search_radius,
                'keyword': 'recycling',
                'type': 'establishment'
            }
            
            # Get first page
            places_result = self.client.places_nearby(**search_query)
            
            while True:
                # Process current page results
                if 'results' in places_result:
                    print(f"Processing page with {len(places_result['results'])} results")
                    
                    for place in places_result['results']:
                        try:
                            place_details = self.client.place(place['place_id'])['result']
                            
                            business = RecyclingBusiness(
                                name=place.get('name', 'Unknown'),
                                address=place_details.get('formatted_address', 'No address')
                            )
                            
                            # Set additional attributes
                            business.coordinates = {
                                'lat': place['geometry']['location']['lat'],
                                'lng': place['geometry']['location']['lng']
                            }
                            business.place_id = place['place_id']
                            business.phone = place_details.get('formatted_phone_number')
                            business.website = place_details.get('website')
                            business.rating = place.get('rating')
                            business.opening_hours = place_details.get('opening_hours', {}).get('weekday_text', [])
                            
                            # Debug print
                            print(f"Processing business: {business.name}")
                            
                            # Analyze website content
                            website_materials = self.analyze_website_content(business.website)
                            print(f"Website materials found: {website_materials}")
                            
                            # Extract materials from place details
                            place_materials = self.extract_materials_from_text(
                                str(place_details).lower()
                            )
                            print(f"Place materials found: {place_materials}")
                            
                            # Combine materials
                            all_materials = set(website_materials.keys()) | set(place_materials.keys())
                            business.materials = list(all_materials)
                            business.website_materials = {
                                **website_materials,
                                **place_materials
                            }
                            
                            businesses.append(business)
                            
                            # Check if we've reached max_results
                            if len(businesses) >= self.max_results:
                                print(f"Reached maximum results limit: {self.max_results}")
                                return businesses
                                
                        except Exception as e:
                            print(f"Error processing place {place.get('name', 'Unknown')}: {str(e)}")
                            continue
                
                # Check for next page
                if 'next_page_token' in places_result:
                    print("Getting next page of results...")
                    sleep(2)  # Wait 2 seconds before requesting next page (API requirement)
                    places_result = self.client.places_nearby(
                        page_token=places_result['next_page_token']
                    )
                else:
                    print("No more pages available")
                    break
            
            print(f"Total businesses found: {len(businesses)}")
            return businesses
            
        except Exception as e:
            print(f"Error in search: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return []

def main():
    # Replace with your Google API key
    GOOGLE_API_KEY = 'YOUR-API-KEY-HERE'
    
    finder = EnhancedRecyclingFinder(GOOGLE_API_KEY)
    
    try:
        location = input("Enter location (city, country): ")
        print("\nSearching for recycling businesses and analyzing materials...")
        results = finder.search_businesses(location)
        
        print(f"\nFound {len(results)} recycling businesses:\n")
        
        # Save results to JSON file
        filename = f"{location.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([business.to_dict() for business in results], f, indent=2, ensure_ascii=False)
        
        # Display results
        for business in results:
            print(f"\nName: {business.name}")
            print(f"Address: {business.address}")
            print(f"Coordinates: {business.coordinates['lat']}, {business.coordinates['lng']}")
            print(f"Place ID: {business.place_id}")
            
            # Display detailed address components if available
            if business.address_components:
                print("\nAddress Components:")
                for component_type, name in business.address_components.items():
                    print(f"  {component_type}: {name}")
            
            print(f"Phone: {business.phone}")
            print(f"Website: {business.website}")
            if business.rating:
                print(f"Rating: {business.rating}")
            
            if business.materials:
                print("\nMaterials Handled:")
                print(", ".join(sorted(business.materials)))
            
            if business.website_materials:
                print("\nDetailed Materials (from website analysis):")
                for category, keywords in business.website_materials.items():
                    print(f"- {category}: {', '.join(keywords)}")
            
            if business.opening_hours:
                print("\nOpening Hours:")
                for hours in business.opening_hours:
                    print(f"  {hours}")
                    
            print("\n" + "-"*50 + "\n")
            
        print(f"\nResults have been saved to {filename}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()