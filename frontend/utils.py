"""
Utility functions for the frontend application
"""
from config import DEFAULT_VALUES


def get_categories(api_data):
    """
    Get category values from API data or fall back to defaults
    
    Args:
        api_data (dict): API response with supported values
        
    Returns:
        dict: Dictionary of category values
    """
    if api_data and api_data.get('success'):
        valid_cats = api_data.get('valid_categories', {})
        return {
            'manufacturers': valid_cats.get('manufacturer', DEFAULT_VALUES['manufacturers']),
            'fuels': valid_cats.get('fuel', DEFAULT_VALUES['fuels']),
            'transmissions': valid_cats.get('transmission', DEFAULT_VALUES['transmissions']),
            'drives': valid_cats.get('drive', DEFAULT_VALUES['drives']),
            'title_status': valid_cats.get('title_status', DEFAULT_VALUES['title_status']),
            'sizes': valid_cats.get('size', DEFAULT_VALUES['sizes']),
            'types': valid_cats.get('type', DEFAULT_VALUES['types']),
            'colors': valid_cats.get('paint_color', DEFAULT_VALUES['colors']),
            'conditions': valid_cats.get('condition', DEFAULT_VALUES['conditions']),
            'states': valid_cats.get('state', DEFAULT_VALUES['states'])
        }
    else:
        return DEFAULT_VALUES
