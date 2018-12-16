from mitmproxy import command


class PassthroughAddon:

    @command.command("passthroughaddon.trackhost")
    def track_host(self, host):
        print("host: {}", host)
