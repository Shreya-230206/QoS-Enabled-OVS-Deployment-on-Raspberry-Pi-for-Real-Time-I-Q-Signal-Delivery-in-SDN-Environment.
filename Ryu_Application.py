# MIT License
# 
# Copyright (c) 2025 Shreya-230206
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ryu.app.simple_switch_13 import SimpleSwitch13
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, set_ev_cls

class ExtendedQueueSwitch(SimpleSwitch13):
    def __init__(self, *args, **kwargs):
        super(ExtendedQueueSwitch, self).__init__(*args, **kwargs)
        self.datapath = None
        self.server_port = 1  # Server is connected to port 1 of the switch
        self.priority_ip = "10.0.0.20"  # High-priority client
        self.low_priority_ip = "10.0.0.10"  # Lower-priority client

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # Retain default L2 learning behavior
        super(ExtendedQueueSwitch, self).switch_features_handler(ev)

        self.datapath = ev.msg.datapath
        self.logger.info("Switch connected. Installing queue-based flow rules.")
        self.install_ip_queue_flows()

    def install_ip_queue_flows(self):
        parser = self.datapath.ofproto_parser
        ofproto = self.datapath.ofproto

        # ---------------- Queue 0 for High-Priority Client ----------------
        match_q0 = parser.OFPMatch(
            eth_type=0x0800,           # IPv4 packets
            ipv4_src=self.priority_ip  # Match source IP
        )
        actions_q0 = [
            parser.OFPActionSetQueue(0),
            parser.OFPActionOutput(self.server_port)
        ]
        inst_q0 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions_q0)]

        mod_q0 = parser.OFPFlowMod(
            datapath=self.datapath,
            priority=100,
            match=match_q0, 
            instructions=inst_q0
        )
        self.datapath.send_msg(mod_q0)
        self.logger.info(f"Installed flow: {self.priority_ip} → queue 0 → port {self.server_port}")

        # ---------------- Queue 1 for Low-Priority Client ----------------
        match_q1 = parser.OFPMatch(
            eth_type=0x0800,
            ipv4_src=self.low_priority_ip
        )
        actions_q1 = [
            parser.OFPActionSetQueue(1),
            parser.OFPActionOutput(self.server_port)
        ]
        inst_q1 = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions_q1)]

        mod_q1 = parser.OFPFlowMod(
            datapath=self.datapath,
            priority=100,
            match=match_q1,
            instructions=inst_q1
        )
        self.datapath.send_msg(mod_q1)
        self.logger.info(f"Installed flow: {self.low_priority_ip} → queue 1 → port {self.server_port}")
