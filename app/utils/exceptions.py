class HTTPClientError(Exception):
    pass


class HTTPTimeoutError(HTTPClientError):
    pass


class HTTPConnectionError(HTTPClientError):
    pass


class HTTPResponseError(HTTPClientError):
    pass


class HTTPRetryExhaustedError(HTTPClientError):
    pass