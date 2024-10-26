## Phone Tracker

This project is a phone number tracking tool that locates the approximate geographical registration area of a phone number and displays it on an interactive map. It combines multiple sources, including OpenCage Geocoding and IP-based location detection, to provide an enhanced and detailed location experience. 

### Features

- **Phone Number Registration Location**: Detects the approximate registered region and time zone of a phone number using the `phonenumbers` library.
- **Real-time IP Location**: Obtains the user’s approximate real-time location based on IP data.
- **Reverse Geocoding with OpenCage**: Converts latitude and longitude into an approximate address to enhance location data.
- **Interactive Map Visualization**: Displays the detected location on a map using `folium` with the ability to save the map as an HTML file.
- This tool combines information from multiple APIs to enhance accuracy and present a clear visualization of location data. Its combination of IP-based and phone registration data gives it an edge for general geographic insights, making it valuable for research and security purposes.

### Prerequisites

- Python 3.x
- The following Python libraries:
  - `phonenumbers`
  - `folium`
  - `requests`
  - `argparse`
  - `colorama`
  
Install dependencies using:
```bash
pip install phonenumbers folium requests argparse colorama
```

### Usage

1. **Set up your OpenCage API Key**:
   Replace the placeholder `OPENCAGE_API_KEY` with your actual OpenCage API key in the script.

2. **Run the Script**:
   Use the following command to run the tracker, providing the phone number with country code.

   ```bash
   python phone_tracker.py -p +1234567890
   ```

3. **Results**:
   - The script will display details about the phone number’s region, carrier, and time zone.
   - It will detect and print the current IP-based location and will attempt to reverse geocode it using OpenCage.
   - Finally, it saves an interactive map (HTML file) showing the location, which can be opened in any browser.

## Disclaimer

Use this tool responsibly. It is designed for educational purposes and should respect privacy and legal boundaries. Ensure you have permission before tracking or displaying location information.

