#!/bin/bash

# Lab 7-P1 Quick Setup Script
# CSC323 Information Security

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Lab 7-P1: DNS Tunneling Setup                           ║"
echo "║  CSC323 Information Security                              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}[1/4] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3 not found!${NC}"
    echo "Install with: sudo apt install python3 python3-pip"
    exit 1
fi

# Check pip
echo -e "\n${YELLOW}[2/4] Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${RED}✗ pip3 not found!${NC}"
    echo "Install with: sudo apt install python3-pip"
    exit 1
fi

# Install requirements
echo -e "\n${YELLOW}[3/4] Installing Python dependencies...${NC}"
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Installation failed${NC}"
    exit 1
fi

# Verify crypto
echo -e "\n${YELLOW}[4/4] Verifying cryptography library...${NC}"
python3 -c "from Crypto.PublicKey import RSA; from Crypto.Cipher import AES; print('OK')" &> /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cryptography library working${NC}"
else
    echo -e "${RED}✗ Cryptography library not working${NC}"
    echo "Try: pip3 install --upgrade pycryptodome"
    exit 1
fi

# Success
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  SETUP COMPLETE!                                         ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Quick Start:"
echo ""
echo "  Full Demonstration:"
echo "    python3 dns_tunnel_simple.py demo"
echo ""
echo "  Server Mode (Attacker):"
echo "    python3 dns_tunnel_simple.py server"
echo ""
echo "  Client Mode (Target):"
echo "    python3 dns_tunnel_simple.py client"
echo ""
echo "For detailed instructions, see LAB7_SETUP_GUIDE.md"
echo ""
