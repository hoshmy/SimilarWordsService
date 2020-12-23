import queue
import threading

from utilities.logger import Logger
from utilities.running_orchestrator import RunningOrchestrator
from configurations import configuration


class StatsCalculator:
    _number_of_requests = 0  # Can overflow?
    _timings_queue = queue.Queue()
    _accumulated_timings = 0.0
    _last_timing_pair = (0, 0.0)  # (_number_of_requests, _accumulated_timings) used for calculation synchronizing
    _running = False

    @staticmethod
    def add_request_stat(timing):
        try:
            StatsCalculator._timings_queue.put_nowait(timing)
        except queue.Full:
            Logger.log('StatsCalculator is Full, Stats doesnt handle incoming timings appropriately',
                       Logger.Level.WARNING)

    @staticmethod
    def worker():
        Logger.log('Stats calculator worker thread is up and running', Logger.Level.DEBUG)
        while RunningOrchestrator.KEEP_RUNNING:
            try:
                timing_sample = \
                    StatsCalculator._timings_queue.get(block=True, timeout=configuration.stats_calculator_timeout)
                StatsCalculator._accumulated_timings += timing_sample
                StatsCalculator._number_of_requests += 1
                StatsCalculator._last_timing_pair = \
                    (StatsCalculator._number_of_requests, StatsCalculator._accumulated_timings)
            except queue.Empty:
                pass

        Logger.log('Stats calculator worker thread is Down', Logger.Level.DEBUG)

    @staticmethod
    def init():
        if not StatsCalculator._running:
            # turn-on the worker thread
            threading.Thread(target=StatsCalculator.worker, daemon=True).start()
            StatsCalculator._running = True

    @staticmethod
    def get_stats():
        current_timing_pair = (StatsCalculator._last_timing_pair[0], StatsCalculator._last_timing_pair[1])
        average_processing_time_ns = 0
        if StatsCalculator._last_timing_pair[0]:
            accumulated_time_ns = StatsCalculator._last_timing_pair[1] * 10**9
            average_processing_time_ns = int(accumulated_time_ns / StatsCalculator._last_timing_pair[0])
        answer = {
            'totalRequests': StatsCalculator._last_timing_pair[0],
            'avgProcessingTimeNs': average_processing_time_ns
        }

        return answer
