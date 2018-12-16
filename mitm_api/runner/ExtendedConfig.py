import os
import typing

from OpenSSL import crypto

from mitmproxy import exceptions
from mitmproxy import options as moptions
from mitmproxy import certs
from mitmproxy.net import server_spec
from mitmproxy.proxy import ProxyConfig
from mitmproxy.proxy.config import CONF_BASENAME

from mitm_api.runner.DynamicHostMatcher import DynamicHostMatcher


class ExtendedConfig(ProxyConfig):
    def configure(self, options: moptions.Options, updated: typing.Any) -> None:
        self.check_ignore = DynamicHostMatcher(options.ignore_hosts)
        self.check_tcp = DynamicHostMatcher(options.tcp_hosts)

        certstore_path = os.path.expanduser(options.confdir)
        if not os.path.exists(os.path.dirname(certstore_path)):
            raise exceptions.OptionsError(
                "Certificate Authority parent directory does not exist: %s" %
                os.path.dirname(certstore_path)
            )
        self.certstore = certs.CertStore.from_store(
            certstore_path,
            CONF_BASENAME
        )

        for c in options.certs:
            parts = c.split("=", 1)
            if len(parts) == 1:
                parts = ["*", parts[0]]

            cert = os.path.expanduser(parts[1])
            if not os.path.exists(cert):
                raise exceptions.OptionsError(
                    "Certificate file does not exist: %s" % cert
                )
            try:
                self.certstore.add_cert_file(parts[0], cert)
            except crypto.Error:
                raise exceptions.OptionsError(
                    "Invalid certificate format: %s" % cert
                )
        m = options.mode
        if m.startswith("upstream:") or m.startswith("reverse:"):
            _, spec = server_spec.parse_with_mode(options.mode)
            self.upstream_server = spec
