# LDS Feed Action

[![Actions Status](https://github.com/dwsilk/lds-feed-action/workflows/Lint/badge.svg)](https://github.com/dwsilk/lds-feed-action/actions)
[![Actions Status](https://github.com/dwsilk/lds-feed-action/workflows/Integration%20Test/badge.svg)](https://github.com/dwsilk/lds-feed-action/actions)

## Usage

Describe how to use your action here.

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
    - uses: actions/checkout@master
    - name: Run action

      uses: dwsilk/lds-feed-action@master

      # Configure the LINZ Data Service layer id that you want to track
      with:
        layer-id: 101290
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `layer-id`  | LINZ Data Service layer id    |
| `anotherInput` _(optional)_  | An example optional input    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myOutput`  | An example output (returns 'Hello world')    |

## Examples

> NOTE: People ❤️ cut and paste examples. Be generous with them!

### Using the optional input

This is how to use the optional input.

```yaml
with:
  layer-id: 101290
  anotherInput: optional
```

### Using outputs

Show people how to use your outputs in another action.

```yaml
steps:
- uses: actions/checkout@master
- name: Run action
  id: ldsfeedaction

  # Put your action name here
  uses: dwsilk/lds-feed-action@master

  # Put an example of your mandatory arguments here
  with:
    layer-id: 101290

# Put an example of using your outputs here
- name: Check outputs
    run: |
    echo "Outputs - ${{ steps.ldsfeedaction.outputs.myOutput }}"
```
