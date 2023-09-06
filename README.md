### Telegram bot for control relay remote

## Setup

```shell
docker run  --detach \
            --restart always \
            --network web \
            --env BOT_TOKEN='BOT_TOKEN_FROM_BOT_FATHER' \
            --env RELAY_URL='http://some_ip_or_domain:port' \
            --name relay_tgbot \
            ghcr.io/smartthinksdiy/esp8266-relay-tgbot:latest
```

## Set commands via [BotFather](https://t.me/BotFather)
```text
switch - Change state
get_state - Get current state
turn_on - Turn lamp on
turn_off - Turn lamp off
uptime - ESP uptime
```