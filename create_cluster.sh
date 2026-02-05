#!/bin/bash

set -e

CONFIG_FILE="kubernetes/config/config.yml"
CLUSTER_NAME="my-k8s"

# Detect OS
if [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/redhat-release ]; then
    OS="redhat"
else
    echo "Unsupported OS"
    exit 1
fi

echo "OS Detected: $OS"

# Install kubectl if not installed
if ! command -v kubectl &> /dev/null
then
    echo "Installing kubectl..."

    if [ "$OS" == "debian" ]; then
        sudo apt update -y
        sudo apt install -y curl
    else
        sudo yum install -y curl
    fi

    cd /tmp
    curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/
    rm -f /tmp/kubectl

    echo "kubectl installed"
else
    echo "kubectl already installed"
fi

# Install kind if not installed
if ! command -v kind &> /dev/null
then
    echo "Installing kind..."

    cd /tmp
    curl -Lo kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64

    chmod +x kind
    sudo mv kind /usr/local/bin/
    rm -f /tmp/kind

    echo "kind installed"
else
    echo "kind already installed"
fi

# Check config file
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

echo "Config file found"

# Check if cluster already exists
if kind get clusters | grep -q "$CLUSTER_NAME"; then
    echo "Cluster already exists"
    exit 0
fi

# Create cluster
echo "Creating kind cluster..."

kind create cluster --name $CLUSTER_NAME --config=$CONFIG_FILE

echo "Cluster created successfully"

