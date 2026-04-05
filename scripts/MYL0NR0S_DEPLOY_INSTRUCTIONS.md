# MYL0NR0S.BRAIN Deployment Instructions

## 📦 Deployment Package
**Location:** `/tmp/myl0nr0s_brain_deploy.tar.gz`

## 🚀 Quick Deploy (if SSH works)

```bash
# Run this script
bash /root/.openclaw/workspace/scripts/deploy_brain_myl0nr0s.sh
```

## 🔧 Manual Deploy (if SSH fails)

1. **Download the archive:**
   - From Miles VPS: `/tmp/myl0nr0s_brain_deploy.tar.gz`

2. **Upload to myl0nr0s.cloud:**
   - Use SCP, SFTP, or Hostinger File Manager
   - Upload to `/tmp/` or `/home/openclaw/`

3. **Extract and install:**
   ```bash
   ssh openclaw@myl0nr0s.cloud
   cd /tmp
   tar -xzf myl0nr0s_brain_deploy.tar.gz
   bash remote_setup.sh
   ```

4. **Start the brain:**
   ```bash
   sudo systemctl start aos-waste-receiver
   sudo systemctl status aos-waste-receiver
   ```

## 🧠 What Gets Installed

- `waste_receiver_brain.py` — The receiver brain
- Systemd service `aos-waste-receiver`
- HTTP endpoint on port 7474
- Data directory `/home/openclaw/.aos/waste_data/`

## 📡 API Endpoints

Once running:
- `GET http://myl0nr0s.cloud:7474/status` — Brain status
- `POST http://myl0nr0s.cloud:7474/waste` — Receive waste JSON

## 📧 Integration with Waste Emailer

Miles will email you waste data every 30 minutes. You can:
1. Save the JSON attachment
2. POST it to `http://myl0nr0s.cloud:7474/waste`
3. Or set up automatic forwarding

## 🔄 Update Miles' Config

To send waste directly to myl0nr0s instead of email:

```bash
# On Miles VPS, update the waste emailer
export WASTE_ENDPOINT="http://myl0nr0s.cloud:7474/waste"
```

## 📊 Monitoring

```bash
# Check service status
sudo systemctl status aos-waste-receiver

# View logs
journalctl -u aos-waste-receiver -f

# Check brain status
curl http://localhost:7474/status
```
