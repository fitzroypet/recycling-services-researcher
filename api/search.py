from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
from dotenv import load_dotenv
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recycling_business_finder.recycling_business_finder import EnhancedRecyclingFinder

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Parse query parameters
        query_params = request.query
        city = query_params.get('city')
        country = query_params.get('country')
        
        if not city or not country:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'Missing city or country parameter'
                })
            }
        
        # Get API key from environment
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'status': 'error',
                    'message': 'API key not configured'
                })
            }

        # Initialize finder and search
        finder = EnhancedRecyclingFinder(api_key)
        results = finder.search_businesses(f"{city}, {country}")
        
        # Return results
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'success',
                'data': [business.to_dict() for business in results]
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        } 