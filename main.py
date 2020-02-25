"""This is the module."""

import os

import atoma
import pendulum
import requests
from bs4 import BeautifulSoup


def diff_timeframe(now: pendulum.DateTime, published_datetime: pendulum.DateTime, units: str) -> int:
    """Determine time since data update was published.
    """
    if units == "minutes":
        time_since_publish = now.diff(published_datetime).in_minutes()
    if units == "hours":
        time_since_publish = now.diff(published_datetime).in_hours()
    if units == "days":
        time_since_publish = now.diff(published_datetime).in_days()

    return time_since_publish


def extract_feature_counts(html_summary: str) -> tuple:
    """Extract the features counts using BeautifulSoup"""

    soup = BeautifulSoup(html_summary, features="html.parser")
    feature_counts = soup.find_all("td")

    total_features = feature_counts[0].string
    adds = feature_counts[1].string
    modifies = feature_counts[2].string
    deletes = feature_counts[3].string
    total_changes = int(adds) + int(modifies) + int(deletes)

    return (total_features, adds, modifies, deletes, total_changes)


def main():  # pylint: disable=too-many-locals
    """This is the main function."""
    layer_id = os.environ["INPUT_LAYERID"]
    timeframe = int(os.environ["INPUT_TIMEFRAME"])
    units = os.environ["INPUT_UNITS"]

    if units not in ["minutes", "hours", "days"]:
        raise ValueError("units should be either 'minutes', 'hours' or 'days'")

    response = requests.get(f"https://data.linz.govt.nz/feeds/layers/{layer_id}/revisions/")
    feed = atoma.parse_atom_bytes(response.content)

    update_found = False
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

            break

        published_time = None

    if published_time:
        published_time = published_time.format("MMM Do YYYY at HH:mm")

    print(f"::set-output name=updateFound::{update_found}")
    print(f"::set-output name=publishedTime::{published_time}")
    print(f"::set-output name=totalFeatures::{total_features}")
    print(f"::set-output name=adds::{adds}")
    print(f"::set-output name=modifies::{modifies}")
    print(f"::set-output name=deletes::{deletes}")


if __name__ == "__main__":
    main()
