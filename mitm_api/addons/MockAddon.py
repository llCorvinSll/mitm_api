from mitmproxy import command, http
from mitmproxy import ctx


class MockAddon:
    def request(self, flow: http.HTTPFlow):
        """
            The full HTTP request has been read.
        """
        print("request")
        print(flow.request)

    def response(self, flow: http.HTTPFlow):
        """
            The full HTTP response has been read.
        """
        print("response")
        print(flow.response)
