import phonenumbers
import folium
import sys
import argparse
import os
import requests
from phonenumbers import geocoder, timezone, carrier
from colorama import init, Fore

init()

# OpenCage Geocoding API key
OPENCAGE_API_KEY = '98c0136d9ff84515a2ff774d6503adc6'

def process_number(number):
    try:
        # Parse the phone number.
        parsed_number = phonenumbers.parse(number)

        # Display the attempt message
        print(f"{Fore.GREEN}[+] Attempting to track registration location of "
              f"{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}..")

        # Get and display the time zone ID
        print(f"{Fore.GREEN}[+] Time Zone ID: {timezone.time_zones_for_number(parsed_number)}")

        # Get the geographic location of the phone number registration.
        location = geocoder.description_for_number(parsed_number, "en")
        if location:
            print(f"{Fore.GREEN}[+] Registered Region: {location}")
        else:
            print(f"{Fore.RED}[-] Region: Unknown")

        # Get the service provider (carrier)
        service_provider = carrier.name_for_number(parsed_number, 'en')
        if service_provider:
            print(f"{Fore.GREEN}[+] Service Provider: {service_provider}")
        else:
            print(f"{Fore.RED}[-] Service Provider: Unknown")

    except Exception as e:
        print(f"{Fore.RED}[-] Please specify a valid phone number (with country code) or check your internet connection.")
        sys.exit()

def get_current_location():
    # Attempt to get current real-time location based on IP
    try:
        response = requests.get("http://ipinfo.io")
        data = response.json()
        # Extract latitude and longitude from the "loc" field
        lat, lon = data['loc'].split(',')
        print(f"{Fore.LIGHTRED_EX}[+] Current Approximate Location (based on IP): {data['city']}, {data['region']}, {data['country']}")
        print(f"[+] Latitude: {lat}, Longitude: {lon}")
        return lat, lon, data['city'], data['region'], data['country']
    except Exception as e:
        print(f"{Fore.RED}[-] Could not get the current location based on IP. Please check your internet connection.")
        sys.exit()

# OpenCage API for Reverse Geocoding
def get_location_from_opencage(lat, lon):
    try:
        opencage_url = f"https://api.opencagedata.com/geocode/v1/json?q={lat},{lon}&key={OPENCAGE_API_KEY}"
        response = requests.get(opencage_url)
        if response.status_code == 200:
            location_data = response.json()
            if location_data['results']:
                address = location_data['results'][0]['formatted']  # Use the formatted address
                print(f"{Fore.GREEN}[+] OpenCage Address: {address}")
                return address
            else:
                print(f"{Fore.RED}[-] No results found for OpenCage.")
                return None
        else:
            print(f"{Fore.RED}[-] OpenCage API error: {response.text}")
            return None
    except Exception as e:
        print(f"{Fore.RED}[-] Error using OpenCage API: {e}")
        return None

# Function to display the location on a map
def draw_map(lat, lon, city, region, country):
    try:
        # Create a Folium map centered around the real-time latitude and longitude
        my_map = folium.Map(location=[lat, lon], zoom_start=9)
        # Add a marker at the location
        folium.Marker([lat, lon], popup=f"{city}, {region}, {country}").add_to(my_map)
        # Clean the phone number to create the file name
        cleaned_phone_number = clean_phone_number(args.phone_number)
        file_name = f"{cleaned_phone_number}_location.html"
        # Save the map as an HTML file
        my_map.save(file_name)
        print(f"[+] See Aerial Coverage at: {os.path.abspath(file_name)}")
    
    except NameError:
        print(f"{Fore.RED}[-] Could not get Aerial coverage for this number. Please check the number again.")

def clean_phone_number(phone_number):
    # Remove unwanted characters from the phone number
    cleaned = ''.join(char for part in phone_number for char in part if char.isdigit() or char == '+')
    return cleaned or "unknown"

def cli_argument():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Get approximate location of a Phone number.")
    parser.add_argument("-p", "--phone", dest="phone_number", type=str,
                        help="Phone number to track. Please include the country code when specifying the number.",
                        required=True, nargs="+")
    argument = parser.parse_args()
    
    if not argument.phone_number:
        print(f"{Fore.RED}[-] Please specify the phone number to track (including country code). Use --help to see usage.")
        sys.exit()
    
    return argument

# Parse the command-line arguments
args = cli_argument()

# Track the phone number registration location
process_number("".join(args.phone_number))

# Get the current location based on IP
latitude, longitude, city, region, country = get_current_location()

# Attempt to get location using OpenCage API
location_address = get_location_from_opencage(latitude, longitude)

if location_address:
    print(f"{Fore.GREEN}[+] OpenCage Address: {location_address}")
    draw_map(latitude, longitude, city, region, country)
else:
    print(f"{Fore.RED}[-] Could not retrieve any additional location data.")

