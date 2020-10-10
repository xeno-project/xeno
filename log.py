__author__ = "Andreas H. Kelch"

# xeno-Project - A no Google, no cloud ViUR Framework
#
# Copyright (c) 2019-2020 Andreas H. Kelch
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import logging, os
from colorlog import ColoredFormatter

DEFAULT = '\033[m'
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

BOLD = '\033[1m'
UNDERLINE = '\033[2m'

colors = {
    'DEBUG': 'purple',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
    "EXCEPTION":"green"
}

isDebugMode = True
if isDebugMode:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO


class xenoFormatter(ColoredFormatter):

    def format(self, record):
        if 'pathname' in record.__dict__.keys():
            # truncate the pathname
            if "/deploy" in record.pathname:
                pathname = "."+record.pathname.split("/deploy") [1]
            else:
                pathname = record.pathname
                #pathname = os.path.basename(record.pathname)
                #if len(pathname) > 20:
                #    filename = '{}~{}'.format(pathname[:3], pathname[-16:])
            record.pathname = pathname
        return super(xenoFormatter, self).format(record)


formatter = xenoFormatter('--------------------------\n%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d]%(log_color)s %(message)s%(reset)s',log_colors = colors)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(LOG_LEVEL)
try:
    log.removeHandler(log.handlers[0])
except:
    pass
log.addHandler(stream)
log.propagate = False


