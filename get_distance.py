import pandas as pd
import googlemaps
import time


def init_google_maps_client(api_key):
    """Initialize and return Google Maps client with the provided API key."""
    return googlemaps.Client(key=api_key)


def calculate_distance(gmaps_client, address1, address2):
    """Calculate driving distance between two addresses in miles."""
    result = gmaps_client.distance_matrix(
        origins=[address1],
        destinations=[address2],
        mode="driving",
        units="imperial"
    )
    
    # Extract distance value (converting meters to miles)
    distance_miles = result["rows"][0]["elements"][0]["distance"]["value"] / 1609.34
    return distance_miles


def process_csv(input_file, output_file, api_key, delay=0.2):
    """Process CSV file and add distance column."""
    # Initialize client
    gmaps = init_google_maps_client(api_key)
    
    # Read CSV file
    df = pd.read_csv(input_file)
    
    # Add distance column
    df["distance_miles"] = None
    
    # Process each row
    for index, row in df.iterrows():
        df.at[index, "distance_miles"] = calculate_distance(
            gmaps, row["address1"], row["address2"]
        )
        
        # Avoid rate limiting
        time.sleep(delay)
    
    # Save results
    df.to_csv(output_file, index=False)
    return df


def main():
    """Main function to orchestrate the distance calculation process."""
    # Configuration
    INPUT_FILE = "addresses.csv"
    OUTPUT_FILE = "addresses_with_distances.csv"
    API_KEY = "YOUR_GOOGLE_API_KEY"
    
    # Process CSV file
    result_df = process_csv(INPUT_FILE, OUTPUT_FILE, API_KEY)
    print(f"Processing complete. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
