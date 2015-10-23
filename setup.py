# vim: filetype=python3 tabstop=2 expandtab

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
