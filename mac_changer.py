#!usr/bin/env python

import subprocess
import optparse
import re
def get_armgs():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="address", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[+] Please enter the interface, type --help for more info.")
    elif not options.address:
        parser.error("[+] Please enter the new mac address, type --help for more info.")
    return options

def mac_changer(interface, address):
    print("[+] Changing MAC address for " + interface + " to " + address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", address])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[+]Could not read the mac address.")

options = get_armgs()
current_mac = get_current_mac(options.interface)
print(">>Current mac: " + str(current_mac))
mac_changer(options.interface, options.address)

def verify_mac(interface):
    current_mac = get_current_mac(interface)

    if current_mac == options.address:
        print("[+]MAC address successfully changed to :" + current_mac)
    else:
        print("[-]MAC address did not get changed.")
verify = verify_mac(options.interface)
