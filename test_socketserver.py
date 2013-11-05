"""
Tests for socketserver
"""

import unittest
from socketserver import ChatServer, Room, Client
import threading
import socket

class TestGetMsg(unittest.TestCase):
    def setUp(self):
        self.server = ChatServer(('', None))
        self.client = Client(None, None)

    def test_rqueues_new_client(self):
        self.assertEqual(self.server.rqueues, {})

        self.server.update_rqueues(self.client, 'Hello')
        self.assertEqual(self.server.rqueues.keys(), [self.client])
        self.assertEqual(self.server.rqueues[self.client], "Hello")

    def test_rqueues_existing_client(self):
        self.server.rqueues[self.client] = "Goodbye\n"
        self.assertEqual(self.server.rqueues.keys(), [self.client])

        self.server.update_rqueues(self.client, "Hello")
        self.assertEqual(self.server.rqueues[self.client], "Goodbye\nHello")

class TestMultipleConnections(unittest.TestCase):
    def setUp(self):
        self.server = ChatServer(('', None))
        self.client1 = Client(None, None)
        self.client2 = Client(None, None)
        self.client3 = Client(None, None)

    def add_all(self, *clients):
        # helper function to add clients to the server
        map(self.server.add, clients)

    def test_add_many_clients(self):
        """Test that all clients are added to server's list of clients'"""
        self.add_all(self.client1, self.client2, self.client3)
        self.assertEqual(self.server.clients,
                    [self.client1, self.client2, self.client3])

    def test_dispatch_msgs(self):
        self.add_all(self.client1, self.client2, self.client3)
        self.server.rqueues[self.client1] = "blah"
        self.assertEqual(len(self.server.wqueues), 3)

        self.server.dispatch_msgs()
        self.assertEqual(self.server.wqueues[self.client1], "")
        self.assertEqual(self.server.wqueues[self.client2], "blah")
        self.assertEqual(self.server.wqueues[self.client3], "blah")


if __name__ == '__main__':
    unittest.main()
