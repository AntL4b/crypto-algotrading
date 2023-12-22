import base64
import hashlib
import hmac
import logging
import threading
import time
import math
from typing import Optional, Any

import requests

from config.exchanges.kaken.private.key_config import key_config
from core.exceptions.rest_api_exception import RestApiException
from core.exchange_api.exchange_rest_api import ExchangeRestApi
from core.models.stock_data_dict import StockDataDict

REST_ENDPOINT = "https://futures.kraken.com"

TIME_FRAME_MAPPING = {
    15: "1m",
    60: "1m",
    300: "5m",
    900: "15m",
    3600: "1h",
    14400: "4h",
    86400: "1d",
}


class KrakenRestApi(ExchangeRestApi):
    _LOCK: threading.Lock = threading.Lock()

    def __init__(self):
        super(KrakenRestApi, self).__init__()
        self._pub_key = key_config['public_key']
        self._secret_key = key_config['private_key']
        self._session: requests.Session = requests.Session()
        self._session.headers.update({"User-Agent": "antlab-crypto-algotrading"})

    def get_ohlcv(self, market: str, time_frame: int, start_time: int = None) -> [StockDataDict]:
        params: dict = {}

        if start_time is not None:
            params["from"] = start_time

        response = self._request(
            method="GET",
            uri=f"/api/charts/v1/trade/{market}/{TIME_FRAME_MAPPING[time_frame]}",
            query_params=params,
            auth=False,
        )

        return [self._format_ohlcv_raw_data(c, time_frame) for c in response["candles"]]

    def _request(self, method: str, uri: str, post_params: Optional[dict] = None, query_params: Optional[dict] = None,
                 *, auth: bool = True) -> Any:

        with KrakenRestApi._LOCK:
            method: str = method.upper()
            post_string: str = ""
            listed_params: list[str]

            if post_params is not None:
                listed_params = [f"{key}={post_params[key]}" for key in sorted(post_params)]
                post_string = "&".join(listed_params)

            query_string: str = ""
            if query_params is not None:
                listed_params = [f"{key}={query_params[key]}" for key in sorted(query_params)]
                query_string = "&".join(listed_params).replace(" ", "%20")

            headers: dict = {}
            if auth:
                if not self._pub_key or not self._secret_key:
                    raise RestApiException("Missing credentials")
                nonce: str = str(int(time.time() * 1000))
                headers.update(
                    {
                        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                        "Nonce": nonce,
                        "APIKey": self._pub_key,
                        "Authent": self._get_kraken_futures_signature(
                            uri,
                            query_string + post_string,
                            nonce,
                        ),
                    },
                )

            response = None

            if method in ["GET", "DELETE"]:
                response = self._session.request(
                    method=method,
                    url=f"{REST_ENDPOINT}{uri}"
                    if not query_string
                    else f"{REST_ENDPOINT}{uri}?{query_string}",
                    headers=headers,
                )

            elif method == "PUT":
                response = self._session.request(
                    method=method,
                    url=f"{REST_ENDPOINT}{uri}",
                    params=str.encode(post_string),
                    headers=headers,
                )
            else:
                response = self._session.request(
                    method=method,
                    url=f"{REST_ENDPOINT}{uri}?{post_string}",
                    data=str.encode(post_string),
                    headers=headers,
                )

            if response is not None and response.status_code in ["200", 200]:
                try:
                    return response.json()
                except ValueError as exc:
                    raise ValueError(response.content) from exc
            elif response is not None:
                raise RestApiException(response.text)
            else:
                raise RestApiException("None response received")

    def _get_kraken_futures_signature(self, endpoint: str, data: str, nonce: str) -> str:
        if endpoint.startswith("/derivatives"):
            endpoint = endpoint[len("/derivatives"):]

        sha256_hash = hashlib.sha256()
        sha256_hash.update((data + nonce + endpoint).encode("utf8"))
        return base64.b64encode(
            hmac.new(
                base64.b64decode(self._secret_key),
                sha256_hash.digest(),
                hashlib.sha512,
            ).digest(),
        ).decode()

    def _format_ohlcv_raw_data(self, ohlcv_raw_data: dict, time_step: int) -> Optional[StockDataDict]:
        """
        Format OHLCV raw data

        :param ohlcv_raw_data: The raw data
        :param time_step: The time between each record
        :return: The formatted data list
        """
        if all(required_field in ohlcv_raw_data for required_field in
               ["time", "open", "high", "low", "close", "volume"]):
            return {
                "id": int(math.floor(ohlcv_raw_data["time"] / 1000) / time_step),
                "time": math.floor(ohlcv_raw_data["time"] / 1000),
                "open_price": float(ohlcv_raw_data["open"]),
                "high_price": float(ohlcv_raw_data["high"]),
                "low_price": float(ohlcv_raw_data["low"]),
                "close_price": float(ohlcv_raw_data["close"]),
                "volume": float(ohlcv_raw_data["volume"]),
            }
        else:
            logging.warning("Data should be composed of 6 fields: <time>, <open>, <high>, <low>, <close>, <volume>")

        return None
