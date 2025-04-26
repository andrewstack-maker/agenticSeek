import unittest
from unittest.mock import patch, MagicMock
import os, sys
import socket
import subprocess
from urllib.parse import urlparse
import platform

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add project root to Python path

from sources.llm_provider import Provider

class TestIsIpOnline(unittest.TestCase):
    def setUp(self):
        self.checker = Provider("ollama", "deepseek-r1:32b")

    def test_empty_address(self):
        """Test with empty address"""
        result = self.checker.is_ip_online("")
        self.assertFalse(result)

    def test_localhost(self):
        """Test with localhost"""
        test_cases = [
            "localhost",
            "http://localhost",
            "https://localhost",
            "127.0.0.1",
            "http://127.0.0.1",
            "https://127.0.0.1:8080"
        ]
        for address in test_cases:
            with self.subTest(address=address):
                result = self.checker.is_ip_online(address)
                self.assertTrue(result)

    def test_google_ips(self):
        """Test with known Google IPs"""
        google_ips = [
            "74.125.197.100",
            "74.125.197.139",
            "74.125.197.101",
            "74.125.197.113",
            "74.125.197.102",
            "74.125.197.138"
        ]
        for ip in google_ips:
            with self.subTest(ip=ip), \
                 patch('socket.gethostbyname', return_value=ip), \
                 patch('subprocess.run', return_value=MagicMock(returncode=0)):
                result = self.checker.is_ip_online(ip)
                self.assertTrue(result)

    def test_unresolvable_hostname(self):
        """Test with unresolvable hostname"""
        address = "nonexistent.example.com"
        with patch('socket.gethostbyname', side_effect=socket.gaierror):
            result = self.checker.is_ip_online(address)
            self.assertFalse(result)

    def test_valid_domain(self):
        """Test with valid domain name"""
        address = "google.com"
        with patch('socket.gethostbyname', return_value="142.250.190.78"), \
             patch('subprocess.run', return_value=MagicMock(returncode=0)):
            result = self.checker.is_ip_online(address)
            self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()