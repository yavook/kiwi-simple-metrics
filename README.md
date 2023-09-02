# kiwi-simple-metrics

[![Build Status](https://github.drone.yavook.de/api/badges/yavook/kiwi-simple-metrics/status.svg)](https://github.drone.yavook.de/yavook/kiwi-simple-metrics)

> `kiwi` - simple, consistent, powerful

A lightweight monitoring solution for [`kiwi-scp`](https://github.com/yavook/kiwi-scp), created with [`uptime-kuma`](https://github.com/louislam/uptime-kuma) in mind. Also [on Docker Hub](https://hub.docker.com/r/yavook/kiwi-simple-metrics).

## Quick start

The minimal config to add to one of your `docker-compose.yml` is this:

```yaml
metrics:
  image: yavook/kiwi-simple-metrics:0.1
```

- admittedly not useful, but it *does* run monitoring
- every 600 seconds (10 minutes), metrics are evaluated
- measures cpu, memory and swap, and disk usage at "/"
- does not log to stdout
- does not trigger any webhooks

Every aspect of kiwi-simple-metrics can be tweaked by environment variables, so this is a more reasonable configuration example:

```yaml
metrics:
  image: yavook/kiwi-simple-metrics:0.1
  environment:
    METRICS__LOG__ENABLED: "True"
    METRICS__WEBHOOK__URL: "https://my.webhook.host/success?report={result}"
    METRICS__WEBHOOK__FAIL: "https://my.webhook.host/failure?report={result}"
```

- same metrics as above
- logs reports to stdout
- triggers webhooks (`{result}` is the placeholder for the result string)

## Configuration

These are the environment variables you most likely need:

- `METRICS__INTERVAL`: Time in seconds between metrics evaluation (default: `600`, i.e. 10 minutes)
- `METRICS__LOG__ENABLED`: If truthy, logs reports to stdout (default: `False`)
- `METRICS__[M]__ENABLED`, `METRICS__[M]__THRESHOLD` (with `[M]` from `CPU`, `MEMORY`, `DISK`): Enable or disable each metric, and set its failure threshold
- `METRICS__MEMORY__SWAP`: How swap space is handled in the "memory" report (default: `include`)
- `METRICS__DISK__PATHS`: At which paths the disk usage is measured (default: `["/"]`)
- `METRICS__EXTERNAL__ENABLED`, `METRICS__EXTERNAL__EXECUTABLES`: Setup for `external values`, as further defined in [`metrics/external.py`](./kiwi_simple_metrics/metrics/external.py) (default: `False`, `[]`)
- `METRICS__WEBHOOK__URL`, `METRICS__WEBHOOK__FAIL`: Which webhooks to push the reports to (default: `None`, `None`)

All settings can be found in the `SETTINGS` variable defined by module [`kiwi_simple_metrics.settings` in `settings/__init__.py`](./kiwi_simple_metrics/settings/__init__.py). For default values, refer to the respective python files.

Example: The above `METRICS__LOG__ENABLED` refers to `SETTINGS.log.enabled`, defined by model [`LogSettings` in `settings/misc.py`](./kiwi_simple_metrics/settings/misc.py).
