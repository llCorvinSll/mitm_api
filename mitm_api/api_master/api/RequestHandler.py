import tornado
import json

from mitmproxy import version
from mitmproxy import flow


class APIError(tornado.web.HTTPError):
    pass


class RequestHandler(tornado.web.RequestHandler):
    def write(self, chunk):
        # Writing arrays on the top level is ok nowadays.
        # http://flask.pocoo.org/docs/0.11/security/#json-security
        if isinstance(chunk, list):
            chunk = tornado.escape.json_encode(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(RequestHandler, self).write(chunk)

    def set_default_headers(self):
        super().set_default_headers()
        self.set_header("Server", version.MITMPROXY)
        self.set_header("X-Frame-Options", "DENY")
        self.add_header("X-XSS-Protection", "1; mode=block")
        self.add_header("X-Content-Type-Options", "nosniff")
        self.add_header(
            "Content-Security-Policy",
            "default-src 'self'; "
            "connect-src 'self' ws:; "
            "style-src   'self' 'unsafe-inline'"
        )

    @property
    def json(self):
        if not self.request.headers.get("Content-Type", "").startswith("application/json"):
            raise APIError(400, "Invalid Content-Type, expected application/json.")
        try:
            return json.loads(self.request.body.decode())
        except Exception as e:
            raise APIError(400, "Malformed JSON: {}".format(str(e)))

    @property
    def filecontents(self):
        """
        Accept either a multipart/form file upload or just take the plain request body.

        """
        if self.request.files:
            return next(iter(self.request.files.values()))[0].body
        else:
            return self.request.body

    @property
    def view(self) -> "mitmproxy.addons.view.View":
        return self.application.master.view

    @property
    def master(self) -> "mitmproxy.tools.web.master.WebMaster":
        return self.application.master

    @property
    def flow(self) -> flow.Flow:
        flow_id = str(self.path_kwargs["flow_id"])
        # FIXME: Add a facility to addon.view to safely access the store
        flow = self.view.get_by_id(flow_id)
        if flow:
            return flow
        else:
            raise APIError(404, "Flow not found.")

    def write_error(self, status_code: int, **kwargs):
        if "exc_info" in kwargs and isinstance(kwargs["exc_info"][1], APIError):
            self.finish(kwargs["exc_info"][1].log_message)
        else:
            super().write_error(status_code, **kwargs)

