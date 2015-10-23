.. vim: tabstop=1 expandtab

pyphctool
=========

About
-----
`pyphctool` is a simple program to find and set CPU voltage IDs (VIDs) exposed
by the `PHC Linux kernel module`_.

.. _PHC Linux kernel module: http://www.linux-phc.org/

Dependencies
------------
- Python >= 3.4
- PHC Linux kernel module
- ``cpufreq`` kernel module

Installation
------------
The included `distutils` setup script can be used to install the files::

 $ python setup.py install

Usage
-----
Find VIDs
*********
Safe VIDs for a CPU can be determined using the ``findvids`` subcommand.
Since Intel & AMD CPUs differ in how the VIDs are actually mapped to the
voltages, the CPU type must be specified to the ``findvids`` subcommand.

For Intel CPUs::

 $ pyphctool findvids intel

And for AMD CPUs::

 $ pyphctool findvids amd
 
``findvids`` works by stressing the CPU while iteratively decreasing the CPU
voltage until the **system crashes**.

Once ``findvids`` finishes (or the system crashes), safe VIDs can be found in
the ``passedvids.temp`` file.

**NOTE:** ``findvids`` **WILL crash your system**

Set VIDs
********
To set VIDs from a config file use the ``setvids`` subcommand::

 $ pyphctool setvids /etc/phc/vids.conf
 
The format of this file will differ from system to system. It should contain a
line containing VIDs for every FID (frequency ID) the CPU supports delimited by
whitespace.
 
Systemd
*******
A ``Systemd`` service is included to automatically set the VIDs at boot time.
Enable it using::

 $ systemctl enable pyphctool-setvids.service
 
Disable it using::

 $ systemctl disable pyphctool-setvids.service
 
The service expects there to be a config file at ``/etc/phc/vids.conf``
