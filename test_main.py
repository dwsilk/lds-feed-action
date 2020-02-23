"""Tests"""

from main import main


def test_main_output(capsys):
    """Test the output of the main function."""
    main()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """::set-output name=updateFound::True
::set-output name=publishedTime::2017-07-01T13:47:57+00:00
::set-output name=totalFeatures::1993687
::set-output name=adds::43445
::set-output name=modifies::84108
::set-output name=deletes::1
"""
    )
