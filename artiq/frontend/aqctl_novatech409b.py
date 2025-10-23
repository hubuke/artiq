#!/usr/bin/env python3

# Written by Joe Britton, 2015

import argparse
import logging
import sys
import os
import asyncio

from artiq.devices.novatech409b.driver import Novatech409B
from sipyco.pc_rpc import simple_server_loop
from sipyco.tools import SimpleSSLConfig
from sipyco import common_args


logger = logging.getLogger(__name__)


def get_argparser():
    parser = argparse.ArgumentParser(
        description="ARTIQ controller for the Novatech 409B 4-channel DDS box")
    common_args.simple_network_args(parser, 3254, ssl=True)
    parser.add_argument(
        "-d", "--device", default=None,
        help="serial port.")
    parser.add_argument(
        "--simulation", action="store_true",
        help="Put the driver in simulation mode, even if --device is used.")
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)
    ssl_config = SimpleSSLConfig(*args.ssl) if args.ssl else None

    if os.name == "nt":
        asyncio.set_event_loop(asyncio.ProactorEventLoop())

    if not args.simulation and args.device is None:
        print("You need to specify either --simulation or -d/--device "
              "argument. Use --help for more information.")
        sys.exit(1)

    dev = Novatech409B(args.device if not args.simulation else None)
    asyncio.get_event_loop().run_until_complete(dev.setup())
    try:
        simple_server_loop(
            {"novatech409b": dev}, common_args.bind_address_from_args(args), args.port,
            ssl_config=ssl_config)
    finally:
        dev.close()

if __name__ == "__main__":
    main()
