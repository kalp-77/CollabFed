from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
import os

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
    net = Mininet(topo=topo, link=TCLink)
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
