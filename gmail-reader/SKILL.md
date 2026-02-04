---
name: gmail-reader
description: Read, search, and send Gmail emails. Fetch recent emails, search by sender/keyword, summarize important messages, and send new emails.
metadata: {"openclaw":{"emoji":"📧","always":false}}
---

# 📧 Gmail Reader & Sender

Read, search, and send Gmail emails. Fetches recent emails, searches by sender/keyword, summarizes important messages, and sends new emails.

## Features

### 📬 读取功能
- **Read Emails** - Fetch recent emails with preview
- **Search** - Search by sender, keyword, or date
- **Summarize** - Get AI summaries of important emails
- **List** - List emails by sender/category
- **Count** - Get unread count

### ✉️ 发送功能
- **Send Email** - Send emails to any address
- **Quick Send** - Subject + body in command
- **File Mode** - Send body from file
- **HTML Support** - Send HTML formatted emails

## Usage Examples

### 读取邮件

```bash
# Check unread count
python gmail.py --count

# List recent emails
python gmail.py --list --limit 10

# Search by sender
python gmail.py --search --from "github"

# Search by keyword
python gmail.py --search --query "important"

# GitHub notifications only
python gmail.py --github

# Summarize important emails
python gmail.py --summary
```

### 发送邮件

```bash
# Quick send
python gmail.py --send --to "user@example.com" --subject "Hello" --body "Message"

# Send from file
python gmail.py --send --to "user@example.com" --subject "Report" --body-file /path/to/body.txt

# Interactive mode
python gmail.py --send
# Then enter: to, subject, body
```

## Setup

### 1. Enable IMAP in Gmail

1. Go to: https://mail.google.com/mail/settings
2. Click "Forwarding and POP/IMAP"
3. Enable "IMAP access"

### 2. Enable SMTP for Sending

SMTP is enabled automatically when you have IMAP enabled.

### 3. Create App Password (Required!)

Gmail requires an **App Password** for both IMAP and SMTP:

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (required)
3. Create App Password:
   - https://myaccount.google.com/apppasswords
   - Select app: "Mail"
   - Select device: "Other" → "OpenClaw"
4. Copy the 16-character password

### 4. Configure Environment

```bash
export GMAIL_USER="your@gmail.com"
export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

## CLI Options

### Read Options

```bash
python gmail.py [READ_OPTIONS]

Options:
  --count              Show unread email count
  --list               List recent emails
  --limit N            Number of emails (default: 10)
  --search             Search emails
  --from SENDER       Filter by sender
  --query KEYWORD      Search keyword
  --github            GitHub notifications only
  --summary            Summarize important emails
  --output FORMAT     Output: text|json (default: text)
```

### Send Options

```bash
python gmail.py --send [SEND_OPTIONS]

Required:
  --to ADDRESS        Recipient email address
  --subject TEXT       Email subject
  --body TEXT          Email body (or use --body-file)
  --body-file FILE     Read body from file

Examples:
  python gmail.py --send --to "friend@email.com" --subject "Hello!" --body "How are you?"
  
  python gmail.py --send --to "team@company.com" --subject "Weekly Report" --body-file report.txt
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `GMAIL_USER` | Yes | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Yes | 16-char App Password |
| `GMAIL_MAX_EMAILS` | No | Max emails to fetch (default: 20) |

## Integration with OpenClaw

### Heartbeat Checks

```bash
# Check for important emails
python gmail.py --summary
```

### Daily Email Summary Script

```bash
#!/bin/bash
source /root/.openclaw/workspace/lerobot_env/bin/activate
cd /root/.openclaw/workspace/skills/web-publisher/gmail-reader/scripts

echo "=== Gmail Summary ==="
python gmail.py --count
echo ""
python gmail.py --github --limit 5
echo ""
python gmail.py --summary
```

### Send Email Script

```bash
#!/bin/bash
source /root/.openclaw/workspace/lerobot_env/bin/activate
cd /root/.openclaw/workspace/skills/web-publisher/gmail-reader/scripts

# Quick email
python gmail.py --send \
  --to "recipient@example.com" \
  --subject "Daily Report" \
  --body "See attached summary."

# Or interactive
python gmail.py --send
```

## Output Format

### Text Output (Default)

```
📧 Gmail - user@gmail.com
   Unread: 42

Recent Emails:
1. [GitHub] A new SSH key was added
   From: noreply@github.com
   📝 The following SSH key was added...

✅ Email sent successfully!
```

### JSON Output

```json
{
  "unread_count": 42,
  "emails": [
    {
      "title": "Email title",
      "sender": "sender@example.com",
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

- 安全 / security / 密码 / password / SSH / token
- 支付 / payment / invoice / 账单 / 续费
- 警告 / alert / warning / 错误 / critical
- 域名 / domain / 到期

## Performance

| Operation | Time |
|-----------|------|
| Unread count | ~500ms |
| List emails (10) | ~1s |
| Search | ~1s |
| Send email | ~2s |

## Troubleshooting

### "Authentication failed"

1. Enable 2-Step Verification
2. Create App Password (not login password)
3. Use format: `xxxx xxxx xxxx xxxx` (with spaces)

### "SMTP authentication failed"

1. Check that IMAP is enabled
2. Verify App Password is correct
3. Some accounts require "Less secure apps" disabled

### "IMAP disabled"

1. Go to Gmail Settings → Forwarding and POP/IMAP
2. Enable IMAP access
3. Save changes

### "Too many simultaneous connections"

- Gmail limits to 15 IMAP connections
- Wait 30 seconds before retrying

## Dependencies

```bash
# No extra dependencies required!
# Uses: curl, standard Python libraries (smtplib, email, base64)
```

## File Structure

```
gmail-reader/
├── SKILL.md              # This file
├── README.md             # Quick guide
└── scripts/
    ├── gmail.py          # Main CLI tool
    └── __init__.py       # Package init
```

## License

Part of OpenClaw. See LICENSE file.
