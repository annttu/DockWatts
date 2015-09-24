#!/bin/python


"""
/usr/sbin/system_profiler SPPowerDataType

      Amperage (mA): -790
            Voltage (mV): 12012
"""

from subprocess import Popen, PIPE

def get_watts():
    p = Popen(['/usr/sbin/system_profiler', 'SPPowerDataType'], stdout=PIPE)

    (stdout, stderr) = p.communicate()

    ampers = 0
    volts = 0

    for line in stdout.splitlines():
        if line.strip().startswith("Amperage (mA)"):
            ampers = float(int(line.split(':', 1)[1].strip().replace('\xe2\x88\x92','-')))
        elif line.strip().startswith("Voltage (mV):"):
            volts = float(int(line.split(':', 1)[1].strip().replace('\xe2\x88\x92','-')))

    #print("ampers: %s volts: %s" % (ampers, volts))

    return (volts * ampers) / -1000000.0


if __name__ == '__main__':
    watts = get_watts()
    print("%.2f W" % watts)

