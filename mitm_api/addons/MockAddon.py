from mitmproxy import command, http
from mitmproxy import ctx
import re

from mitm_api.addons.mock_storage.MockStorage import MockContext


class MockAddon:
    def __init__(self):
        self.sessions = {}

    def request(self, flow: http.HTTPFlow):
        """
            The full HTTP request has been read.
        """
        pass

    def response(self, flow: http.HTTPFlow):
        """
            The full HTTP response has been read.
        """
        session = extract_context(flow)

        if session and session in self.sessions:
            mock_storage = self.sessions[session]
            mock_storage.get_mock()

    def add_mock(self, session, mock_config):
        print(session)

        if session not in self.sessions:
            self.sessions[session] = MockContext(session)

        self.sessions[session].add_mock(mock_config)


def extract_context(flow: http.HTTPFlow):
    referer = flow.request.headers["Referer"]

    is_context = re.search(r"/key-[\w-]*/", referer)

    if is_context:
        return is_context.group().replace("key-", "").replace("/", "")
