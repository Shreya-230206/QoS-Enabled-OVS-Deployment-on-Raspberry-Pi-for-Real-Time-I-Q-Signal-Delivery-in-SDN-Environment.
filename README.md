# QoS-Enabled-OVS-Deployment-on-Raspberry-Pi-for-Real-Time-I-Q-Signal-Delivery-in-SDN-Environment.
This project demonstrates how SDN principles, combined with lightweight hardware like Raspberry Pi, can be effectively used to implement host-based prioritization and traffic control. 

## Abstract
Modern communication systems often involve multiple clients transmitting varying types of data, some of which are more critical or time-sensitive than others. Traditional static network infrastructures lack the flexibility to prioritize traffic based on the sender, leading to performance degradation during congestion. This project addresses this limitation by designing a cost-effective Software-Defined Networking (SDN) testbed using a Raspberry Pi 4 configured as an Open vSwitch (OVS), where traffic from a specific client is dynamically prioritized over others using Quality of Service (QoS) mechanisms.
A Python-based Ryu SDN controller manages the flow rules and queue assignments on the switch, identifying connected hosts and installing queue-specific rules based on source IP addresses. The prioritized client’s traffic is directed to a high-bandwidth queue, while lower-priority clients are limited to a constrained bandwidth path. The performance of the setup was evaluated using a socket-based client-server model, where multiple clients sent data—both bulk and time-sensitive—to a server. Results show that with SDN-enabled prioritization, the high-priority client consistently achieved higher bandwidth and zero packet loss, even under congestion, while lower-priority clients experienced controlled throughput and packet drops. Without QoS, bandwidth was shared inefficiently, leading to contention and performance degradation.
This project demonstrates how SDN principles, combined with lightweight hardware like Raspberry Pi, can be effectively used to implement host-based prioritization and traffic control. It provides a flexible, scalable, and low-cost solution suitable for edge computing, real-time systems, and network-aware IoT applications.


---

## Steps
1. [Install Ryu Controller](Install_Ryu.md)
2. [Raspberry as an OVS configuration](Raspberry_Configuration.md)
3. [Create Queues for each host](Queue_Creation.md) 
4. [Connect hosts to switch ports](Network_Topology.md)
5. [Dynamic Flows installation with Ryu application](Ryu_Application.py)
	###### This Ryu application is built by extending SimpleSwitch13 and provides dynamic flow installation with QoS queue prioritization for specific hosts in a 	Software-Defined Network (SDN). It retains normal L2 switching behavior (learning switch) and adds special treatment for traffic from a designated host (h2) 	by directing it into a high-priority queue.
	###### Features:
	1. Maintains L2 learning switch behavior
	2. Adds dynamic QoS policy for critical traffic
	3. Ensures priority bandwidth for selected host
	4. Easily extensible for more queue logic or flow types
	###### How it works: 
	1.	Extends SimpleSwitch13: Inherits MAC learning and basic forwarding logic (priority=1 flows).
	2.	Handles Switch Connection: Stores the datapath and installs default table-miss flow (via base class).
	3.	Detects New Hosts: Uses EventHostAdd to react when a new host connects to the switch.
	4.	Checks Server Port (Port 3): Skips flows installation if the host is connected to port 3 (reserved for server), flow rules are meant to prioritize traffic 	going to the server, not from it.
	5.	Identifies Priority Host (MAC 00:00:00:00:00:02)
    	1. Installs a high-priority flow (priority=100)
    	2. Sets traffic to Queue 0 using OFPActionSetQueue
    	3. Forwards traffic to server port (port 3)
	6.	For Other Hosts
    	1. Default SimpleSwitch13 behavior handles them (no queue set).
    	2. Traffic is forwarded based on learned MAC–port mappings.
6. [Performance Evaluation](Results.md)
---

## Repository Purpose
This repository is designed for **beginners** who want to:
- Learn SDN basics
- Experiment with Raspberry Pi as a network switch
- Implement QoS using SDN controllers  

---

## Author
Shreya Kumari | https://www.linkedin.com/in/shreya-kumari-23feb2006 | shreya230206@gmail.com

## License
MIT License
