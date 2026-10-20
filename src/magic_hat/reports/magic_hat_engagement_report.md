# Magic Hat Security Engagement Report

**Total Records Captured:** 7

---

## Executive Summary
This report aggregates telemetry, host discoveries, and service scans executed during the tactical engagement.

---

## Detailed Scan Telemetry Logs

### Log ID: 7 - Wireless Recon
* **Target Space:** `Airspace`
* **Timestamp:** `2026-10-19 18:09:16`
* **Metadata:** `{}`

```text
[-] Wi-Fi scanner ('nmcli') requires NetworkManager daemon, which is restricted in Termux without root/proot.
```

---

### Log ID: 6 - Wireless Recon
* **Target Space:** `Airspace`
* **Timestamp:** `2026-10-19 18:09:05`
* **Metadata:** `{}`

```text
[-] Wireless query failed: Command '['ip', 'link']' returned non-zero exit status 1.
```

---

### Log ID: 5 - Web Fuzzer
* **Target Space:** `http://192.168.8.0/24/FUZZ`
* **Timestamp:** `2026-10-19 18:08:07`
* **Metadata:** `{}`

```text

```

---

### Log ID: 4 - Pipeline Stage 2: Port Scan
* **Target Space:** `192.168.8.0/24`
* **Timestamp:** `2026-10-19 18:07:04`
* **Metadata:** `{}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 18:06 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.0099s latency).
Not shown: 94 closed tcp ports (conn-refused)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
445/tcp  open  microsoft-ds
8080/tcp open  http-proxy
8443/tcp open  https-alt

Nmap scan report for Roku.lan (192.168.8.119)
Host is up (0.28s latency).
All 100 scanned ports on Roku.lan (192.168.8.119) are in ignored states.
Not shown: 100 closed tcp ports (conn-refused)

Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.0038s latency).
All 100 scanned ports on Brandon-s-A16.lan (192.168.8.139) are in ignored states.
Not shown: 100 closed tcp ports (conn-refused)

Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.034s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8008/tcp open  http
8009/tcp open  ajp13
8443/tcp open  https-alt

Nmap scan report for 192.168.8.183
Host is up (0.022s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8008/tcp open  http
8009/tcp open  ajp13
8443/tcp open  https-alt

Nmap done: 256 IP addresses (5 hosts up) scanned in 6.50 seconds

```

---

### Log ID: 3 - Pipeline Stage 1: Sweep
* **Target Space:** `192.168.8.0/24`
* **Timestamp:** `2026-10-19 18:06:57`
* **Metadata:** `{}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 18:06 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.016s latency).
Nmap scan report for Roku.lan (192.168.8.119)
Host is up (0.040s latency).
Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.000094s latency).
Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.047s latency).
Nmap scan report for 192.168.8.183
Host is up (0.020s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 2.67 seconds

```

---

### Log ID: 2 - Subnet Sweep
* **Target Space:** `192.168.8.0/24`
* **Timestamp:** `2026-10-19 18:06:41`
* **Metadata:** `{}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 18:06 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.010s latency).
Nmap scan report for Roku.lan (192.168.8.119)
Host is up (0.037s latency).
Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.011s latency).
Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.086s latency).
Nmap scan report for 192.168.8.183
Host is up (0.039s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 2.68 seconds

```

---

### Log ID: 1 - Wireless & BT Scanner
* **Target Space:** `Local Airspace`
* **Timestamp:** `2026-10-19 18:06:28`
* **Metadata:** `{}`

```text
Executed airspace scan via Termux API/binaries
```

---

