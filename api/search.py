from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Import your existing classes
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recycling_business_finder.recycling_business_finder import EnhancedRecyclingFinder

def search_recycling_services(city: str, country: str) -> Dict[str, Any]:
    """Search for recycling services and return results."""
    try:
        # Get API key from environment
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        # Initialize finder
        finder = EnhancedRecyclingFinder(api_key)
        
        # Search for businesses
        location = f"{city}, {country}"
        results = finder.search_businesses(location)
        
        # Convert results to dict
        return {
            "status": "success",
            "data": [business.to_dict() for business in results],
            "count": len(results)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def handler(event, context):
    """Serverless function handler."""
    try:
        # Get query parameters
        params = event.get('queryStringParameters', {})
        city = params.get('city')
        country = params.get('country')

        if not city or not country:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Missing city or country parameter'
                })
            }

        # Search for recycling services
        results = search_recycling_services(city, country)

        # Return response
        return {
            'statusCode': 200 if results['status'] == 'success' else 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(results)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        } 