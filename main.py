import logging as log
import sys
import json
import pandas as pd
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from src.trip import Trip


def get_args() -> Namespace:
    """
    Get arguments from the command line.
    """
    parser = ArgumentParser(
        description="""
        This script will read a csv file and insert the data into a database.
        """,
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "--file",
        type=str,
        help="""
        The path to the csv file.
        """
    )

    parser.add_argument(
        "--metric",
        type=str,
        help="""
        Return average number of trips per week for each region.
        """
    )

    return parser.parse_args()


def main() -> None:
    """
    Main function.
    """

    log.info("Starting the script...")
    args = get_args()

    if args.metric == "weekly":
        log.info("Calculating average number of trips per week...")
        trip = Trip(None)
        trip.get_average_trips_per_week()
    
    elif args.metric == "commonly":
        log.info("Getting the latest datasource of two commonly region...")
        trip = Trip(None)
        trip.get_latest_datasource()

    elif args.metric == "cheap_mobile":
        log.info("Getting the number of appearance for data source 'cheap_mobile' in each region...")
        trip = Trip(None)
        trip.get_number_of_appearance()

    elif args.file:

        log.info("Starting data ingestion...")

        trips = pd.read_csv(args.file)
        trips = trips.to_dict("records")

        for trip in trips:
            data = json.dumps(trip)
            trip = Trip(data)
            trip.run()

        log.info("Data ingestion finished...")

    log.info("Script finished.")


if __name__ == "__main__":
    log.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=log.INFO,
        stream=sys.stdout
    )
    main()