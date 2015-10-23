# vim: filetype=python3 tabstop=2 expandtab

from distutils.core import setup

if __name__ == "__main__":
  setup(
    name = 'pyphctool',
    version = '0.1',
    description = 'Find, set PHC VIDs for under/over volting CPUs.',
    author = 'Jashandeep Sohi',
    author_email = 'jashandeep.s.sohi@gmail.com',
    url = 'https://github.com/jashandeep-sohi/pyphctool',
    license = 'GPLv3',
    py_modules = ['pyphctoolcore'],
    scripts = ['pyphctool'],
    data_files = [
      ('/etc/phc', ['vids.conf']),
      ('/usr/lib/systemd/system', ['pyphctool-setvids.service'])
    ]
  )
