#!/usr/bin/env python3
"""
Gmail Reader - Read, search, and send Gmail emails

Usage:
    # 读取邮件
    python gmail.py --count                    # Show unread count
    python gmail.py --list --limit 10          # List recent emails
    python gmail.py --search --from "github"   # Search by sender
    python gmail.py --github                   # GitHub notifications only
    python gmail.py --summary                  # Summarize important emails
    
    # 发送邮件
    python gmail.py --send --to "user@example.com" --subject "Hello" --body "Message"
"""

import os
import sys
import smtplib
import base64
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from email.utils import parsedate_to_datetime
import json

# Configuration
DEFAULT_LIMIT = 10

# Important email keywords
IMPORTANT_KEYWORDS = [
    '安全', 'security', 'password', '密码', 'ssh', 'token', 'key',
    'credential', '登录', 'unauthorized',
    '支付', 'payment', 'invoice', '账单', '欠费', 'overdue',
    '续费', 'renew', 'expire', '过期',
    '警告', 'alert', 'warning', '错误', 'error', 'critical',
    '紧急', 'urgent', 'important',
    '域名', 'domain', '到期',
]


class GmailSender:
    """Gmail sender with SMTP"""
    
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
    
    def send(self, to_email, subject, body):
        """Send email"""
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = formataddr(("Brad", self.user))
        msg['To'] = to_email
        msg['Subject'] = subject
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.user, [to_email], msg.as_string())
            server.quit()
            return True, "邮件发送成功！"
        except Exception as e:
            return False, f"发送失败: {e}"


class GmailReader:
    """Gmail reader with IMAP"""
    
    def __init__(self, user=None, password=None):
        self.user = user or os.environ.get('GMAIL_USER')
        self.password = password or os.environ.get('GMAIL_APP_PASSWORD')
        self.max_emails = int(os.environ.get('GMAIL_MAX_EMAILS', '20'))
        
        if not self.user or not self.password:
            raise ValueError(
                "GMAIL_USER and GMAIL_APP_PASSWORD must be set!"
            )
    
    def _fetch_feed(self):
        """Fetch Gmail Atom feed"""
        auth = f"{self.user}:{self.password}"
        url = "https://mail.google.com/mail/feed/atom"
        
        req = urllib.request.Request(url)
        auth_header = f'Basic {base64.b64encode(auth.encode()).decode()}'
        req.add_header('Authorization', auth_header)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            raise ConnectionError(f"Failed to fetch Gmail: {e}")
    
    def _parse_feed(self, xml_content):
        """Parse Atom feed and extract emails"""
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse feed: {e}")
        
        emails = []
        
        for entry in root.findall('.//{http://purl.org/atom/ns#}entry'):
            email = {
                'title': '',
                'sender': '',
                'date': '',
                'summary': '',
                'link': '',
            }
            
            title_elem = entry.find('.//{http://purl.org/atom/ns#}title')
            if title_elem is not None and title_elem.text:
                email['title'] = title_elem.text.strip()
            
            author_elem = entry.find('.//{http://purl.org/atom/ns#}author/{http://purl.org/atom/ns#}email')
            if author_elem is not None and author_elem.text:
                email['sender'] = author_elem.text.strip()
            
            summary_elem = entry.find('.//{http://purl.org/atom/ns#}summary')
            if summary_elem is not None and summary_elem.text:
                summary = ' '.join(summary_elem.text.strip().split())
                if len(summary) > 300:
                    summary = summary[:300] + '...'
                email['summary'] = summary
            
            emails.append(email)
        
        return emails
    
    def _is_important(self, email):
        """Check if email is important"""
        text = f"{email['title']} {email['summary']}".lower()
        for keyword in IMPORTANT_KEYWORDS:
            if keyword.lower() in text:
                return True
        return False
    
    def get_unread_count(self):
        """Get unread email count"""
        feed = self._fetch_feed()
        root = ET.fromstring(feed)
        count_elem = root.find('.//{http://purl.org/atom/ns#}fullcount')
        if count_elem is not None and count_elem.text:
            return int(count_elem.text)
        return 0
    
    def list_emails(self, limit=DEFAULT_LIMIT):
        """List recent emails"""
        feed = self._fetch_feed()
        emails = self._parse_feed(feed)
        return emails[:limit]
    
    def search(self, query=None, sender=None):
        """Search emails"""
        emails = self.list_emails(limit=self.max_emails)
        
        if query:
            query = query.lower()
            emails = [e for e in emails if query in e['title'].lower() or query in e['summary'].lower()]
        
        if sender:
            sender = sender.lower()
            emails = [e for e in emails if sender in e['sender'].lower()]
        
        return emails
    
    def get_github_emails(self):
        """Get GitHub notifications"""
        return self.search(sender='github')
    
    def summarize(self, limit=10):
        """Summarize important emails"""
        emails = self.list_emails(limit=limit)
        
        summary = {
            'total': len(emails),
            'important': [],
            'normal': [],
        }
        
        for email in emails:
            if self._is_important(email):
                summary['important'].append(email)
            else:
                summary['normal'].append(email)
        
        return summary


def format_email_list(emails, show_summary=True):
    """Format email list for display"""
    if not emails:
        return "No emails found.\n"
    
    lines = []
    for i, email in enumerate(emails, 1):
        title = email['title'][:50] if len(email['title']) > 50 else email['title']
        lines.append(f"{i}. [{email['sender'][:30]}]")
        lines.append(f"   {title}")
        if show_summary and email['summary']:
            summary = email['summary'][:100]
            lines.append(f"   📝 {summary}")
        lines.append('')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='📧 Gmail Reader & Sender',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # 读取相关
    parser.add_argument('--count', action='store_true', help='Show unread count')
    parser.add_argument('--list', action='store_true', help='List recent emails')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT, help='Number of emails')
    parser.add_argument('--search', action='store_true', help='Search emails')
    parser.add_argument('--from', dest='sender', help='Filter by sender')
    parser.add_argument('--query', help='Search keyword')
    parser.add_argument('--github', action='store_true', help='GitHub notifications only')
    parser.add_argument('--summary', action='store_true', help='Summarize important emails')
    
    # 发送相关
    parser.add_argument('--send', action='store_true', help='Send email')
    parser.add_argument('--to', help='Recipient email')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body')
    parser.add_argument('--body-file', help='Read body from file')
    
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    try:
        # 发送邮件模式
        if args.send:
            if not args.to:
                print("❌ 需要指定收件人: --to user@example.com")
                sys.exit(1)
            
            subject = args.subject or ""
            body = ""
            
            if args.body:
                body = args.body
            elif args.body_file and os.path.exists(args.body_file):
                with open(args.body_file, 'r') as f:
                    body = f.read()
            elif not args.body:
                body = "(空邮件)"
            
            sender = GmailSender(
                os.environ.get('GMAIL_USER'),
                os.environ.get('GMAIL_APP_PASSWORD')
            )
            success, msg = sender.send(args.to, subject, body)
            
            if args.output == 'json':
                print(json.dumps({'success': success, 'message': msg}))
            else:
                print(f"{'✅' if success else '❌'} {msg}")
            sys.exit(0)
        
        # 读取邮件模式
        gmail = GmailReader()
        
        if not any([args.count, args.list, args.search, args.github, args.summary]):
            args.count = True
            args.list = True
        
        if args.count:
            count = gmail.get_unread_count()
            if args.output == 'json':
                print(json.dumps({'unread_count': count}))
            else:
                print(f"📧 Gmail - {gmail.user}")
                print(f"   Unread: {count}")
                print()
        
        if args.list:
            emails = gmail.list_emails(limit=args.limit)
            if args.output == 'json':
                print(json.dumps({'emails': emails}, ensure_ascii=False, indent=2))
            else:
                print("Recent Emails:")
                print("=" * 60)
                print(format_email_list(emails))
        
        if args.search or args.sender:
            emails = gmail.search(query=args.query, sender=args.sender)
            if args.output == 'json':
                print(json.dumps({'results': emails}, ensure_ascii=False, indent=2))
            else:
                print(f"Search Results ({len(emails)}):")
                print("=" * 60)
                print(format_email_list(emails))
        
        if args.github:
            emails = gmail.get_github_emails()
            if args.output == 'json':
                print(json.dumps({'github_emails': emails}, ensure_ascii=False, indent=2))
            else:
                print("🐙 GitHub Notifications:")
                print("=" * 60)
                print(format_email_list(emails))
        
        if args.summary:
            summary = gmail.summarize(limit=args.limit)
            if args.output == 'json':
                print(json.dumps(summary, ensure_ascii=False, indent=2))
            else:
                print("📊 Email Summary:")
                print("=" * 60)
                print(f"Total: {summary['total']}")
                print(f"🔴 Important: {len(summary['important'])}")
                print(f"🟢 Normal: {len(summary['normal'])}")
                print()
                if summary['important']:
                    print("🔴 Important Emails:")
                    print("-" * 40)
                    print(format_email_list(summary['important'], show_summary=True))
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Cancelled.")
        sys.exit(0)


if __name__ == '__main__':
    main()
