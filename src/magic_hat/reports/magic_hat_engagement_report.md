# Magic Hat Security Engagement Report

**Total Records Captured:** 1

---

## Executive Summary
This report aggregates telemetry, host discoveries, and service scans executed during the tactical engagement.

---

## Detailed Scan Telemetry Logs

### Log ID: 1 - Nmap Deep Recon
* **Target Space:** `192.168.8.1`
* **Timestamp:** `2026-10-23 21:21:07`
* **Metadata:** `{"open_ports": [{"port": "53/tcp", "service": "domain", "details": "80/tcp   open  http"}, {"port": "443/tcp", "service": "https", "details": "445/tcp  open  microsoft-ds"}, {"port": "2222/tcp", "service": "EtherNetIP-1", "details": "8080/tcp open  http-proxy"}, {"port": "8443/tcp", "service": "https-alt", "details": "Nmap done: 1 IP address (1 host up) scanned in 38.15 seconds"}], "os_guess": "Unknown / Not Detected", "mac_address": "Unknown", "device_type": "Unknown"}`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-23 14:20 -0700
Nmap scan report for console.gl-inet.com (192.168.8.1)
Host is up (0.0016s latency).
Not shown: 993 closed tcp ports (conn-refused)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
445/tcp  open  microsoft-ds
2222/tcp open  EtherNetIP-1
8080/tcp open  http-proxy
8443/tcp open  https-alt

Nmap done: 1 IP address (1 host up) scanned in 38.15 seconds

```

---

