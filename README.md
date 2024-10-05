# MQTT to BigQuery

MQTT subscriber message streaming load into BigQuery.

## Prerequisites

### Docker

### Python

### Just

## How to use

### Step 1

Download this repositories to your localhost:

```sh
$ git clone https://github.com/mslavov/mqtt-to-bigquery.git
$ cd mqtt-to-bigquery
```

### Step 2

Change your parameter in `mqtt.conf`:

```sh
[mqtt_broker]
ip=[YOUR BROKER IP]
port=[YOUR BROKER PORT]
timeout=60

[gcp]
table_name = [YOUR GCP PROJECT ID].[YOUR BIGQUERY DATASET ID].[YOUR BIGQUERY TABLE ID]
```

### Step 3

Build your docker image:

```sh
$ just build
```

### Step 4

Run your docker image:

```sh
$ just docker_run
```

Or run locally without docker:

```sh
$ just run
```
