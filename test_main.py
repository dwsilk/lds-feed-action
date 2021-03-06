"""Tests"""

import os

import pytest

from main import main


def test_update_found_using_days(capsys):
    """Test that an update is found using days."""
    os.environ["INPUT_LAYERID"] = "52054"
    os.environ["INPUT_TIMEFRAME"] = "10000"
    os.environ["INPUT_UNITS"] = "days"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::True
::set-output name=datasetTitle::Landonline: Street Address (Deprecated)
::set-output name=revisionNumber::146
::set-output name=publishedTime::Jul 2nd 2017 at 01:47
::set-output name=totalFeatures::1,993,687
::set-output name=adds::43,445
::set-output name=modifies::84,108
::set-output name=deletes::1
"""
    )


def test_update_found_using_hours(capsys):
    """Test that an update is found using hours."""
    os.environ["INPUT_LAYERID"] = "52054"
    os.environ["INPUT_TIMEFRAME"] = "1000000"
    os.environ["INPUT_UNITS"] = "hours"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::True
::set-output name=datasetTitle::Landonline: Street Address (Deprecated)
::set-output name=revisionNumber::146
::set-output name=publishedTime::Jul 2nd 2017 at 01:47
::set-output name=totalFeatures::1,993,687
::set-output name=adds::43,445
::set-output name=modifies::84,108
::set-output name=deletes::1
"""
    )


def test_no_update_found_using_minutes(capsys):
    """Test that no update is found using minutes."""
    os.environ["INPUT_LAYERID"] = "52054"
    os.environ["INPUT_TIMEFRAME"] = "5"
    os.environ["INPUT_UNITS"] = "minutes"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::False
::set-output name=datasetTitle::None
::set-output name=revisionNumber::None
::set-output name=publishedTime::None
::set-output name=totalFeatures::None
::set-output name=adds::None
::set-output name=modifies::None
::set-output name=deletes::None
"""
    )


def test_raises_value_error_wrong_units():
    """Test that ValueError is raised when incorrect units provided."""
    with pytest.raises(ValueError):
        os.environ["INPUT_LAYERID"] = "52054"
        os.environ["INPUT_TIMEFRAME"] = "1"
        os.environ["INPUT_UNITS"] = "minute"
        main()


def test_update_found_raster(capsys):
    """Test that no update is found using minutes."""
    os.environ["INPUT_LAYERID"] = "104485"
    os.environ["INPUT_TIMEFRAME"] = "10000"
    os.environ["INPUT_UNITS"] = "days"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::True
::set-output name=datasetTitle::Chatham Islands 0.5m Satellite Imagery (2014-2019)
::set-output name=revisionNumber::4
::set-output name=publishedTime::Feb 20th 2020 at 11:32
::set-output name=totalFeatures::None
::set-output name=adds::None
::set-output name=modifies::None
::set-output name=deletes::None
"""
    )


def test_no_update_found_raster(capsys):
    """Test that no update is found using minutes."""
    os.environ["INPUT_LAYERID"] = "104485"
    os.environ["INPUT_TIMEFRAME"] = "5"
    os.environ["INPUT_UNITS"] = "minutes"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::False
::set-output name=datasetTitle::None
::set-output name=revisionNumber::None
::set-output name=publishedTime::None
::set-output name=totalFeatures::None
::set-output name=adds::None
::set-output name=modifies::None
::set-output name=deletes::None
"""
    )


def test_update_found_table(capsys):
    """Test that no update is found using minutes."""
    os.environ["INPUT_LAYERID"] = "51741"
    os.environ["INPUT_TIMEFRAME"] = "10000"
    os.environ["INPUT_UNITS"] = "days"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::True
::set-output name=datasetTitle::Landonline: Road Name Association (Deprecated)
::set-output name=revisionNumber::148
::set-output name=publishedTime::Jul 2nd 2017 at 01:24
::set-output name=totalFeatures::258,503
::set-output name=adds::26,865
::set-output name=modifies::0
::set-output name=deletes::26,823
"""
    )


def test_no_update_found_table(capsys):
    """Test that no update is found using minutes."""
    os.environ["INPUT_LAYERID"] = "51741"
    os.environ["INPUT_TIMEFRAME"] = "5"
    os.environ["INPUT_UNITS"] = "minutes"
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::False
::set-output name=datasetTitle::None
::set-output name=revisionNumber::None
::set-output name=publishedTime::None
::set-output name=totalFeatures::None
::set-output name=adds::None
::set-output name=modifies::None
::set-output name=deletes::None
"""
    )
