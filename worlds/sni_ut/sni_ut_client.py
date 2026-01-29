import asyncio
import Utils
import sys
import logging
from Utils import async_start

def my_launch(*launch_args) -> None:
    from CommonClient import get_base_parser, server_loop, logger, gui_enabled
    from SNIClient import SNIContext, SNIClientCommandProcessor, snes_connect, run_game, game_watcher, _snes_connect
    tracker_loaded = False
    try:
        from worlds.tracker.TrackerClient import (TrackerGameContext as SuperContext,
                                                  TrackerCommandProcessor as SuperCommandProcessor,
                                                  UT_VERSION, updateTracker)
        tracker_loaded = True
    except ModuleNotFoundError:
        from CommonClient import CommonContext as SuperContext
        from CommonClient import ClientCommandProcessor as SuperCommandProcessor

    async def main():
        parser = get_base_parser()
        parser.add_argument('diff_file', default="", type=str, nargs="?",
                            help='Path to a Archipelago Binary Patch file')
        parser.add_argument('--snes', default='localhost:23074', help='Address of the SNI server.')
        parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
        args = parser.parse_args(launch_args)

        class MyClientCommandProcessor(SNIClientCommandProcessor, SuperCommandProcessor):
            pass

        class MyClientContext(SNIContext, SuperContext):
            command_processor = MyClientCommandProcessor
            tags = SNIContext.tags

            def __init__(self, snes_address: str, server_address: str, password: str) -> None:
                super().__init__(snes_address, server_address, password)
                self.tracker_enabled = tracker_loaded

            def on_package(self, cmd, args):
                super().on_package(cmd, args)
                if self.tracker_enabled:
                    SuperContext.on_package(self, cmd, args)

            def make_gui(self):
                ui = super().make_gui()
                if self.tracker_enabled:
                    ui.base_title += f" (with Tracker {UT_VERSION}) for AP version"
                return ui


        if args.diff_file:
            import Patch
            logging.info("Patch file was supplied. Creating sfc rom..")
            try:
                meta, romfile = Patch.create_rom_file(args.diff_file)
            except Exception as e:
                Utils.messagebox('Error', str(e), True)
                raise
            args.connect = meta["server"]
            logging.info(f"Wrote rom file to {romfile}")
            if args.diff_file.endswith(".apsoe"):
                import webbrowser
                async_start(run_game(romfile))
                await _snes_connect(MyClientContext(args.snes, args.connect, args.password), args.snes, False)
                webbrowser.open(f"http://www.evermizer.com/apclient/#server={meta['server']}")
                logging.info("Starting Evermizer Client in your Browser...")
                import time
                time.sleep(3)
                sys.exit()
            elif args.diff_file.endswith(".aplttp"):
                from worlds.alttp.Client import get_alttp_settings
                adjustedromfile, adjusted = get_alttp_settings(romfile)
                async_start(run_game(adjustedromfile if adjusted else romfile))
            else:
                async_start(run_game(romfile))


        ctx = MyClientContext(args.snes, args.connect, args.password)
        if ctx.server_task is None:
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.snes_connect_task = asyncio.create_task(snes_connect(ctx, ctx.snes_address), name="SNES Connect")
        watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

        await ctx.exit_event.wait()

        ctx.server_address = None
        ctx.snes_reconnect_address = None
        if ctx.snes_socket is not None and not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        await watcher_task
        await ctx.shutdown()

    Utils.init_logging("SNIUniversalTracker", exception_logger="Client")
    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
