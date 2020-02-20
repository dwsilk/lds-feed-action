# LDS Feed Action

[![Actions Status](https://github.com/dwsilk/lds-feed-action/workflows/Lint/badge.svg)](https://github.com/dwsilk/lds-feed-action/actions)
[![Actions Status](https://github.com/dwsilk/lds-feed-action/workflows/Integration%20Test/badge.svg)](https://github.com/dwsilk/lds-feed-action/actions)

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
        uses: dwsilk/lds-feed-action@test
        with:
          layerid: 101290
          frequency: 7
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `layerid`  | The LINZ Data Service layer id    |
| `frequency` _(optional)_  | Number of days of history to check for dataset updates. Default: 10000.    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `updateFound`  | If a dataset update was found, returns True    |
| `publishedTime`  | A datetime for the time the dataset update was published on the LINZ Data Service    |
| `totalFeatures`  | The total number of features in the dataset after the update    |
| `adds`  | The number of features added by the update    |
| `modifies`  | The number of features modified by the update    |
| `deletes`  | The number of features deleted by the update    |

## Examples

### Using outputs

Show people how to use your outputs in another action.

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
        uses: dwsilk/lds-feed-action@test
        with:
          layerid: 101290
          frequency: 7

      - name: Check outputs
        run: |
          echo Update found: ${{ steps.check-lds-history-feed.outputs.updateFound }}
          echo Published time: ${{ steps.check-lds-history-feed.outputs.publishedTime }}
          echo Total features: ${{ steps.check-lds-history-feed.outputs.totalFeatures }}
          echo Adds: ${{ steps.check-lds-history-feed.outputs.adds }}
          echo Modifies: ${{ steps.check-lds-history-feed.outputs.modifies }}
          echo Deletes: ${{ steps.check-lds-history-feed.outputs.deletes }}
```
