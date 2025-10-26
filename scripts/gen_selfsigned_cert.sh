#!/bin/bash
# Generate self-signed TLS certificates for local HTTPS development

echo "Generating self-signed certificate for BaraChat..."

# Create certs directory if it doesn't exist
mkdir -p certs

# Generate certificate
openssl req -x509 -newkey rsa:4096 -nodes \
    -keyout certs/key.pem \
    -out certs/cert.pem \
    -days 365 \
    -subj "/C=US/ST=State/L=City/O=BaraChat/CN=localhost"

echo "Certificate generated successfully!"
echo "Files:"
echo "  - certs/cert.pem (certificate)"
echo "  - certs/key.pem (private key)"
echo ""
echo "Update your server config to use:"
echo "  cert_file=certs/cert.pem"
echo "  key_file=certs/key.pem"

