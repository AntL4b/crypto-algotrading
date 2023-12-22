class CryptoAlgotradingException(Exception):
    """Generic exception for crypto_algotrading"""

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return "/!\\ CRYPTO ALGOTRADING EXCEPTION: " + self.message
