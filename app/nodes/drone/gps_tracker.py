import _thread
import logging
import socket
import time
from copy import deepcopy
from dataclasses import dataclass, field
import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk.sdk as sdk
log = logging.getLogger(__file__)

def create_node(plugin_name=plugin_name(__file__), parent=None, port:int=5005):
    return GpsTracker(plugin_name=plugin_name, parent=parent, port=port)

@dataclass
class Input:
    tts: str = ""

@dataclass
class Output:
    lat:float=-11111
    lon:float=-11111
    acc:float=-11111
    speed:float = -1111
    heading:float = -1111
    course_acc: float = -1111
    gps_altitude:float = -1111
    barometer_altitude:float = -1111
    rtt: float = -1111
    packet_nbr:int = -1111
    connected: bool = False
    timestamp: bool = False
    tracker_ip4:str=""
    tracker_ip6:str=""
    local_ip4s:str=""
    local_ip6s:str=""
    port:int=-1111

class GpsTracker(Node):
    input: Input
    output: Output
    _next_output: Output
    def __init__(self, port:int, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)
        self.port=port
        self.server_thread = _thread.start_new_thread(self.receiver,())
        output.local_ip4s = self.get_local_ip4()
        output.local_ip6s = self.get_local_ip6()


    def run(self) -> None:
        self.output = self._next_output

    def receiver(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", self.port))
        self.log.info("listen on: {sock}")
        self.log.info(f"UDP server started on port: {str(self.port)}")
        while True:
            data, address = sock.recvfrom(1024)
            self._next_output = self.parse_message(data.decode())

            if data:
                data = data.decode().split(',')[0] + "," + self.input.tts
                sock.sendto(data.encode(), address)


    def get_local_ip4(self):
        ip4s = [x[4][0] for x in socket.getaddrinfo(socket.gethostname(), port=None, family=socket.AddressFamily.AF_INET)]
        return ip4s
    def get_local_ip6(self):
        ip6s = [x[4][0] for x in socket.getaddrinfo(socket.gethostname(), port=None, family=socket.AddressFamily.AF_INET6)]
        return ip6s

    def parse_message(self, data) -> Output:
        o = deepcopy(self.output)
        parameters = data.split(',')
        o.packet_nbr = parameters.pop(0)
        if o.packet_nbr <= self.output.packet_nbr or o.packet_nbr <= self._next_output.packet_nbr:
            return self.output
        o.lat = float(parameters.pop(0))
        o.lon = float(parameters.pop(0))
        o.speed = float(parameters.pop(0))
        o.heading = float(parameters.pop(0))
        o.acc = float(parameters.pop(0))
        o.course_acc = float(parameters.pop(0))
        o.gps_altitude = float(parameters.pop(0))
        o.timestamp = int(parameters.pop(0))
        o.rtt = int(parameters.pop(0))
        o.barometer_altitude = float(parameters.pop(0))
        return o

    def _start_simulate_tracker_from_file(self, filename):
        line_nbr=-1
        with open(filename) as fp:
            line = fp.readline()

            starttime = time.time()
            while line:
                line = fp.readline()
                line_nbr += 1
                if line_nbr % 10 != 0:
                    continue
                #log.info("LINE", line)
                columns = line.split(',')
                columns.pop(0) # Remove packet number
                line = ','.join(columns)
                # log.info("LINE", line)
                cls.sock_send = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
                cls.sock_send.settimeout(cls.TIMEOUT)
                sock_send.sendto(msg, (ip_address, cls.port))
                time.sleep(1.0 - ((time.time() - starttime) % 1.0))
    @classmethod
    def _send(cls, ip_address, message):
        cls.latest_sent_packet_nbr = cls.latest_sent_packet_nbr + 1
        msg_sent = str(cls.latest_sent_packet_nbr) + ',' + message
        msg = str.encode(str(cls.latest_sent_packet_nbr) + ',' + message)
        cls.timestamp_latest_send = time.time_ns()
        # log.info("send.sendto " + msg_sent + " ip:" + ip_address)
        UdpCommunicator.sock_send.sendto(msg, (ip_address, cls.port))
        return int(cls.latest_rtt)



if __name__ == "__main__":
    #NodeCore.run_from_main(__file__)
    node = create_node()
    print(node.output.local_ip4s)

