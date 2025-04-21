from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
import os
import hashlib

# BLS curve order for BLS12-381 (used for generating private keys)
BLS12_381_ORDER = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001

class CollabFedTopo(Topo):
    def build(self, latency='50ms'):
        csp_nodes = []
        for i in range(32):
            csp = self.addHost(f'csp{i}', cls=Host)
            csp_nodes.append(csp)
        for i in range(31):
            self.addLink(csp_nodes[i], csp_nodes[i+1], cls=TCLink, delay=latency)

def setup_network(latency='50ms'):
    topo = CollabFedTopo(latency=latency)
    
    # Fix: Disable controller requirement
    net = Mininet(topo=topo, link=TCLink, controller=None)
    net.start()
    
    for i in range(32):
        csp = net.get(f'csp{i}')
        csp.cmd(f'docker run -d --name collabfed_csp{i} --network=host -v /home/kalp-77/Desktop/bct/config:/config collabfed_image')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    latencies = ['50ms', '100ms', '200ms', '400ms']
    for lat in latencies:
        print(f"Starting simulation with latency {lat}")
        setup_network(latency=lat)

        # BLS private key simulation (optional here, but useful in consumer simulation)
        num_consumers = 4  # or any other number you're using
        private_keys = [
            int.from_bytes(hashlib.sha256(str(i).encode()).digest(), 'big') % BLS12_381_ORDER
            for i in range(num_consumers)
        ]
        print("Sample BLS private keys:", private_keys)

