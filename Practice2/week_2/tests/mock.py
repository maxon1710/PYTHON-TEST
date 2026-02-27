import requests
from unittest.mock import patch


def good_weather():
    response = requests.get(
        url='http://some-url.com',
        params={'city': 'London'}
    ).json()

    return True if response['temp'] > 20 else False


with patch('requests.get') as mock:
    mock_response = mock.return_value
    mock_response.json.return_value = {"temp": 25}

    weather_quality = good_weather()

print(weather_quality)