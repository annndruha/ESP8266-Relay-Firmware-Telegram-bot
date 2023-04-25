### Telegram bot for control relay remote

TBD;

```shell
docker run  --detach \
            --restart always \
            --network web \
            --env BOT_TOKEN='BOT_TOKEN_FROM_BOT_FATHER' \
            --env RELAY_URL='http://some_ip_or_domain:port' \
            --name relay_tgbot \
            ghcr.io/annndruha/relay-tgbot:latest
```