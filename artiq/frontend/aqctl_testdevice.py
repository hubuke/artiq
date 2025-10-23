#!/usr/bin/env python3
from sipyco.pc_rpc import simple_server_loop
from artiq.devices.testdevice.driver import *

def main():
    simple_server_loop({"hello": Hello()}, "::1", 3249)

if __name__ == "__main__":
    main()