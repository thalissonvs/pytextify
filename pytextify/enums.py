from enum import Enum


class TaskStatus(str, Enum):
    PROCESSING = 'processing'
    DONE = 'done'
    FAILED = 'failed'
