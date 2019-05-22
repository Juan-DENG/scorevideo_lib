# This file is part of scorevideo_lib: A library for working with scorevideo
# Use of this file is governed by the license in LICENSE.txt.

"""Add marks from annotations (behaviors) in other logs

"""

from typing import List, Tuple
import re
from datetime import timedelta
from scorevideo_lib.parse_log import RawLog, Log, Mark, BehaviorFull


START_MARK = "video start"
END_MARK = "video end"


def copy_mark_disjoint(logs: List[Log], src_pattern: str, dest: RawLog,
                       dest_label: str) -> RawLog:
    """Copy a behavior into another log file as a mark, adjusting time and frame

    Time and frame are adjusted so as to be correct (potentially by being
    negative) in relation to the other entries in ``dest``, assuming that the
    logs in ``logs`` are in order, consecutive, and non-overlapping and that
    ``dest`` begins immediately after the last behavior scored in the last log
    of ``logs``.

    Args:
        logs: List of consecutive and non-overlapping logs to search for
            ``src_pattern`` in and account for when adjusting time and frame
        src_pattern: Search pattern (regular expression) that identifies the
            behavior to copy
        dest: Log to insert mark into
        dest_label: Label for inserted mark

    Returns:
        A copy of ``dest``, but with the new mark inserted

    """

    log_tuples = []

    for log in logs:
        end_mark = get_ending_mark(log.marks)
        log_tuples.append((log, end_mark.time, end_mark.frame))

    return copy_mark(log_tuples, src_pattern, dest, dest_label)


def copy_mark(logs: List[Tuple[Log, timedelta, int]], src_pattern: str,
              dest: RawLog, dest_label: str) -> RawLog:
    """Copy a behavior into another log file as a mark, adjusting time and frame

    Time and frame are adjusted so as to be correct (potentially by being
    negative) in relation to the other entries in ``dest``. The logs are aligned
    in time using the provided start time and frame information.

    Args:
        logs: List of tuples containing log to search for ``src_pattern`` in and
            account for when adjusting time and frame, time at which the next
            video (``dest`` for last video) starts, and frame at which the next
            video (``dest`` for last video) starts
        src_pattern: Search pattern (regular expression) that identifies the
            behavior to copy
        dest: Log to insert mark into
        dest_label: Label for inserted mark

    Returns:
        A copy of ``dest``, but with the new mark inserted

    """
    found = False
    frames = 0
    time = timedelta(seconds=0)
    for tup in logs:
        tup[0].sort_lists()

    for log, s_time, s_frame in logs:
        if not found:
            for behav in log.full:
                if re.match(src_pattern, behav.description):
                    found = True

                    frames = s_frame - behav.frame
                    time = s_time - behav.time
        else:
            frames += s_frame
            time += s_time

    new_mark = Mark(-frames, -time, dest_label)
    new_log = RawLog.from_raw_log(dest)
    new_log.marks.append(new_mark.to_line_tab())
    return new_log


def get_ending_mark(marks: List[Mark]) -> Mark:
    """Get the mark that has :py:const:`END_MARK` as its :py:attr:`Mark.name`

    Args:
        marks: List of marks to search through

    Returns:
        The identified :py:class:`Mark`

    Raises:
        ValueError: When no matching mark is found

    """
    for mark in marks:
        if mark.name == END_MARK:
            return mark
    raise ValueError("No mark with name '{}' found in list '{}'".format(
        END_MARK, marks))


def get_ending_behav(behavs: List[BehaviorFull],
                     end_descriptions: List[str]) -> BehaviorFull:
    """Get the behavior whose description is found in a list

    Args:
        behavs: List of behaviors whose descriptions to search through
        end_descriptions: List of descriptions to search for

    Returns: The first behavior whose description is found in the list

    """
    for behav in behavs:
        if behav.description in end_descriptions:
            return behav
    raise ValueError("No ending behavior description found in '{}'".format(
        behavs))
