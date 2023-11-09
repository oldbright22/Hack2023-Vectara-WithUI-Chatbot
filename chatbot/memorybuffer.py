import os

class MemoryBuffer:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.buffer = []

    def add_message(self, message):
        """Add a new message to the buffer."""
        if len(self.buffer) >= self.max_size:
            self.buffer.pop(0)  # Remove the oldest message if buffer exceeds its size
        self.buffer.append(message)

    def get_messages(self):
        """Retrieve all stored messages."""
        return self.buffer

    def clear(self):
        """Clear the buffer."""
        self.buffer = []
