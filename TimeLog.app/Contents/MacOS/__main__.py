#!/Users/micha/opt/miniconda3/bin/python
# anaconda python has to be explicitly referenced here to work in an app
# /usr/bin/env python fails to ask for permission to access app dir (~/Documents/TimeLLog)
# and crashes with SIGKILL

import sys

from TimeLog.TimeLog import main


if __name__ == '__main__':
    sys.exit(main())
