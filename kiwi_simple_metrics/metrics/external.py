import os
import subprocess
from typing import Iterator

from ..settings import SETTINGS
from ._report import Report, ReportData


def _hwdata() -> Iterator[ReportData]:
    def parse_output(exe: os.PathLike) -> ReportData:
        try:
            # check exe is executable
            assert os.access(exe, os.X_OK)

            # run exe
            # => TimeoutExpired: execution took too long
            execution = subprocess.run(
                args=[exe],
                stdout=subprocess.PIPE,
                timeout=SETTINGS.external.timeout,
            )

            # look at the first four output lines
            # => UnicodeDecodeError: output is not decodable
            output = execution.stdout.decode().split("\n")[:4]

            # extract and check name (fail if empty)
            assert (name := "".join(
                char
                for char in output[0]
                if char.isprintable()
            )[:100]) != ""

        except (AssertionError,
                subprocess.TimeoutExpired,
                UnicodeDecodeError,
                IndexError):
            return ReportData.from_settings(
                name=os.path.basename(exe)[:100],
                value=100,
                settings=SETTINGS.external,
            )

        try:
            # check exit status
            assert execution.returncode == 0

            # check output length
            assert len(output) == 4

            # extract threshold and value
            threshold = float(output[1])
            value = float(output[3])

            # extract and check inversion
            assert (inverted := output[2].strip().lower()) in (
                "normal", "inverted",
            )

        except (ValueError, AssertionError):
            return ReportData.from_settings(
                name=name,
                value=100,
                settings=SETTINGS.external,
            )

        # success
        return ReportData(
            name=name,
            value=value,
            threshold=threshold,
            inverted=inverted == "inverted",
            format=SETTINGS.external.report,
        )

    yield from (
        parse_output(exe)
        for exe in SETTINGS.external.executables
    )


def external() -> Report | None:
    """
    External Metric
    =====

    This metric's values are defined external executables (e.g. shell scripts).
    Any executable with suitable output can be used as a value for this metric.

    To comply, the executable's output must be UTF-8 decodable and start with
    four consecutive lines holding the following information:

    1. value name
    2. percent threshold
    3. the string "normal" or "inverted", without quotes
    4. percent current value

    The executable may produce additional output, which will be ignored.
    Percentages may be floating point numbers and must use a decimal point "."
    as a separator in that case.
    The output is evaluated once execution finishes with exit status 0.
    A report is generated for each executable. Its value name is stripped of
    non-printable characters and limited to a length of 100.

    Non-compliance will be reported as failed values, i.e. normal values with a
    threshold of 0% and a value of 100%, in these cases:

    - non-executable files and executables outputting non-UTF8:
        reported as the files' basename
    - executables with generally noncompliant outputs:
        reported as the first line of output
    - failure to parse any of the threshold, inversion or current value
    - otherwise compliant executables with non-zero exit status
    """

    return Report.aggregate(
        settings=SETTINGS.external,
        get_data=_hwdata,
    )
