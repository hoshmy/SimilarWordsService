import queue
import threading
import time

from utilities.logger import Logger
from utilities.running_orchestrator import RunningOrchestrator


class StatsCalculator:
    _number_of_requests = 0
    _timings_queue = queue.Queue()
    _accumulated_timings = 0.0
    _last_timing_pair = (0, 0.0)  # (_number_of_requests, _accumulated_timings) used for calculation synchronizing
    _running = False
    _worker_thread_yield_time = 1e-6

    @staticmethod
    def add_request_stat(timing: float) -> None:
        try:
            # Non blocking put in synchronized queue. IF queue is full the sample is discarded
            StatsCalculator._timings_queue.put_nowait(timing)
        except queue.Full:
            Logger.log('StatsCalculator is Full, Stats doesnt handle incoming timings appropriately',
                       Logger.Level.WARNING)

    @staticmethod
    def init() -> threading.Thread:
        thread = None
        if not StatsCalculator._running:  # Avoid double initialization
            thread = threading.Thread(target=StatsCalculator._worker, daemon=True)
            thread.start()
            StatsCalculator._running = True
        else:
            Logger.log('StatsCalculator double initialization was blocked', Logger.Level.WARNING)

        # The thread is returned for client to join
        return thread

    @staticmethod
    def get_stats() -> dict:
        # single shot copying of statistics information to avoid inter threads interference
        number_of_requests, accumulated_timings = tuple(StatsCalculator._last_timing_pair)
        average_processing_time_ns = 0

        if number_of_requests > 0:  # Avoid dividing by zero
            accumulated_time_ns = accumulated_timings * 10**9  # Convert from seconds to nano seconds
            average_processing_time_ns = int(accumulated_time_ns / number_of_requests)

        answer = {
            'totalRequests': number_of_requests,
            'avgProcessingTimeNs': average_processing_time_ns
        }

        return answer

    @staticmethod
    def _worker() -> None:
        Logger.log('Stats calculator worker thread is up and running', Logger.Level.DEBUG)
        while RunningOrchestrator.KEEP_RUNNING:
            try:
                # No timeout. the queue is released upon program exit from main
                timing_sample = \
                    StatsCalculator._timings_queue.get(block=True)
                StatsCalculator._accumulated_timings += timing_sample
                StatsCalculator._number_of_requests += 1

                # Save a statistics pair for perfect synchronization upon stats query
                StatsCalculator._last_timing_pair = \
                    (StatsCalculator._number_of_requests, StatsCalculator._accumulated_timings)
                time.sleep(StatsCalculator._worker_thread_yield_time)
            except queue.Empty:
                pass

        StatsCalculator._running = False
        Logger.log('Stats calculator worker thread is Down', Logger.Level.DEBUG)
