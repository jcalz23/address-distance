import os
import pandas as pd
import googlemaps
import time
from dotenv import load_dotenv
from typing import Tuple

def calculate_distance(gmaps: googlemaps.Client, origin: str, destination: str) -> Tuple[float, str]:
    """
    Calculate driving distance between two addresses using Google Maps API
    Returns distance in miles and status
    """
    try:
        result = gmaps.distance_matrix(
            origins=[origin],
            destinations=[destination],
            mode="driving",
            units="imperial"
        )

        if result['status'] != 'OK':
            return None, f"API Error: {result['status']}"

        if result['rows'][0]['elements'][0]['status'] != 'OK':
            return None, f"Route Error: {result['rows'][0]['elements'][0]['status']}"

        # Extract distance in miles
        distance_text = result['rows'][0]['elements'][0]['distance']['text']
        distance_miles = float(distance_text.replace(' mi', ''))
        
        return distance_miles, 'OK'
    except Exception as e:
        return None, f"Error: {str(e)}"


def process_csv(input_path: str, output_path: str, api_key: str) -> None:
    """
    Process a CSV file containing address pairs and calculate distances
    """
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=api_key)
    
    try:
        # Read CSV file
        df = pd.read_csv(input_path)
        
        # Validate columns
        required_columns = ['address1', 'address2']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {', '.join(required_columns)}")
        
        # Initialize results
        distances = []
        statuses = []
        
        # Calculate distances for each pair
        for _, row in df.iterrows():
            distance, status = calculate_distance(gmaps, row['address1'], row['address2'])
            distances.append(distance if distance is not None else None)
            statuses.append(status)
        
        # Add results to dataframe
        df['distance_miles'] = distances
        df['status'] = statuses
        
        # Save results
        df.to_csv(output_path, index=False)
        
    except Exception as e:
        raise Exception(f"Error processing CSV: {str(e)}")


def main():
    """Main function to orchestrate the distance calculation process."""
    # Configuration
    INPUT_FILE = "mileage.csv"
    OUTPUT_FILE = "mileage_with_distances.csv"
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    
    # Process CSV file
    process_csv(INPUT_FILE, OUTPUT_FILE, API_KEY)
    print(f"Processing complete. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
