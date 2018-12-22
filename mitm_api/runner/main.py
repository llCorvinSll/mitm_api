import os
import sys
import asyncio
import argparse
import signal
import typing


from mitmproxy.tools import cmdline
from mitmproxy import exceptions, master
from mitmproxy import options
from mitmproxy import optmanager
from mitmproxy import proxy
from mitmproxy.utils import debug, arg_check

from mitm_api.api_master.ApiMaster import ApiMaster
from mitm_api.runner.ExtendedConfig import ExtendedConfig

OPTIONS_FILE_NAME = "config.yaml"


def assert_utf8_env():
    spec = ""
    for i in ["LANG", "LC_CTYPE", "LC_ALL"]:
        spec += os.environ.get(i, "").lower()
    if "utf" not in spec:
        print(
            "Error: mitmproxy requires a UTF console environment.",
            file=sys.stderr
        )
        print(
            "Set your LANG environment variable to something like en_US.UTF-8",
            file=sys.stderr
        )
        sys.exit(1)


def process_options(parser, opts, args):
    if args.version:
        print(debug.dump_system_info())
        sys.exit(0)
    if args.quiet or args.options or args.commands:
        # also reduce log verbosity if --options or --commands is passed,
        # we don't want log messages from regular startup then.
        args.termlog_verbosity = 'error'
        args.flow_detail = 0
    if args.verbose:
        args.termlog_verbosity = 'debug'
        args.flow_detail = 2

    adict = {}
    for n in dir(args):
        if n in opts:
            adict[n] = getattr(args, n)
    opts.merge(adict)

    return ExtendedConfig(opts)


def run(
        master_cls: typing.Type[master.Master],
        make_parser: typing.Callable[[options.Options], argparse.ArgumentParser],
        arguments: typing.Sequence[str],
        extra: typing.Callable[[typing.Any], dict] = None
) -> master.Master:  # pragma: no cover
    """
        extra: Extra argument processing callable which returns a dict of
        options.
    """
    debug.register_info_dumpers()

    opts = options.Options()
    master = master_cls(opts)

    parser = make_parser(opts)

    # To make migration from 2.x to 3.0 bearable.
    if "-R" in sys.argv and sys.argv[sys.argv.index("-R") + 1].startswith("http"):
        print("-R is used for specifying replacements.\n"
              "To use mitmproxy in reverse mode please use --mode reverse:SPEC instead")

    try:
        args = parser.parse_args(arguments)
    except SystemExit:
        arg_check.check()
        sys.exit(1)
    try:
        opts.confdir = args.confdir
        optmanager.load_paths(
            opts,
            os.path.join(opts.confdir, OPTIONS_FILE_NAME),
        )
        pconf = process_options(parser, opts, args)
        server: typing.Any = None
        if pconf.options.server:
            try:
                server = proxy.server.ProxyServer(pconf)
            except exceptions.ServerException as v:
                print(str(v), file=sys.stderr)
                sys.exit(1)
        else:
            server = proxy.server.DummyServer(pconf)

        master.server = server
        if args.options:
            print(optmanager.dump_defaults(opts))
            sys.exit(0)
        if args.commands:
            master.commands.dump()
            sys.exit(0)
        opts.set(*args.setoptions, defer=True)
        if extra:
            opts.update(**extra(args))

        loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM'):
            try:
                loop.add_signal_handler(getattr(signal, signame), master.shutdown)
            except NotImplementedError:
                # Not supported on Windows
                pass

        # Make sure that we catch KeyboardInterrupts on Windows.
        # https://stackoverflow.com/a/36925722/934719
        if os.name == "nt":
            async def wakeup():
                while True:
                    await asyncio.sleep(0.2)
            asyncio.ensure_future(wakeup())

        master.run()
    except exceptions.OptionsError as e:
        print("%s: %s" % (sys.argv[0], e), file=sys.stderr)
        sys.exit(1)
    except (KeyboardInterrupt, RuntimeError):
        pass
    return master


def mitmapi(args=None) -> typing.Optional[int]:  # pragma: no cover
    run(ApiMaster, cmdline.mitmweb, args)
    return None
