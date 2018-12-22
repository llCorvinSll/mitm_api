from mitmproxy import command
from mitmproxy import ctx


class PassthroughAddon:

    @command.command("passthroughaddon.trackhost")
    def track_host(self, host):
        ctx.log("add host to track %s" % host)
        cfg = ctx.master.server.config

        cfg.check_ignore.add(host)
