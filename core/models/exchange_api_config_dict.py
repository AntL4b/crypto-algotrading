from typing import TypedDict


class ExchangeApiConfigDict(TypedDict):
    rest_public_endpoint: str
    rest_private_endpoint: str
    ws_public_endpoint: str
    ws_private_endpoint: str
