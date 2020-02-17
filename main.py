"""This is the module."""

import os


def main():
    """This is the main function."""
    layer_id = os.environ["INPUT_LAYERID"]

    my_output = f"Hello {layer_id}"

    print(f"::set-output name=myOutput::{my_output}")


if __name__ == "__main__":
    main()
