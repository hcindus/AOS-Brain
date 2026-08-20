import imaplib, os
for line in open('/root/.openclaw/workspace/aocros/secrets/smtp.env'):
    line = line.strip()
    if line.startswith('#') or '=' not in line: continue
    if line.startswith('export '): line = line[7:]
    k, v = line.split('=', 1)
    os.environ[k] = v.strip().strip('"').strip("'")

def conn():
    M = imaplib.IMAP4_SSL(os.environ['HOSTINGER_IMAP_SERVER'], int(os.environ['HOSTINGER_IMAP_PORT']))
    M.login(os.environ['HOSTINGER_SMTP_USER'], os.environ['HOSTINGER_SMTP_PASS'])
    return M

M = conn()
M.select('INBOX')

# ensure Archive folder
typ, folders = M.list()
if not any(b'Archive' in f for f in folders):
    M.create('Archive')
    print("created Archive")

# chunked bulk helper
def apply_chunked(ids, fn_copy, fn_del):
    chunk = 400
    for i in range(0, len(ids), chunk):
        sub = ids[i:i+chunk]
        msgset = ','.join(sub)
        fn_copy(msgset)
        fn_del(msgset)

# 1. delete mailer-daemon bounces
typ, d = M.search(None, 'FROM', '"mailer-daemon"')
bounces = [x.decode() for x in d[0].split()] if d[0] else []
print(f"bounces to delete: {len(bounces)}")
for i in range(0, len(bounces), 400):
    msgset = ','.join(bounces[i:i+400])
    M.store(msgset, '+FLAGS', '\\Deleted')

# 2. archive messages older than 30 days
typ, d = M.search(None, 'BEFORE', '21-Jul-2026')
old = [x.decode() for x in d[0].split()] if d[0] else []
print(f"old messages to archive: {len(old)}")
for i in range(0, len(old), 400):
    msgset = ','.join(old[i:i+400])
    M.copy(msgset, 'Archive')
    M.store(msgset, '+FLAGS', '\\Deleted')

M.expunge()
M.logout()
print("DONE cleanup")

# recount
M = conn()
M.select('INBOX')
t, d = M.search(None, 'ALL')
print("INBOX remaining:", len(d[0].split()))
M.select('Archive')
t, d = M.search(None, 'ALL')
print("ARCHIVE:", len(d[0].split()))
M.logout()
