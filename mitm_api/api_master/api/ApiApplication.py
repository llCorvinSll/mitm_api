import tornado

from tornado.routing import PathMatches

from mitm_api.api_master.api.RequestHandler import RequestHandler


class MatcherHandler(RequestHandler):
    """
    добавляет хост в отслеживаемые,
    будет работать только для https
    http трекается всегда

    добавление
    curl -X POST http://localhost:8082/api/v1/api.ivi.ru/track
    """
    def post(self, host):
        print(host)
        passthrough_addon = self.master.addons.get("passthroughaddon")
        passthrough_addon.track_host(host)

    """
    удаление
    
    после этого хост перестает трекаться
    curl -X DELETE http://localhost:8082/api/v1/api.ivi.ru/track
    """
    def delete(self, host):
        print(host)
        passthrough_addon = self.master.addons.get("passthroughaddon")
        passthrough_addon.untrack_host(host)


class MockCreateHandler(RequestHandler):
    """
    добавляет мок для текущего контекста
    """
    def post(self, context):
        print("create proxy for", context)
        mock_addon = self.master.addons.get("mockaddon")
        mock_addon.add_mock(context, tornado.escape.json_decode(self.request.body))


class RedirectHandler(RequestHandler):
    """
    перенаправляет запрос с одного хоста на другой
    прозрачно для клиента
    """

    def post(self, context):
        print("make redirect for ", context)
        print(tornado.escape.json_decode(self.request.body))


class BaseApiApplication(tornado.web.Application):
    def __init__(self, master, debug):
        self.master = master
        super().__init__(
            default_host="dns-rebind-protection",
            debug=debug,
            autoreload=False,
        )


HOST_MATHER = r'^(localhost|[0-9.:\[\]]+)$'


class ApiRouter(BaseApiApplication):
    def __init__(self, master, debug):
        super().__init__(master, debug)
        self.add_handlers(HOST_MATHER, [
            (r"/api/v1/mock/(?P<context>[\.0-9a-zA-Z\-]+)", MockCreateHandler),
            (r"/api/v1/(?P<host>[\.0-9a-z\-]+)/track", MatcherHandler),
            (r"/api/v1/(?P<context>[\.0-9a-zA-Z\-]+)/redirect", RedirectHandler),
        ])


class ApiApplication(BaseApiApplication):
    def __init__(self, master, debug):
        super().__init__(master, debug)

        self.add_handlers(
            HOST_MATHER,
            [
                (PathMatches("/api/v1.*"), ApiRouter(master, debug)),
            ]
        )
