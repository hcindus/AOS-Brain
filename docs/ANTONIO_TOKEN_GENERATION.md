# Generate New GitHub Token for antoniohudnall-eng
**Required:** To push psdepot-landing repository

---

## Step 1: Log into GitHub as antoniohudnall-eng
Go to: https://github.com/login

## Step 2: Navigate to Token Settings
Go to: https://github.com/settings/tokens

## Step 3: Generate New Token
1. Click "Generate new token (classic)"
2. Token name: `Miles-VPS-Access`
3. Expiration: 90 days (or No expiration)
4. Scopes to select:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)

## Step 4: Copy Token
Copy the generated token (starts with `ghp_`)

## Step 5: Store on VPS
Run this command on the VPS:

```bash
echo "ANTONIO_GITHUB_TOKEN=ghp_YOUR_TOKEN_HERE" > /root/.openclaw/workspace/aocros/secrets/antonio_github_token.env
chmod 600 /root/.openclaw/workspace/aocros/secrets/antonio_github_token.env
```

## Step 6: Configure Git
Then run these commands:

```bash
echo "https://ghp_YOUR_TOKEN_HERE@github.com" > ~/.git-credentials-antonio
chmod 600 ~/.git-credentials-antonio
cd /root/.openclaw/workspace/psdepot-landing
git remote set-url origin https://ghp_YOUR_TOKEN_HERE@github.com/antoniohudnall-eng/psdepot-landing.git
git push origin master
```

---

**Alternative:** If you provide the token now, I can execute all these steps automatically.
