#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

from utilities.stats_calculator import StatsCalculator
from utilities.running_orchestrator import RunningOrchestrator
from utilities.logger import Logger


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SimilarWordsServer.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def _similar_words_server_main() -> threading.Thread:
    stats_thread_instance = None

    # Filter out the auto reloader mock run
    if os.environ.get('RUN_MAIN'):
        stats_thread_instance = StatsCalculator.init()

        if os.environ.get('test'):
            Logger.log('Running Test mode', Logger.Level.DEBUG)

    return stats_thread_instance


def _deinit_stats_calculator():
    # Adding stat_request will cause the statistics worker thread to exit
    StatsCalculator.add_request_stat(0)


if __name__ == '__main__':
    stats_thread = _similar_words_server_main()
    main()

    # Cleanup
    RunningOrchestrator.KEEP_RUNNING = False
    _deinit_stats_calculator()

    if stats_thread:
        stats_thread.join()
