# vim: filetype=python3 tabstop=2 expandtab

# pyphctool
# Copyright (C) 2015 Jashandeep Sohi <jashandeep.s.sohi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import pyphctool
from distutils.core import setup

if __name__ == "__main__":
  setup(
    name = "pyphctool",
    version = pyphctool.__version__,
    description = pyphctool.__doc__,
    author = "Jashandeep Sohi",
    author_email = "jashandeep.s.sohi@gmail.com",
    url = "https://github.com/jashandeep-sohi/pyphctool",
    license = "GPLv3",
    scripts = ["pyphctool.py"],
    data_files = [
      ("/etc/phc", ["vids.conf"]),
      ("/usr/lib/systemd/system", ["pyphctool-setvids.service"])
    ]
  )
