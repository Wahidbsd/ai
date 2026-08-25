import os
import subprocess
import time

def capture_handshake(interface='wlan0', duration=60, output='capture.cap'):
    print("[+] Starting packet capture on %s for %d seconds..." % (interface, duration))
    cmd = ['tcpdump', '-i', interface, '-n', '-e', '-v', '-c', '5000', '-w', output]
    try:
        subprocess.run(cmd, timeout=duration, check=True)
        print("[+] Capture completed. File saved as %s" % output)
        return True
    except subprocess.TimeoutExpired:
        print("[!] Timeout reached, but capture may still be valid.")
        return True
    except Exception as e:
        print("[ERROR] %s" % str(e))
        return False

def extract_pmkid(cap_file):
    print("[+] Extracting PMKID from %s..." % cap_file)
    # This uses hcxdump tool – you can also use aircrack-ng
    cmd = ['aircrack-ng', cap_file, '-J', 'output']
    subprocess.run(cmd)
    print("[+] PMKID extracted to output.hccapx (if available)")

if __name__ == "__main__":
    if capture_handshake():
        extract_pmkid('capture.cap')
    else:
        print("[!] Capture failed. Ensure tcpdump is installed and Wi-Fi is on.")