import logging as log
import sys
import json
import pandas as pd
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from src.pipelines.trip import TripPipeline


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
    return parser.parse_args()


def main() -> None:
    """
    Main function.
    """

    log.info("Starting the script...")
    args = get_args()

    trips = pd.read_csv(args.file)
    trips = trips.to_dict("records")

    for trip in trips:
        data = json.dumps(trip)
        trip_pipeline = TripPipeline(data)
        trip_pipeline.run()

    log.info("Script finished.")


if __name__ == "__main__":
    log.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=log.INFO,
        stream=sys.stdout
    )
    main()