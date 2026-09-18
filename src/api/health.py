"""Health check endpoint for CipherChat server."""

import time
import psutil
from dataclasses import dataclass


@dataclass
class HealthStatus:
    """Server health status."""
    status: str
    uptime: float
    memory_mb: float
    cpu_percent: float
    active_connections: int
    version: str = "0.1.0"


class HealthChecker:
    """Monitors server health metrics."""

    def __init__(self):
        self.start_time = time.monotonic()
        self.active_connections = 0

    def check(self) -> HealthStatus:
        """Return current health status."""
        return HealthStatus(
            status="healthy",
            uptime=time.monotonic() - self.start_time,
            memory_mb=psutil.Process().memory_info().rss / 1024 / 1024,
            cpu_percent=psutil.cpu_percent(interval=0.1),
            active_connections=self.active_connections,
        )

    def connection_opened(self):
        self.active_connections += 1

    def connection_closed(self):
        self.active_connections = max(0, self.active_connections - 1)
