"""
Generate client certificates for AOS Brain connection
"""

from datetime import datetime, timedelta
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_client_cert(cert_dir: Path, client_name: str) -> None:
    """Generate client certificate signed by CA."""
    
    # Load CA
    ca_cert_path = cert_dir / "ca_cert.pem"
    ca_key_path = cert_dir / "ca_key.pem"
    
    if not ca_cert_path.exists():
        raise FileNotFoundError("CA certificate not found. Run secure_bridge.py first.")
    
    ca_cert = x509.load_pem_x509_certificate(ca_cert_path.read_bytes())
    ca_key = serialization.load_pem_private_key(ca_key_path.read_bytes(), password=None)
    
    # Generate client key
    client_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    
    # Create client certificate
    subject = x509.Name([
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, "Performance Supply Depot"),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, client_name),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        client_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=30)  # Client certs valid 30 days
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            key_cert_sign=False,
            crl_sign=False,
            content_commitment=True,
            key_encipherment=True,
            data_encipherment=False,
            key_agreement=False,
            encipher_only=False,
            decipher_only=False
        ),
        critical=True
    ).sign(ca_key, hashes.SHA256())
    
    # Save
    cert_path = cert_dir / f"{client_name}_cert.pem"
    key_path = cert_dir / f"{client_name}_key.pem"
    
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(client_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))
    
    print(f"Generated client certificate: {cert_path}")


if __name__ == "__main__":
    import sys
    
    cert_dir = Path(__file__).parent.parent / "certs"
    client_name = sys.argv[1] if len(sys.argv) > 1 else "aos_brain_client"
    
    generate_client_cert(cert_dir, client_name)
