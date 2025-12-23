#services/rate_limiter.py

import time
import random

class RateLimiter:
    def __init__(self, max_calls: int, window_sec: int):
        self.max_calls = max_calls
        self.window_sec = window_sec
        self.calls = []

    def allow(self) -> bool:
        now = time.time()
        self.calls = [t for t in self.calls if now - t < self.window_sec]

        if len(self.calls) >= self.max_calls:
            return False

        self.calls.append(now)
        return True


def retry_with_backoff(fn, retries: int = 3):
    for attempt in range(retries):
        try:
            return fn()
        except Exception:
            sleep_time = (2 ** attempt) + random.random()
            time.sleep(sleep_time)
    raise RuntimeError("Max retries exceeded")
