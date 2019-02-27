import requests
import subprocess
import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Starts a Gadgetron worker node')
    parser.add_argument('--relay', help="Address of the CloudBus relay")
    parser.add_argument('--port', type=int, help="Port on which to start the Gadgetron worker", default=9002)
    parser.add_argument('--poll_time', type=int,
                        help="Time interval (in seconds) betweens polls to Gadgetron and the relay",
                        default=10)

    args = parser.parse_args()

    port = args.port
    relay = args.relay


    def start_gadgetron():
        return subprocess.Popen(["gadgetron", "-p", str(port)])


    gadgetron = start_gadgetron()

    while True:
        if gadgetron.poll() is not None: gadgetron = start_gadgetron()
        requests.post("http://"+relay + '/cloudbus/add_worker', json={'port': str(port)})
        time.sleep(args.poll_time)
