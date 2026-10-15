# Magic Hat Intelligence Report
**Generated:** 2026-10-15 11:34:26
**Total Records Exported:** 7

---

## Tool: Nmap
* **Target / Interface:** `192.168.8.139`
* **Timestamp:** `2026-10-15 11:34:08`
* **Log ID:** `7`

```text
Starting Nmap 7.99 ( https://nmap.org ) at 2026-10-15 11:34 -0700
Nmap scan report for Brandon-s-A16.lan (192.168.8.139)
Host is up (0.0037s latency).
All 100 scanned ports on Brandon-s-A16.lan (192.168.8.139) are in ignored states.
Not shown: 100 closed tcp ports (conn-refused)

Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds

```

---

## Tool: Tech Fingerprint
* **Target / Interface:** `https://www.metrohospitality.com/`
* **Timestamp:** `2026-10-15 11:33:08`
* **Log ID:** `6`

```text
ERROR: <internal:/data/data/com.termux/files/usr/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb>:136:in 'Kernel#require': cannot load such file -- lib/whatweb (LoadError)
	from <internal:/data/data/com.termux/files/usr/lib/ruby/3.4.0/rubygems/core_ext/kernel_require.rb>:136:in 'Kernel#require'
	from /data/data/com.termux/files/usr/bin/whatweb:59:in '<main>'

```

---

## Tool: DNS Recon
* **Target / Interface:** `https://www.metrohospitality.com/`
* **Timestamp:** `2026-10-15 11:32:42`
* **Log ID:** `5`

```text
ERROR: Command '['dig', 'https://www.metrohospitality.com/', 'AXFR']' returned non-zero exit status 9.
```

---

## Tool: DNS Recon
* **Target / Interface:** `https://www.metrohospitality.com/`
* **Timestamp:** `2026-10-15 11:31:46`
* **Log ID:** `4`

```text
ERROR: Command '['dig', 'https://www.metrohospitality.com/', 'ANY']' returned non-zero exit status 9.
```

---

## Tool: DNS Recon
* **Target / Interface:** `https://www.metrohospitality.com/`
* **Timestamp:** `2026-10-15 11:30:28`
* **Log ID:** `3`

```text

; <<>> DiG 9.20.24 <<>> https://www.metrohospitality.com/
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 29111
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;https://www.metrohospitality.com/. IN	A

;; AUTHORITY SECTION:
.			900	IN	SOA	a.root-servers.net. nstld.verisign-grs.com. 2026101500 1800 900 604800 86400

;; Query time: 28 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
;; WHEN: Thu Oct 15 11:30:28 MST 2026
;; MSG SIZE  rcvd: 137


```

---

## Tool: Web Fuzzer
* **Target / Interface:** `https://www.metrohospitality.com/FUZZ`
* **Timestamp:** `2026-10-15 11:29:59`
* **Log ID:** `2`

```text
ERROR: Encountered error(s): 1 errors occured.
	* stat /data/data/com.termux/files/home/Magic_Hat/src/magic_hat/common.txt: no such file or directory

Encountered error(s): 1 errors occured.
	* stat /data/data/com.termux/files/home/Magic_Hat/src/magic_hat/common.txt: no such file or directory


```

---

## Tool: Net Shark
* **Target / Interface:** `rmnet0`
* **Timestamp:** `2026-10-15 11:28:56`
* **Log ID:** `1`

```text
ERROR: Capturing on 'rmnet0'
tshark: The capture session could not be initiated on capture device "rmnet0".
(rmnet0: SIOCETHTOOL(ETHTOOL_GET_TS_INFO) ioctl failed: Permission denied)
Please check that you have the proper interface or pipe specified.
0 packets captured

```

---
