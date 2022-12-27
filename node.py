from threading import Event, Thread, Timer
from datetime import datetime, timedelta
import time
from nodeServer import NodeServer
from nodeSend import NodeSend
from message import Message
import config
from enum_type import STATE
from math import ceil, sqrt
import re
import select
import sys
import random



class Node():
    def __init__(self,id):
        Thread.__init__(self)
        self.id = id

        self.CS_INT = 15
        self.NEXT_REQ = 15

        self.port = config.port+id
        self.daemon = True
        self.lamport_ts = 0

        self.curr_state = STATE.INIT

        # attributes as a voter (receive & process request)
        self.has_voted = False
        self.voted_request = None
        self.request_queue = []  # a priority queue (key = lamportTS, value = request)

        # attributess as a proposer (propose & send request)
        self.num_votes_received = 0
        self.has_inquired = False
        
        # Event signals
        self.signal_request_cs = Event()
        self.signal_request_cs.set()
        self.signal_enter_cs = Event()
        self.signal_exit_cs = Event()

        # Timestamp for next expected request/exit
        self.time_request_cs = None
        self.time_exit_cs = None

        self.server = NodeServer(self)
        self.server.start()

        self.client = NodeSend(self)

        if id % 2 == 0:
            self.collegues = list(range(0,config.numNodes,2))
            print("Colegas del nodo : -" ,self.id,self.collegues)
            self.voting_set = dict()
            for i in range(0, len(self.collegues)):
                self.voting_set[self.collegues[i]] = None
            print (self.voting_set)


        else:
            self.collegues = list(range(1,config.numNodes,2))
            print("Colegas del nodo : -" ,self.id,self.collegues)
            self.voting_set = dict()
            for i in range(0, len(self.collegues)):
                self.voting_set[self.collegues[i]] = None
            print (self.voting_set)

    def do_connections(self):
        self.client.build_connection()


    def _reset_voting_set(self):
        for voter in self.voting_set:
            self.voting_set[voter] = None

    def request_cs(self, ts):
        """Node requests to enter critical section.
        Set state to REQEUST.
        Increase lamport timestamp by 1.
        Multicast the request to its voting set.
        """
        self.curr_state = STATE.REQUEST
        self.lamport_ts += 1
        request_msg = Message(msg_type="REQUEST",src=self.id)
        print("---Node asking for cs : ", self.id)
        self.client.multicast(request_msg, self.voting_set.keys())
        self.signal_request_cs.clear()

    def enter_cs(self, ts):
        """Node enters the critical section.
        Set state to HELD.
        Increase lamport timestamp by 1.
        Calculate the timestamp that it should exit.
        """
        print("---Node asking entering cs : ", self.id)
        self.time_exit_cs = ts + timedelta(milliseconds=self.CS_INT)
        self.curr_state = STATE.HELD    
        self.lamport_ts += 1
        self.signal_enter_cs.clear()

    def exit_cs(self, ts):
        """Node exits the critical section.
        Set state to RELEASE.
        Increase lamport timestamp by 1 and reset corresponding variables.
        Multicast the release message to its voting set.
        """
        self.time_request_cs = ts + timedelta(milliseconds=self.NEXT_REQ)
        self.curr_state = STATE.RELEASE
        self.lamport_ts += 1
        self.num_votes_received = 0
        # self._reset_voting_set()
        print("---Node leaving for cs : ", self.id)
        release_msg = Message(msg_type="RELEASE",src=self.id)
        self.client.multicast(release_msg, self.voting_set.keys())
        self.signal_exit_cs.clear()

    def build_connection(self, num_node):
        self.client.build_connection(num_node)
    def state(self):
        timer = Timer(1, self.state) #Each 1s the function call itself
        timer.start()
        self.curr_time = datetime.now()


        if (self.curr_state == STATE.RELEASE and 
                self.time_request_cs <= self.curr_time):
            if not self.signal_request_cs.is_set():
                self.signal_request_cs.set()

        elif (self.curr_state == STATE.REQUEST and 
                self.num_votes_received == len(self.collegues)):
            if not self.signal_enter_cs.is_set():
                self.signal_enter_cs.set()

        elif (self.curr_state == STATE.HELD and 
                self.time_exit_cs <= self.curr_time):
            if not self.signal_exit_cs.is_set():
                self.signal_exit_cs.set()

    def run(self):
        print("Run Node%i with the follows %s"%(self.id,self.voting_set))
        self.client.start()
        self.wakeupcounter = 0
        self.state()
