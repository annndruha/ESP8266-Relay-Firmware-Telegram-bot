### Telegram bot for control relay remote

## Run

* Docker compose
  * Clone this repo to target machine 
  * create inside cloned repo empty file with name `.env` in same folder
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