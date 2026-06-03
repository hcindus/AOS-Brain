# 🛡️ Sentinel Shield

> Enterprise Authentication with Real-Time Threat Detection

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Node Version](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)

Sentinel Shield is the only open-source authentication platform with **built-in real-time threat detection**. Self-hosted, zero licensing fees, superior security to Auth0 and Okta.

![Sentinel Shield](https://psdepot.com/sentinel-shield/hero.png)

## ✨ Features

- 🔒 **Argon2id + Pepper** - Superior password hashing (better than bcrypt)
- 🛡️ **Sentinel-Dusty Guardian** - Real-time threat detection and monitoring
- 🔐 **Multi-Factor Authentication** - TOTP-based MFA
- 🌐 **Social Auth** - Google, Microsoft, Apple OAuth
- 📊 **Admin Dashboard** - Beautiful React-based management
- 📝 **Audit Logging** - Complete compliance trail
- ⚡ **5-Minute Deploy** - Docker ready

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/psdepot/sentinel-shield.git
cd sentinel-shield

# Deploy
docker-compose up -d

# Access
open http://localhost:3001/admin
```

[📖 Full Documentation](https://psdepot.com/sentinel-shield/docs/QUICKSTART.md)

## 📊 vs Competitors

| Feature | Sentinel | Auth0 | Okta |
|---------|----------|-------|------|
| **Price** | $0 | $23K+/yr | $24K+/yr |
| **Password Hashing** | Argon2id + Pepper | bcrypt | bcrypt |
| **Breach Detection** | ✅ Built-in | $ Add-on | ❌ |
| **Real-time Monitoring** | ✅ Sentinel-Dusty | ❌ | ❌ |
| **Source Code** | ✅ Full ownership | ❌ SaaS | ❌ SaaS |
| **Vendor Lock-in** | ✅ None | ❌ High | ❌ High |

## 🛠️ Installation

### Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  sentinel:
    image: psdepot/sentinel-shield:latest
    ports:
      - "3001:3001"
    environment:
      - JWT_ACCESS_SECRET=your-secret
      - JWT_REFRESH_SECRET=your-refresh-secret
```

### Kubernetes

```bash
kubectl apply -f https://raw.githubusercontent.com/psdepot/sentinel-shield/main/k8s/
```

### Traditional

```bash
npm install
npm start
```

## 🔒 Security

- **Password Hashing:** Argon2id with pepper
- **Token Security:** RS256 JWT with refresh rotation
- **Rate Limiting:** Configurable per endpoint
- **CSRF Protection:** Double-submit cookie pattern
- **Breach Detection:** Have I Been Pwned API integration
- **Account Lockout:** After 5 failed attempts
- **Session Security:** Device fingerprinting

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [User Guide](docs/HUMAN_GUIDE.md)
- [Developer Integration](docs/AGENT_GUIDE.md)
- [API Reference](https://psdepot.com/sentinel-shield/api.yaml)

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 💼 Commercial Support

- **Community:** Free, self-supported
- **Professional:** $499/mo - Priority support, SLA
- **Enterprise:** Custom - Dedicated support, custom features

[Contact Sales](mailto:sales@psdepot.com)

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

Made with ❤️ by Performance Supply Depot

[🌐 Website](https://psdepot.com/sentinel-shield) · [📖 Docs](https://psdepot.com/sentinel-shield/docs) · [💬 Discord](https://discord.gg/sentinel-shield)
