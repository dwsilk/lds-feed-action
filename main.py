"""LINZ Data Service History Feed - GitHub Action.

This script allows the user to interrogate a LINZ Data Service layer to
retrieve statistics about the most recent data update within a specified
timeframe.

It accepts a LINZ Data Service layer identifier and a timeframe specified
in either minutes, hours or days.

This script requires that `atoma`, `pendulum`, `requests` and `beautifulsoup4`
be installed within the Python environment you are running this script in (see
requirements.txt).

This file can also be imported as a module and contains the following
functions:

    * diff_timeframe - returns the time between now and when the most recent
      update was published
    * extract_feature_counts - extracts the feature counts from the html
      summary provided within the Atom feed for the most recent update
    * main - the main function of the script
"""

import os

import atoma
import pendulum
import requests
from bs4 import BeautifulSoup


OUTPUT_TIMEZONE = "Pacific/Auckland"
OUTPUT_TIME_FORMAT = "MMM Do YYYY at HH:mm"


def diff_timeframe(now: pendulum.DateTime, published_datetime: pendulum.DateTime, units: str) -> int:
    """Determine time since data update was published.

    Parameters
    ----------
    now : pendulum.DateTime
        The current datetime.
    published_datetime : pendulum.DateTime
        The datetime for the published update.
    units : str
        Either "minutes", "hours" or "days".

    Returns
    -------
    int
        The amount of time that has elapsed since the dataset was updated.
    """
    if units == "minutes":
        time_since_publish = now.diff(published_datetime).in_minutes()
    if units == "hours":
        time_since_publish = now.diff(published_datetime).in_hours()
    if units == "days":
        time_since_publish = now.diff(published_datetime).in_days()

    return time_since_publish


def extract_feature_counts(html_summary: str) -> tuple:
    """Extract features counts from html summary using BeautifulSoup.

    Parameters
    ----------
    html_summary : str
        The dataset update summary component from the LINZ Data Service Atom
        feed.

    Returns
    -------
    tuple
        (total_features, adds, modifies, deletes, total_changes)
    """
    soup = BeautifulSoup(html_summary, features="html.parser")
    feature_counts = soup.find_all("td")

    total_features = feature_counts[0].string
    adds = feature_counts[1].string
    modifies = feature_counts[2].string
    deletes = feature_counts[3].string
    total_changes = int(adds) + int(modifies) + int(deletes)

    return (total_features, adds, modifies, deletes, total_changes)


def main():  # pylint: disable=too-many-locals
    """Intended to be used as part of a GitHub Action.

    Requires INPUT_LAYERID, INPUT_TIMEFRAME and INPUT_UNITS environment
    variables to be set within the environment that the script is run.

    Prints "set-output" commands that create Outputs within GitHub Actions.
    The Outputs created are:

        * updateFound - True if an update was found within the specified
          timeframe, otherwise False
        * publishedTime - The time the data update was published
        * totalFeatures - The total number of features in the entire dataset
          after the update
        * adds - The number of added features in the update
        * modifies - The number of modified features in the update
        * deletes - The number of deleted features in the update

    Raises
    ------
    ValueError
        If environment variable INPUT_UNITS is not either "minutes", "hours"
        or "days".
    """
    layer_id = os.environ["INPUT_LAYERID"]
    timeframe = int(os.environ["INPUT_TIMEFRAME"])
    units = os.environ["INPUT_UNITS"]

    if units not in ["minutes", "hours", "days"]:
        raise ValueError("units should be either 'minutes', 'hours' or 'days'")

    response = requests.get(f"https://data.linz.govt.nz/feeds/layers/{layer_id}/revisions/")
    feed = atoma.parse_atom_bytes(response.content)

    update_found = False
    dataset_title = None
    revision_number = None
    total_features = None
    adds = None
    modifies = None
    deletes = None
    published_time = None

    todays_date = pendulum.now("UTC")

    for entry in feed.entries:

        published_time = pendulum.instance(entry.published)
        time_since_publish = diff_timeframe(todays_date, published_time, units)

        if time_since_publish < timeframe:
            total_features, adds, modifies, deletes, total_changes = extract_feature_counts(entry.summary.value)

            if total_changes == 0:
                continue

            update_found = True
            dataset_title = entry.title.value.split(f" ({layer_id}", 1)[0]
            revision_number = entry.title.value.rsplit(" ", 1)[-1]

            break

        published_time = None

    if published_time:
        published_time = published_time.in_timezone(OUTPUT_TIMEZONE)
        published_time = published_time.format(OUTPUT_TIME_FORMAT)

    print(f"::set-output name=updateFound::{update_found}")
    print(f"::set-output name=datasetTitle::{dataset_title}")
    print(f"::set-output name=revisionNumber::{revision_number}")
    print(f"::set-output name=publishedTime::{published_time}")
    print(f"::set-output name=totalFeatures::{total_features}")
    print(f"::set-output name=adds::{adds}")
    print(f"::set-output name=modifies::{modifies}")
    print(f"::set-output name=deletes::{deletes}")


if __name__ == "__main__":
    main()
