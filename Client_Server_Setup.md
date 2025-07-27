## Socket-Based IQ Signal Prioritization with OVS and Ryu

### Overview
Socket programming is used to simulate two types of traffic:
- **IQ Signal Data** → Sent from `Client 2 (10.0.0.2)`  
- **Competing Traffic** → Sent from `Client 1 (10.0.0.1)`  

Both traffic streams are transmitted to `Server (10.0.0.3)` through a **Raspberry Pi running Open vSwitch (OVS)**, which applies **QoS policies managed by the Ryu controller**.

---

### Server
- **Port:** `12345`
- **Functions:**
  - Listens for incoming connections.
  - Echoes received data back to the client.
  - Measures **actual bytes expected vs. received bytes**.
  - Computes **packet loss**:  
    ```
    loss = actual_bytes - received_bytes
    ```
  - Displays **bandwidth utilization per client**.

---

### Clients
1. **Client 1 (10.0.0.1)** – Sends continuous bulk data (e.g., file transfer or heavy stream).  
2. **Client 2 (10.0.0.2)** – Sends real-time IQ signal packets.

Both send to **the same destination port (12345)** at the server.

---

## Test Scenarios

### 1. Default Setup (No Controller)
- **Server Port:** Default queue installed (FIFO).
- **Effect:**  
  - Packets from both clients are queued together without priority.
  - Causes **packet loss for both clients** when sending simultaneously.
- **Result:**  
  - **IQ signal quality is degraded** due to no priority treatment.  
  *(See Figure 6)*

---

### 2. With Queues and Flows (Ryu Controlled)
- **Queue Configuration at Server Port:**
  - **Queue 0 (q0):** 70% bandwidth → Allocated to **Client 2 (IQ signals)**.
  - **Queue 1 (q1):** 30% bandwidth → Allocated to **Client 1 (bulk traffic)**.

- **Effect:**
  - IQ signals from Client 2 receive **strict priority**.
  - Bulk data from Client 1 is **rate-limited** and does not interfere with real-time IQ traffic.
