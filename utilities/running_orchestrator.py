
"""
The Running orchestrator is a singleton like class that holds a global flag
 The flag signals whether the system is running or not
 It is a convenient way to signal to running threads that they should return
"""


class RunningOrchestrator:
    KEEP_RUNNING = True
