# 📧 Gmail Reader Skill

Quick start guide for Gmail Reader skill.

## Setup

```bash
# 1. Enable IMAP in Gmail
#    https://mail.google.com/mail/settings → Forwarding and POP/IMAP → Enable IMAP

# 2. Create App Password
#    https://myaccount.google.com/apppasswords
#    Select: Mail → Other → "OpenClaw"

# 3. Set environment variables
export GMAIL_USER="your@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

## Quick Commands

```bash
cd /root/.openclaw/workspace/skills/gmail-reader/scripts

# Check unread count
python gmail.py --count

# List recent emails (10)
python gmail.py --list

# List 20 emails
python gmail.py --list --limit 20

# Search by sender
python gmail.py --search --from "github"

# GitHub notifications only
python gmail.py --github

# Summarize important emails
python gmail.py --summary

# JSON output
python gmail.py --list --output json
```

## Examples

```bash
# Daily summary
echo "=== Gmail Summary ==="
python gmail.py --count
python gmail.py --github --limit 5

# Check for important emails
python gmail.py --summary
```

## See Also

- [SKILL.md](./SKILL.md) - Full documentation
