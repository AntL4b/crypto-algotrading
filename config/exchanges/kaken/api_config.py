from core.models.exchange_api_config_dict import ExchangeApiConfigDict

api_config: ExchangeApiConfigDict = {
    "rest_public_endpoint": "https://api.kraken.com/0/public/",
    "rest_private_endpoint": "https://api.kraken.com/0/private/",
    "ws_public_endpoint": "wss://ws.kraken.com/",
    "ws_private_endpoint": "wss://ws-auth.kraken.com/",
}
