---
name: gmail-reader
description: Read, search, and manage Gmail emails. Fetch recent emails, search by sender/keyword, and summarize important messages.
metadata: {"openclaw":{"emoji":"📧","always":false}}
---

# 📧 Gmail Reader

Read, search, and manage Gmail emails. Fetches recent emails, searches by sender/keyword, and summarizes important messages.

## Features

- **Read Emails** - Fetch recent emails with preview
- **Search** - Search by sender, keyword, or date
- **Summarize** - Get AI summaries of important emails
- **List** - List emails by sender/category
- **Count** - Get unread count

## Usage Examples

```bash
# Check unread count
"Check my Gmail unread count"

# List recent emails
"Show my recent 10 emails"

# Search by sender
"Show me emails from GitHub"

# Search by keyword
"Find emails about OpenClaw"

# List all GitHub emails
"List all GitHub notifications"

# Get important emails
"Show me important emails from this week"
```

## Setup

### 1. Enable IMAP in Gmail

1. Go to: https://mail.google.com/mail/settings
2. Click "Forwarding and POP/IMAP"
3. Enable "IMAP access"

### 2. Create App Password (Required!)

Gmail requires an **App Password**, not your login password:

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (required)
3. Create App Password:
   - https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → "OpenClaw"
4. Copy the 16-character password

### 3. Configure Environment

```bash
# Set credentials (only for current session)
export GMAIL_USER="your@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

## Configuration

The skill reads credentials from environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GMAIL_USER` | Yes | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Yes | 16-char App Password |
| `GMAIL_MAX_EMAILS` | No | Max emails to fetch (default: 20) |

## CLI Usage

### Basic Commands

```bash
source /root/.openclaw/workspace/lerobot_env/bin/activate
cd /root/.openclaw/workspace/skills/gmail-reader/scripts

# Check unread count
python gmail.py --count

# List recent emails
python gmail.py --list --limit 10

# Search by sender
python gmail.py --search --from "github.com"

# Search by keyword
python gmail.py --search --query "OpenClaw"

# Get recent GitHub emails
python gmail.py --github

# Get summary of recent emails
python gmail.py --summary
```

### All Options

```bash
python gmail.py [OPTIONS]

Options:
  --count              Show unread email count
  --list               List recent emails
  --limit N            Number of emails (default: 10)
  --search             Search emails
  --from SENDER        Filter by sender
  --query KEYWORD      Search keyword
  --since DATE         Emails after date (YYYY-MM-DD)
  --summary            Summarize recent emails
  --github             Show GitHub notifications only
  --output FORMAT      Output format: text|json (default: text)
  --help               Show help
```

## Integration with OpenClaw

### Heartbeat Checks

Add to your heartbeat routine:

```bash
# Check for important emails
python gmail.py --summary
```

### Example: Daily Email Summary

```bash
# Daily summary script
#!/bin/bash
source /root/.openclaw/workspace/lerobot_env/bin/activate
cd /root/.openclaw/workspace/skills/gmail-reader/scripts

echo "=== Gmail Summary ==="
python gmail.py --count
echo ""
python gmail.py --github --limit 5
echo ""
echo "=== Done ==="
```

## Output Format

### Text Output (Default)

```
📧 Gmail - Inbox for user@gmail.com
Unread: 42

Recent Emails:
1. [GitHub] A new SSH key was added
   From: noreply@github.com
   Date: 2024-01-15
   Preview: The following SSH key was added...

2. [重要] 阿里云域名过期通知
   From: system@notice.aliyun.com
   Date: 2024-01-14
   Preview: 您的域名即将过期...
```

### JSON Output

```json
{
  "user": "user@gmail.com",
  "unread_count": 42,
  "emails": [
    {
      "title": "Email title",
      "sender": "sender@example.com",
      "date": "2024-01-15",
      "summary": "Email preview..."
    }
  ]
}
```

## Important Email Detection

The skill automatically flags important emails:

| Tag | Meaning |
|-----|---------|
| 🔴 高优先级 | 域名过期、安全警报、支付问题 |
| 🟡 中优先级 | GitHub 通知、服务器状态 |
| 🟢 低优先级 | 产品更新、营销邮件 |

### Keywords for Important Detection

- 域名过期 / domain / 到期
- 安全 / security / 密码 / password
- 支付 / payment / invoice / 账单
- SSH / token / key
- 警告 / alert / warning

## Rate Limiting

- Gmail IMAP: ~500 emails/day
- Atom Feed: Unlimited reads (no auth needed for count)
- Recommended: Cache results for 5-10 minutes

## Troubleshooting

### "Authentication failed"

1. Enable 2-Step Verification
2. Create App Password (not login password)
3. Use format: `xxxx xxxx xxxx xxxx` (with spaces)

### "IMAP disabled"

1. Go to Gmail Settings → Forwarding and POP/IMAP
2. Enable IMAP access
3. Save changes

### "Too many simultaneous connections"

- Gmail limits to 15 IMAP connections
- Wait 30 seconds before retrying

### Emails not showing

- Atom feed only shows unread emails
- Mark emails as unread to appear in feed

## Security Notes

- 🔐 Never commit real credentials
- Use environment variables only
- App Password is separate from login password
- Token grants access to read emails only

## API Reference

### Python Module

```python
from gmail import GmailReader

# Initialize
gmail = GmailReader(
    user="user@gmail.com",
    password="xxxx xxxx xxxx xxxx"
)

# Get unread count
count = gmail.get_unread_count()

# List emails
emails = gmail.list_emails(limit=10)

# Search
results = gmail.search(sender="github.com")

# Get GitHub notifications
gh_emails = gmail.get_github_emails()

# Summarize
summary = gmail.summarize(limit=5)
```

### GmailReader Class

| Method | Description |
|--------|-------------|
| `get_unread_count()` | Get unread email count |
| `list_emails(limit)` | List recent emails |
| `search(query, sender, since)` | Search emails |
| `get_github_emails()` | Get GitHub notifications |
| `summarize(limit)` | Summarize recent emails |
| `mark_as_read(msgid)` | Mark email as read (via Gmail API) |

## Performance

| Operation | Time |
|-----------|------|
| Unread count | ~500ms |
| List emails (10) | ~1s |
| Search | ~1s |
| Summary | ~2s |

## Dependencies

```bash
# No extra dependencies required!
# Uses: curl, standard Python libraries
```

## File Structure

```
gmail-reader/
├── SKILL.md              # This file
├── README.md             # Quick guide
└── scripts/
    ├── gmail.py          # Main CLI tool
    ├── __init__.py       # Package init
    └── config.py         # Config handling
```

## License

Part of OpenClaw. See LICENSE file.
