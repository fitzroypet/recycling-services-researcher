from http.server import BaseHTTPRequestHandler
import json

def handler(request):
    """Vercel serverless function handler"""
    try:
        # Get query parameters
        query = request.query
        city = query.get('city', '')
        country = query.get('country', '')

        # Return test response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Test response",
                "query": {
                    "city": city,
                    "country": country
                }
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        } 