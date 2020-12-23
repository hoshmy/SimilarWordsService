#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from utilities.stats_calculator import StatsCalculator
from utilities.running_orchestrator import RunningOrchestrator


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


def similar_words_server_main():
    StatsCalculator.init()


if __name__ == '__main__':
    similar_words_server_main()
    main()
    RunningOrchestrator.KEEP_RUNNING = False
