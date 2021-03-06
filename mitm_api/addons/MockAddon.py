from mitmproxy import http
from mitmproxy import ctx
import re

from mitm_api.addons.mock_storage.MockContext import MockContext


class MockAddon:
    def __init__(self):
        self.sessions = {}

    def request(self, flow: http.HTTPFlow):
        """
            The full HTTP request has been read.
        """
        session = extract_context(flow)
        context = self._get_context(session)
        original_host = flow.request.pretty_host

        if context:
            self._handle_hidden_redirect(context, flow, original_host)

    @staticmethod
    def _handle_hidden_redirect(context, flow, original_host):
        """
        если указано что какой-то хост нужно тихо перевести на другой хост
        можно просто поменять параметры в флоу
        """
        redirect_host = context.get_redirect(original_host)

        if redirect_host:
            ctx.log("[spoofing][{}] redirect {} to {}".format(context.key, original_host, redirect_host))
            flow.request.host = redirect_host
            flow.request.port = 80
            flow.request.scheme = 'http'
            flow.request.headers["Host"] = redirect_host

    def response(self, flow: http.HTTPFlow):
        """
            The full HTTP response has been read.
        """
        session = extract_context(flow)

        if session and session in self.sessions:
            mock_storage = self.sessions[session]
            mock_storage.get_mock(flow)

    def error(self, flow: http.HTTPFlow):
        """
            An HTTP error has occurred, e.g. invalid server responses, or
            interrupted connections. This is distinct from a valid server HTTP
            error response, which is simply a response with an HTTP error code.
        """
        pass

    def add_mock(self, session, mock_config):
        self._ensure_context(session)

        ctx.log("[mocking][{}] add mock".format(session))
        self.sessions[session].add_mock(mock_config)

    def clear_mocks(self, session):
        self._ensure_context(session)

        ctx.log("[mocking][{}] clear all mocks".format(session))
        self.sessions[session].clear_mocks()

    def add_redirect(self, session, from_url, to_url):
        ctx.log("[spoofing][{}] add_redirect ({} -> {})".format(session, from_url, to_url))
        self._ensure_context(session)

        self.sessions[session].add_redirect(from_url, to_url)

    def _ensure_context(self, session):
        if session and session not in self.sessions:
            self.sessions[session] = MockContext(session)

    def _get_context(self, session):
        if session and session in self.sessions:
            return self.sessions[session]


def extract_context(flow: http.HTTPFlow):
    if "Referer" not in flow.request.headers:
        return None

    referer = flow.request.headers["Referer"]

    is_context = re.search(r"/key-[\w-]*/", referer)

    if is_context:
        return is_context.group().replace("key-", "").replace("/", "")
