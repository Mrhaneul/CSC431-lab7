# Lab 7-P1: DNS Tunneling Firewall Bypass
## CSC323 Information Security

---

## 📋 Lab Overview

This lab demonstrates a **firewall bypass attack** using DNS tunneling with RSA encryption.

### Scenario
- **Environment**: Network with firewall blocking non-standard ports
- **Firewall**: Allows HTTP and DNS traffic, inspects packets
- **Attacker**: Outside network, sets up malicious DNS server
- **Target**: Employee inside network, tricked via social engineering
- **Method**: Exfiltrate data through allowed DNS queries

---

## 🚀 Quick Start

### Step 1: Setup

```bash
# Install dependencies
pip3 install pycryptodome

# Or use the setup script
chmod +x setup_lab7.sh
./setup_lab7.sh
```

### Step 2: Run Demonstration

```bash
# Run complete attack simulation
python3 dns_tunnel_simple.py demo
```

This will:
1. Generate RSA encryption keys
2. Simulate social engineering attack
3. Exfiltrate sample sensitive data
4. Decrypt on attacker's side
5. Generate attack report

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `dns_tunnel_simple.py` | **Main implementation** - Easy to test in VM |
| `dns_tunnel.py` | Advanced version - Uses real DNS protocol |
| `LAB7_SETUP_GUIDE.md` | **Complete setup and testing guide** |
| `requirements.txt` | Python dependencies |
| `setup_lab7.sh` | Automated setup script |

---

## 🎯 Three Ways to Run

### Method 1: Full Demo (Recommended First)
```bash
python3 dns_tunnel_simple.py demo
```
- Automatic simulation of complete attack
- Shows all phases: setup, exfiltration, decryption
- Generates logs and summary report
- Best for understanding the attack flow

### Method 2: Interactive Mode

**Terminal 1 - Server (Attacker):**
```bash
python3 dns_tunnel_simple.py server
```

**Terminal 2 - Client (Target Employee):**
```bash
python3 dns_tunnel_simple.py client
# Then enter data to exfiltrate
Data> secret_password_123
```

### Method 3: Advanced (Real DNS)

```bash
# Requires sudo for port 53
sudo python3 dns_tunnel.py server

# In another terminal
python3 dns_tunnel.py client --server localhost --data "sensitive_data"
```

---

## 🔑 Key Concepts Demonstrated

### 1. DNS Tunneling
- Exfiltrates data via DNS queries
- Bypasses firewall that allows DNS
- Legitimate DNS traffic hides malicious payload

### 2. Hybrid Encryption
- **RSA-2048**: For key exchange
- **AES-256**: For data encryption
- Combines security of both algorithms

### 3. Social Engineering
- Fake LinkedIn profile builds trust
- Target unknowingly runs malicious client
- Demonstrates human factor in security

### 4. Firewall Bypass
- Exploits firewall allowing DNS
- Encrypted payload prevents inspection
- Demonstrates defense limitations

---

## 📊 What Gets Exfiltrated

Example sensitive data the lab demonstrates:
```
• Usernames and passwords
• Credit card information
• Social security numbers
• Confidential file locations
• Database credentials
• Session tokens
• API keys
```

---

## 📝 Lab Report Requirements

### Must Include:

1. **Screenshots** (10 required)
   - VM setup
   - Server generating keys
   - Client encrypting data
   - Server decrypting data
   - Log files
   - Attack summary

2. **Code Execution**
   - Successfully run demo mode
   - Generate attack logs
   - Create summary report

3. **Analysis**
   - Why attack succeeds
   - Firewall limitations
   - Mitigation strategies
   - Real-world implications

4. **Documentation**
   - 8-12 page report
   - Technical explanations
   - Defense recommendations

---

## 🛡️ Defense Strategies

The lab teaches these defenses:

1. **DNS Monitoring**
   - Detect unusual query patterns
   - Flag long subdomains
   - Monitor query frequency

2. **DNS Filtering**
   - Whitelist approved DNS servers
   - Block suspicious domains
   - Inspect query content

3. **Behavioral Analysis**
   - Detect anomalous DNS usage
   - Monitor data volumes
   - Alert on encryption patterns

4. **Policy Controls**
   - Restrict DNS servers
   - Require encrypted DNS with inspection
   - Implement egress filtering

---

## 🔍 Log Files Generated

After running, you'll have:

```
logs/
└── firewall_bypass.log          # Detailed event timeline

dns_tunnel_shared/
├── public_key.pem                # RSA public key
├── exfil_*.dns                  # Encrypted DNS queries
└── exfil_*.processed            # Processed queries

attack_summary.json               # Complete attack report
```

---

## ⚠️ Important Notes

### Safety
- **USE ONLY IN ISOLATED VMs**
- **NEVER on production networks**
- **Educational purposes only**
- Disable VM network if concerned

### Requirements
- Python 3.8 or higher
- pycryptodome library
- 2GB RAM minimum
- Ubuntu 22.04 or Windows 10/11

### Permissions
- Simplified version: No special permissions needed
- Advanced version: Requires sudo/admin for port 53

---

## 🐛 Troubleshooting

### "No module named 'Crypto'"
```bash
pip3 install pycryptodome
# NOT pycrypto (that's outdated)
```

### "Public key not found"
```bash
# Run server first to generate keys
python3 dns_tunnel_simple.py server
# Then run client in another terminal
```

### "Permission denied" (Port 53)
```bash
# Use simplified version (recommended)
python3 dns_tunnel_simple.py demo

# Or use sudo for advanced version
sudo python3 dns_tunnel.py server
```

---

## 📖 Full Documentation

For complete setup instructions, VM configuration, and detailed testing procedures, see:

**→ LAB7_SETUP_GUIDE.md**

This 18-page guide includes:
- Complete VM setup
- Step-by-step walkthrough
- Testing scenarios
- Log analysis
- Report structure
- Grading rubric

---

## ✅ Quick Checklist

Before starting:
- [ ] VM set up (Ubuntu or Windows)
- [ ] Python 3.8+ installed
- [ ] pycryptodome installed
- [ ] Files downloaded
- [ ] Read scenario above

To complete lab:
- [ ] Run demo mode successfully
- [ ] Understand each phase
- [ ] Capture 10 screenshots
- [ ] Analyze log files
- [ ] Write mitigation strategies
- [ ] Complete lab report

---

## 🎓 Learning Objectives

After completing this lab, you will understand:

✅ How DNS tunneling bypasses firewalls  
✅ Why allowed services can be exploited  
✅ How encryption hides malicious payloads  
✅ The role of social engineering in attacks  
✅ Limitations of perimeter-based security  
✅ How to detect and prevent DNS tunneling  
✅ Importance of defense-in-depth  

---

## 🤝 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review LAB7_SETUP_GUIDE.md (comprehensive guide)
3. Verify Python and library versions
4. Check log files for error details

---

## 📄 License

This lab is for educational purposes as part of CSC323 Information Security course at California Baptist University.

**Created by:** Haneul (CSC323 Student)  
**Course:** Information Security  
**Lab:** 7-P1 - DNS Tunneling Firewall Bypass  

---

**Good luck with your lab! 🚀**
