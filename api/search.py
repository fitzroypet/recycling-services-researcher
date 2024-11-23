from http.server import BaseHTTPRequestHandler
import json
import os

def handler(request):
    """Simplified handler for testing"""
    try:
        # Basic response to test the function
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'success',
                'message': 'API is working',
                'query': {
                    'city': request.query.get('city'),
                    'country': request.query.get('country')
                }
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'status': 'error',
                'message': str(e)
            })
        } 