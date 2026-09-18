"""Tests for health check endpoint."""

import time
import pytest
from src.api.health import HealthChecker, HealthStatus


class TestHealthChecker:
    def setup_method(self):
        self.checker = HealthChecker()

    def test_initial_status_healthy(self):
        status = self.checker.check()
        assert status.status == "healthy"

    def test_uptime_increases(self):
        status1 = self.checker.check()
        time.sleep(0.01)
        status2 = self.checker.check()
        assert status2.uptime > status1.uptime

    def test_memory_positive(self):
        status = self.checker.check()
        assert status.memory_mb > 0

    def test_connection_tracking(self):
        assert self.checker.active_connections == 0
        self.checker.connection_opened()
        assert self.checker.active_connections == 1
        self.checker.connection_opened()
        assert self.checker.active_connections == 2
        self.checker.connection_closed()
        assert self.checker.active_connections == 1

    def test_connection_close_floor(self):
        self.checker.connection_closed()
        assert self.checker.active_connections == 0

    def test_version(self):
        status = self.checker.check()
        assert status.version == "0.1.0"
