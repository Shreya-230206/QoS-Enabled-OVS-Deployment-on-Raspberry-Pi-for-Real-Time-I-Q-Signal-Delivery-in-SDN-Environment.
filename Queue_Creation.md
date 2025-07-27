# Creating Queues for each host
Created two queues allocating 70% of the bandwidth to queue0 and remaining to queue1 on port eth0, to which the server is connected.
$sudo ovs-vsctl \
-- set port h1 qos=@newqos \
-- --id=@newqos create qos type=linux-htb other-config:max-rate=20000000 \
queues:0=@q0 queues:1=@q1 \
-- --id=@q0 create queue other-config:min-rate=14000000 other-config:max-rate=20000000 \
-- --id=@q1 create queue other-config:min-rate=6000000 other-config:max-rate=6000000

---

## What this does: 
The command is a series of ovs-vsctl instructions to configure Quality of Service (QoS) on a port named h1 in Open vSwitch. Here's a breakdown:

-- set port h1 qos=@newqos: Associates the h1 port with a new QoS configuration named @newqos.
-- --id=@newqos create qos type=linux-htb other-config:max-rate=20000000 queues:0=@q0 queues:1=@q1: Creates a QoS entry of type linux-htb (Hierarchical Token Bucket) with a maximum rate of 20,000,000 bps (20 Mbps), and defines two queues: @q0 and @q1.
-- --id=@q0 create queue other-config:min-rate=14000000 other-config:max-rate=20000000: Creates queue @q0 with a minimum rate of 14,000,000 bps (14 Mbps) and a maximum rate of 20,000,000 bps (20 Mbps).
-- --id=@q1 create queue other-config:min-rate=6000000 other-config:max-rate=6000000: Creates queue @q1 with a minimum rate of 6,000,000 bps (6 Mbps) and a maximum rate of 6,000,000 bps (6 Mbps).
This configuration sets up traffic shaping on port h1, allocating bandwidth with a total cap of 20 Mbps, where queue @q0 can use up to 14-20 Mbps and queue @q1 is limited to 6 Mbps.
