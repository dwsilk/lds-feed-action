# LDS Feed Action

[![Lint & Test Status](https://github.com/dwsilk/lds-feed-action/workflows/Lint%20&%20Test/badge.svg)](https://github.com/dwsilk/lds-feed-action/actions)
[![Integration Test Status](https://github.com/dwsilk/lds-feed-action/workflows/Integration%20Test/badge.svg)](https://github.com/dwsilk/lds-feed-action/actions)
[![Codecov Status](https://badgen.net/codecov/c/github/dwsilk/lds-feed-action?icon=codecov&labelColor=2e3a44&color=EC5772)](https://codecov.io/gh/dwsilk/lds-feed-action)
[![Conventional Commits](https://badgen.net/badge/Commits/conventional?labelColor=2e3a44&color=EC5772)](https://conventionalcommits.org)
[![Dependabot Status](https://badgen.net/dependabot/dwsilk/lds-feed-action?icon=dependabot&labelColor=2e3a44&color=blue)](https://dependabot.com)
[![License](https://badgen.net/badge/License/MIT?labelColor=2e3a44&color=blue)](https://github.com/dwsilk/lds-feed-action/blob/master/LICENSE)
[![Code Style](https://badgen.net/badge/Code%20Style/black?labelColor=2e3a44&color=000000)](https://black.readthedocs.io/en/stable/)
[![Doc Style](https://badgen.net/badge/Doc%20Style/numpy?labelColor=2e3a44&color=000000)](https://numpydoc.readthedocs.io/en/latest/format.html)

## Usage

This GitHub Action checks the history feed of a [LINZ Data Service](https://data.linz.govt.nz/) for updates within the specified timeframe, and if found, returns statistics about that update.

It is designed to be run on a cron schedule with the outputs utilised in other actions, for example creating an issue whenever a dataset is updated.

### Example workflow

```yaml
name: Building Outlines Update Check
on:
  schedule:
    # Run at 5am every Monday morning
    - cron: '0 5 * * mon'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check LDS history feed
        id: check-lds-history-feed
        uses: dwsilk/lds-feed-action@master
        with:
          layerid: 101290
          timeframe: 7
          units: days
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `layerid`  | The LINZ Data Service layer id    |
| `timeframe` _(optional)_  | Number of days, hours or minutes of history to check for dataset updates. Default: 10000.    |
| `units` _(optional)_  | Either `days`, `hours` or `minutes`. Default: days.    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `updateFound`  | If a dataset update was found, returns True    |
| `datasetTitle`  | The title of the dataset    |
| `revisionNumber`  | The unique identifier for the dataset update    |
| `publishedTime`  | A datetime for the time the dataset update was published on the LINZ Data Service    |
| `totalFeatures`  | The total number of features in the dataset after the update    |
| `adds`  | The number of features added by the update    |
| `modifies`  | The number of features modified by the update    |
| `deletes`  | The number of features deleted by the update    |

## Examples

### Using outputs

This example checks for updates to the `NZ Building Outlines` dataset within the last week, every Monday morning at 5am. The outputs of that check are shown in the GitHub Actions console.

```yaml
name: Building Outlines Update Check
on:
  schedule:
    # Run at 5am every Monday morning
    - cron: '0 5 * * mon'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check LDS history feed
        id: check-lds-history-feed
        uses: dwsilk/lds-feed-action@master
        with:
          layerid: 101290
          timeframe: 7
          units: days

      - name: Check outputs
        run: |
          echo "Update found: ${{ steps.check-lds-history-feed.outputs.updateFound }}"
          echo "Dataset title: ${{ steps.check-lds-history-feed.outputs.datasetTitle }}"
          echo "Revision number: ${{ steps.check-lds-history-feed.outputs.revisionNumber }}"
          echo "Published time: ${{ steps.check-lds-history-feed.outputs.publishedTime }}"
          echo "Total features: ${{ steps.check-lds-history-feed.outputs.totalFeatures }}"
          echo "Adds: ${{ steps.check-lds-history-feed.outputs.adds }}"
          echo "Modifies: ${{ steps.check-lds-history-feed.outputs.modifies }}"
          echo "Deletes: ${{ steps.check-lds-history-feed.outputs.deletes }}"
```

This example checks for updates to both the `NZ Building Outlines` and `NZ Building Outlines (All Sources)` datasets within the last day, every morning at 7am. The outputs of that check are shown in the GitHub Actions console.

A bot user account within Slack then posts a message if an update is found, using `pullreminders/slack-action`. A `SLACK_BOT_TOKEN` must be stored as a Secret on the repository with this workflow configured, as well as configuring the channel identifier shown as `CXXXXXXXX` below.

```
name: Building Outlines Update Check
on:
  schedule:
    # Daily at 7am
    - cron: '0 7 * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        layer_id: [101290, 101292]
    steps:
      - uses: actions/checkout@v1

      - name: Check LDS history feed
        id: check-lds-history-feed
        uses: dwsilk/lds-feed-action@master
        with:
          layerid: ${{ matrix.layer_id }}
          timeframe: 1
          units: days

      - name: Check outputs
        id: check-outputs
        run: |
          echo "Update found: ${{ steps.check-lds-history-feed.outputs.updateFound }}"
          echo "Dataset title: ${{ steps.check-lds-history-feed.outputs.datasetTitle }}"
          echo "Revision number: ${{ steps.check-lds-history-feed.outputs.revisionNumber }}"
          echo "Published time: ${{ steps.check-lds-history-feed.outputs.publishedTime }}"
          echo "Total features: ${{ steps.check-lds-history-feed.outputs.totalFeatures }}"
          echo "Adds: ${{ steps.check-lds-history-feed.outputs.adds }}"
          echo "Modifies: ${{ steps.check-lds-history-feed.outputs.modifies }}"
          echo "Deletes: ${{ steps.check-lds-history-feed.outputs.deletes }}"

      - name: Notify Slack
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
        uses: pullreminders/slack-action@master
        if: steps.check-lds-history-feed.outputs.updateFound == 'True'
        with:
          args: '{\"channel\":\"CXXXXXXXX\",\"text\":\"Hello\",\"blocks\":[{\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"*${{ steps.check-lds-history-feed.outputs.datasetTitle }}* · Layer ${{ matrix.layer_id }} · Revision ${{ steps.check-lds-history-feed.outputs.revisionNumber }}\"}, \"accessory\": {\"type\": \"button\", \"text\": {\"type\": \"plain_text\",\"text\": \"View Layer\"}, \"url\": \"https://data.linz.govt.nz/layer/${{ matrix.layer_id }}/?c=-40.87127%2C173.44655&e=0&lpw=650&l=${{ matrix.layer_id }}&al=m&mt=Streets&z=7&cv=0\"}}, {\"type\": \"section\",\"text\": {\"type\": \"mrkdwn\",\"text\": \":heavy_plus_sign: ${{ steps.check-lds-history-feed.outputs.adds }} Added\n:wastebasket: ${{ steps.check-lds-history-feed.outputs.deletes }} Deleted\n:construction: ${{ steps.check-lds-history-feed.outputs.modifies }} Modified\n:earth_asia: ${{ steps.check-lds-history-feed.outputs.totalFeatures }} Total Features\"}, \"accessory\": {\"type\": \"image\",\"image_url\": \"https://koordinates-tiles-c.global.ssl.fastly.net/services/tiles/v4/thumbnail/layer=${{ matrix.layer_id }},style=auto/150x150.png\", \"alt_text\": \"Dataset thumbnail\"}}, {\"type\": \"context\",\"elements\": [{\"type\": \"mrkdwn\", \"text\": \"Update published: ${{ steps.check-lds-history-feed.outputs.publishedTime }}\"}]}]}'
```

The Slack message generated by this configuration looks like this:

![LDS Feed Action Post to Slack](https://user-images.githubusercontent.com/8953184/75604822-b5d72880-5b41-11ea-85ff-440a6276a78e.png)
