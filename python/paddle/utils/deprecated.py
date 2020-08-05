# Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
decorator to deprecate a function or class
"""

import warnings
import functools
from packaging import version
import paddle

_current_version = version.parse(paddle.__version__)


def deprecated(update_to="", since="", reason=""):
    """Decorate a function to signify its deprecation.

       This function wraps a method that will soon be removed and does two things:
           - The docstring of the API will be modified to include a notice
             about deprecation."
           - Raises a :class:`~exceptions.DeprecatedWarning` when old API is called.
       Args:
           since(str): The version at which the decorated method is considered deprecated.
           update_to(str): The new API users should use.
           reason(str): The reason why the API is deprecated.
       Returns:
           decorator: decorated function or class.
    """

    def decorator(func):
        """construct warning message, and return a decorated function or class."""
        assert isinstance(update_to, str), 'type of "update_to" must be str.'
        assert isinstance(since, str), 'type of "since" must be str.'
        assert isinstance(reason, str), 'type of "reason" must be str.'

        _since = since.strip()
        _update_to = update_to.strip()
        _reason = reason.strip()

        msg = 'API "{}.{}" is deprecated'.format(func.__module__, func.__name__)
        if len(_since) > 0:
            msg += " since {}".format(_since)
        msg += ", and may be removed in future versions."
        if len(_update_to) > 0:
            assert _update_to.startswith(
                "paddle."
            ), 'Argument update_to must start with "paddle.", your value is "{}"'.format(
                update_to)
            msg += ' Use "{}" instead.'.format(_update_to)
        if len(_reason) > 0:
            msg += "\n reason: {}".format(_reason)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """check version, and print warning if current version is newer than deprecated version."""
            if paddle.__version__ == "0.0.0" or _since == "" or _current_version >= version.parse(
                    _since):
                # if current version is develop version or newer than _since, print deprecation warning.
                warnings.simplefilter('always',
                                      DeprecationWarning)  # turn off filter
                warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
                warnings.simplefilter('default',
                                      DeprecationWarning)  # reset filter
            return func(*args, **kwargs)

        return wrapper

    return decorator
