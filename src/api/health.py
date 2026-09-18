"""Health check endpoint for CipherChat server."""

import time
from dataclasses import dataclass, asdict

try:
    import psutil
    _HAS_PSUTIL = True
except ImportError:
    psutil = None
    _HAS_PSUTIL = False


@dataclass
class HealthStatus:
    """Server health status."""
    status: str
    uptime: float
    memory_mb: float
    cpu_percent: float
    active_connections: int
    version: str = "0.1.0"

    def to_dict(self) -> dict:
        return asdict(self)


class HealthChecker:
    """Monitors server health metrics (psutil optional)."""

    def __init__(self):
        self.start_time = time.monotonic()
        self.active_connections = 0

    def check(self) -> HealthStatus:
        """Return current health status."""
        if _HAS_PSUTIL:
            try:
                memory_mb = psutil.Process().memory_info().rss / 1024 / 1024
            except Exception:
                memory_mb = 0.0
            try:
                cpu_percent = psutil.cpu_percent(interval=None)
            except Exception:
                cpu_percent = 0.0
        else:
            memory_mb = 0.0
            cpu_percent = 0.0
        return HealthStatus(
            status="healthy",
            uptime=time.monotonic() - self.start_time,
            memory_mb=memory_mb,
            cpu_percent=cpu_percent,
            active_connections=self.active_connections,
        )

    def connection_opened(self):
        self.active_connections += 1

    def connection_closed(self):
        self.active_connections = max(0, self.active_connections - 1)
