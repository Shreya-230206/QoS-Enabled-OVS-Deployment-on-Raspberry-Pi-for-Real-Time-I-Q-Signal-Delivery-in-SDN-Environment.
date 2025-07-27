# Raspberry as an OVS configuration

## This setup process included:
•	Installing OVS: Installed OVS 3.5.1 with necessary dependencies. 
•	Configuring Network Interfaces: Added four USB-to-Ethernet adapters (eth1 to eth4).
•	Creating OVS Bridge: Established a bridge (ovsbr0) and attached network interfaces. 
•	Connecting to Ryu Controller: Linked OVS to the Ryu controller via Open Flow.

### 1. Install Dependencies
$sudo apt update  
$apt-get install python-simplejson python-qt4 libssl-dev python-twisted-conch automake autoconf gcc uml-utilities libtool build-essential pkg-config 

### 2. Install Open vSwitch
$sudo apt update ; wget http://openvswitch.org/releases/openvswitch-3.5.1.tar.gz 

### 3. Unzip the file installed and go to directory
$tar -xvf openvswitch-3.5.1.tar.gz ; cd openvswitch-3.5.1

### 4. Run “uname -r” to see what version we are at and “apt-cache search linux-headers” to match the version of linux header and install the version
$uname -r
$apt-get install -y <linux-headers-your_version>

### 5. Use the “kernel headers in /lib/modules/6.12.25+rpt-rpi-v8/build” to compile the OVS kernel module (openvswitch.ko) for that kernel 
$kernel headers in /lib/modules/<your_version>

### 6. Build the OVS binaries and install into /usr/local/ 
$make && make install

### 7. Upload the model we just created to the OS
$modprobe openvswitch

### 8. Append the openvswitch to the file /etc/modules to automatically run “modprobe openvswitch” on every boot, which loads the openvswitch.ko kernel module into the running kernel
$echo "openvswitch" >> /etc/modules

### 9. Create new database file using vswitch.ovsschema
$touch /usr/local/etc/ovs-vswitchd.conf; mkdir -p /usr/local/etc/openvswitch; ovsdb-tool create /usr/local/etc/openvswitch/conf.db vswitchd/vswitch.ovsschema

### 10. Script file to start OVS./local
$nano script

### 11. Add this script
#!/bin/bash
ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
    --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
    --private-key=db:Open_vSwitch,SSL,private_key \
    --certificate=db:Open_vSwitch,SSL,certificate \
    --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
    --pidfile --detach
ovs-vsctl --no-wait init
ovs-vswitchd --pidfile --detach
ovs-vsctl show

### 12. Execute the file
$chmod +x script
$./script

#### And configuration of Raspberry Pi to act as an Open Flow Switch is completed. But we’ll see no components of the switch. 

---
## Next, adding bridge and ports:

### 1. Add a new network interface br0. br0 is your new virtual switch. 
$ovs-vsctl add-br br0

### 2. Add ports to the switch 
$ovs-vsctl add-port br0 eth0

### This will detach eth0 from the linux IP stack, hands control to Open vSwitch. Any traffic coming in from the physical NIC eth0 now enters the OVS bridge. 
### Similarly, add other ports as well as internal host, connecting via port h1 in to the OVS and assigning an IP:
$ovs-vsctl add-port br0 eth1
$ovs-vsctl add-port br0 eth2
$ovs-vsctl add-port br0 h1 –set interface h1 type=internal
$ip addr add 10.0.0.3/24 dev h1

---
## Add Controller:

### Add controller, set controller’s IP and port at which it runs
$ovs-vsctl set-controller br0 tcp:<Controller_IP>:6633
### Now, the switch will act as a dumb switch, and will be controlled by the controller.

### Verify configuration
$ovs-vsctl show
