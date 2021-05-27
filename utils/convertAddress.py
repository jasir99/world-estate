import math
import googlemaps
from .keys import getGoogleMapsApiKey

"""Make sure not to publish the API key in GitHub please!!!"""

gmaps = googlemaps.Client(key=getGoogleMapsApiKey())

def shortGeoCode(lat, lng):
    lat = int(lat)
    lng = int(lng)
    if float(lat) < 0:
        lat = 'n{}'.format(abs(lat))
    if float(lng) < 0:
        lng = 'n{}'.format(abs(lng))
    return '{}m{}'.format(lat, lng)


def reverseAddress(lat, lng):
    lat = float(lat)
    lng = float(lng)
    city = None
    country = None
    administrative = None
    geocode_result = gmaps.reverse_geocode((lat, lng))[0]
    for n in geocode_result['address_components']:
        if 'locality' in n['types'] or 'postal_town' in n['types'] or 'neighborhood' in n['types']:
            city = n['long_name']
            continue
        if 'country' in n['types']:
            country = n['long_name']
            continue
        if 'administrative_area_level_1' in n['types']:
            administrative = n['long_name']

    if city is None:
        city = administrative

    data = {
        'city': city,
        'country': country,
        'full_address': geocode_result['formatted_address'],
        'latitude': lat,
        'longitude': lng,
    }
    return data

def getCity(lat,lng):
    geocode_result = gmaps.reverse_geocode((lat, lng))[0]['address_components']
    city = None
    administrative = None
    for n in geocode_result:
        if 'locality' in n['types'] or 'postal_town' in n['types'] or 'neighborhood' in n['types']:
            city = n['long_name']
            break
        if 'administrative_area_level_1' in n['types']:
            administrative = n['long_name']

    if city is None:
        return administrative
    return city
