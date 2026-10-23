import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import requests


class BrokerAdapter:
    def __init__(self, config):
        self.config = config
        self.base_url = self.get_base_url()
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get_base_url(self):
        raise NotImplementedError

    def _request(self, method, path, params=None, json_body=None, auth=False):
        url = f"{self.base_url}{path}"
        request_params = dict(params or {})
        if auth:
            if not self.config.api_key or not self.config.api_secret:
                raise ValueError("Missing API credentials for authenticated broker request.")
            request_params["timestamp"] = int(time.time() * 1000)
            request_params["recvWindow"] = 5000
            query = urlencode(request_params)
            signature = hmac.new(
                self.config.api_secret.encode("utf-8"),
                query.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            request_params["signature"] = signature
            self.session.headers.update({"X-MBX-APIKEY": self.config.api_key})
            url = f"{url}?{query}&signature={signature}"

        response = self.session.request(method, url, params=None, json=json_body, timeout=self.config.order_timeout_seconds)
        response.raise_for_status()
        data = response.json()
        if "code" in data and data["code"] != 200:
            raise RuntimeError(f"Broker error: {data}")
        return data

    def get_account_balance(self):
        raise NotImplementedError

    def get_prices(self, symbol):
        raise NotImplementedError

    def place_market_order(self, symbol, side, quantity):
        raise NotImplementedError

    def get_open_orders(self, symbol=None):
        raise NotImplementedError

    def cancel_order(self, symbol, order_id):
        raise NotImplementedError


class BinanceBroker(BrokerAdapter):
    def get_base_url(self):
        if self.config.broker_testnet:
            return "https://testnet.binancefuture.com"
        return "https://fapi.binance.com"

    def _signed_request(self, method, path, params=None, json_body=None):
        return self._request(method, path, params=params, json_body=json_body, auth=True)

    def get_account_balance(self):
        return self._signed_request("GET", "/fapi/v1/account")

    def get_prices(self, symbol):
        return self._request("GET", "/fapi/v1/ticker/price", params={"symbol": symbol.upper()})

    def place_market_order(self, symbol, side, quantity):
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        payload = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "MARKET",
            "quantity": float(quantity),
        }
        return self._signed_request("POST", "/fapi/v1/order", params=payload)

    def get_open_orders(self, symbol=None):
        params = {} if symbol is None else {"symbol": symbol.upper()}
        return self._signed_request("GET", "/fapi/v1/openOrders", params=params)

    def cancel_order(self, symbol, order_id):
        params = {"symbol": symbol.upper(), "orderId": order_id}
        return self._signed_request("DELETE", "/fapi/v1/order", params=params)


def get_broker(config):
    if config.broker_name.lower() == "binance":
        return BinanceBroker(config)
    raise ValueError(f"Unsupported broker: {config.broker_name}")
