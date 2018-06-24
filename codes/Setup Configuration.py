from pyroute2 import netns
from pyroute2 import IPDB
from pyroute2 import NetNS

def createNameSpace() :
    print("Creating network namespace....")
    #Create network namespace named 'blue'
    netns.create('blue')
    #Create network namespace named 'red'
    netns.create('red')
    #Display all namespaces
    print("Network Namespaces created: {}".format(netns.listnetns()))

def createAndMoveVeth():
    print("Creating Virtual Ethernet....... ")
    ip = IPDB()
    # create 2 veth devices vnet1@vnet2 and vnet3@vnet4
    ip.create(ifname='vnet1', kind='veth', peer='vnet2').commit()
    ip.create(ifname='vnet3', kind='veth', peer='vnet4').commit()
    # move peer to netns
    with ip.interfaces.vnet2 as veth:
        veth.net_ns_fd = 'blue'
    with ip.interfaces.vnet4 as veth:
        veth.net_ns_fd = 'red'
    # release before exit
    ip.release()
    print("veth created and connected to corresponding namespace")

def createBridgeWithPorts():
    # creating bridge and assigning port vnet1 and vnet3 to it
    with IPDB() as ip:
        with ip.create(kind='bridge', ifname="br-test") as i:
            i.add_port('vnet1')
            i.add_port('vnet3')

def bringUpDevices():
    # Bringing UP devices and assigning IP (namespace blue and red)
    ipdb = IPDB(nl=NetNS('blue'))
    with ipdb.interfaces['vnet2'] as vnet:
        vnet.up()
        vnet.add_ip('10.1.1.1/24')
    ipdb.release()

    ipdb = IPDB(nl=NetNS('red'))
    with ipdb.interfaces['vnet4'] as vnet:
        vnet.up()
        vnet.add_ip('10.1.1.2/24')
    ipdb.release()

    # Bringing UP devices (default namespace)
    ipdb = IPDB()
    with ipdb.interfaces['vnet1'] as vnet:
        vnet.up()
    with ipdb.interfaces['vnet3'] as vnet:
        vnet.up()
    with ipdb.interfaces['br-test'] as br:
        br.up()

#Calling Functions to Setup Proper Configuration
createNameSpace()
createAndMoveVeth()
createBridgeWithPorts()
bringUpDevices()

















