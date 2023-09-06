### Telegram bot for control relay remote

## Run

* Variant 1: docker run
    ```shell
    docker run  --detach \
                --restart always \
                --network web \
                --env BOT_TOKEN='BOT_TOKEN_FROM_BOT_FATHER' \
                --env RELAY_URL='http://some_ip_or_domain:port' \
                --name relay_tgbot \
                ghcr.io/smartthinksdiy/esp8266-relay-tgbot:latest
    ```

* Variant 2: docker compose
  * Move `docker-compose.yaml` to target machine
  * create empty file with name `.env` in same folder
  * Paste this text with you credits in `.env` :
    ```text
    BOT_TOKEN=BOT_TOKEN_FROM_BOT_FATHER
    RELAY_URL=http://some_ip_or_domain:port
    ```
  * Run command in folder with `docker-compose.yaml` and `.env`:
    ```bash
    docker compose up -d
    ```

## Set commands via [BotFather](https://t.me/BotFather)
```text
switch - Change state
get_state - Get current state
turn_on - Turn lamp on
turn_off - Turn lamp off
uptime - ESP uptime
help - Instruction
```