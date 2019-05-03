# -*- coding: utf-8 -*-

from functools import wraps


def skip_signal():
    """
    It provides a way to skip the signal to post_save
    to avoid unwanted recursion
    """
    def _skip_signal(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_signal'):
                return None
            return signal_func(sender, instance, **kwargs)
        return _decorator
    return _skip_signal
