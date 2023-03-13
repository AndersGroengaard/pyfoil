

import sys
import warnings




__version__ = "0.1.0-a"



if sys.version_info.major <= 3 and sys.version_info.minor <= 8:
    warnings.warn(
        "Python 3.8 or older will soon be deprecated."
        " Please upgrade to Python 3.9 or newer.",
        DeprecationWarning,
    )