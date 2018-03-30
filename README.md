### TODO

- Cleanup comments, etc
- Optimize generally and generally document and cleanup metrics_get.py 
- Error handling for when the router reboots (sometimes router will repsond but not with the right html response, unhandled exception when selecing elements)
- Setup logger
- Implement signal handler for systemd unit
- Write systemd unit to manage the docker container 
- Refactor into proper modules and `main()`
- Refactor the configuration a bit
- Add an outputs module that accepts output plugins and make telegraf_client.Telegraf an output plugin
- Repo should actually be named nighthawk-r7000-metrics, or some such
- Make a nice README.md

### Config

```
export METRICS_USER="admin"
export METRICS_PASSWORD="<password>"
export METRICS_URL="http://<ip_of_router>/RST_stattbl.htm"
```

### Building

`docker build -t nighthawk-r7000-metrics .`

### Running

`docker run -d --name nighthawk-r7000-metrics -eMETRICS_USER=$METRICS_USER -eMETRICS_PASSWORD=$METRICS_PASSWORD -eMETRICS_URL=$METRICS_URL nighthawk-r7000-metrics`
