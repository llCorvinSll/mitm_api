from mitmproxy import ctx
import typing


class PassthroughAddon:
    def load(self, loader):
        loader.add_option(
            name="notkube",
            typespec=typing.Optional[str],
            default='plumbus',
            help="Add a header to responses",
        )

    def request(self, flow):
        host_name = flow.request.host
        if host_name == 'api.ivi.ru':
            flow.request.host = f'api.{ctx.options.notkube}.notkube.dev.ivi.ru'
