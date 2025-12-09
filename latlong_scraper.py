from geopy.geocoders import Nominatim
import pandas as pd
import time

# Define Islamabad locations
locations = ['DHA Phase 1', 'G-15', 'Bahria Town', 'G-12', 'I-8', 'G-9', 'Margalla Hills', 'F-6', 'F-11', 'G-13',
             'F-8', 'G-14', 'E-7', 'G-10', 'F-7', 'DHA Phase 2', 'G-6', 'Chaklala', 'G-11', 'F-10', 'Rawalp',
             'DHA Phase 3', 'F-5', 'E-11', 'Gulzar-e-Quaid', 'Sadiqabad']

# Manually added coordinates for locations that couldn't be found
manual_coordinates = {
    'Rawalp': (33.1895, 73.1797),
    'Gulzar-e-Quaid': (33.6500, 73.1800),
    'E-7': (33.7253, 73.0454),
    'DHA Phase 2': (33.5273, 73.1609)
}

# Initialize geocoder
geolocator = Nominatim(user_agent="islamabad_location_scraper")


# Function to get latitude and longitude
def get_coordinates(location):
    try:
        # Check if location has manual coordinates
        if location in manual_coordinates:
            return manual_coordinates[location]

        # Add Islamabad to location for better accuracy
        full_location = f"{location}, Islamabad, Pakistan"

        # Geocode the location
        location_data = geolocator.geocode(full_location)

        if location_data:
            latitude = location_data.latitude
            longitude = location_data.longitude
            return latitude, longitude
        else:
            print(f"Location not found: {location}")
            return None, None

    except Exception as e:
        print(f"Error fetching coordinates for {location}: {e}")
        return None, None


# Function to format coordinates with directions
def format_coordinates(latitude, longitude):
    if latitude is None or longitude is None:
        return None

    # Determine North/South
    lat_dir = "N" if latitude >= 0 else "S"
    # Determine East/West
    lon_dir = "E" if longitude >= 0 else "W"

    # Format: 28.3603° N, 70.0456° E
    coordinates = f"{abs(latitude):.4f}° {lat_dir}, {abs(longitude):.4f}° {lon_dir}"
    return coordinates


# Create a list to store data
data_list = []

# Iterate over locations and fetch coordinates
print("Scraping coordinates for Islamabad locations...")
for location in locations:
    print(f"Fetching coordinates for: {location}")
    latitude, longitude = get_coordinates(location)

    # Format coordinates with directions
    coordinates = format_coordinates(latitude, longitude)

    # Append data to list
    data_list.append({"location": location, "coordinates": coordinates})

    # Add delay to avoid rate limiting
    time.sleep(1)

# Create DataFrame from list
df = pd.DataFrame(data_list)

# Save DataFrame to CSV
df.to_csv("Islam(updt)_location_coordinates.csv", index=False)
print(f"\nScraping complete! Data saved to 'Islam_location_coordinates.csv'")
print(df)