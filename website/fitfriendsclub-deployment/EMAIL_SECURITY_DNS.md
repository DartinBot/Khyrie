# Email Security DNS Records for fitfriendsclub.com

## Required DNS Records for Email Security

### 1. SPF Record (Sender Policy Framework)
**Prevents email spoofing by specifying authorized mail servers**

```
Type: TXT
Name: @
Content: v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all
TTL: 300
```

### 2. DKIM Record (DomainKeys Identified Mail)
**Adds digital signature to emails for authenticity**

After setting up Google Workspace or email provider, they will provide a DKIM key like:
```
Type: TXT
Name: google._domainkey
Content: v=DKIM1; k=rsa; p=[DKIM_PUBLIC_KEY_PROVIDED_BY_GOOGLE]
TTL: 300
```

### 3. DMARC Record (Domain-based Message Authentication)
**Policy for handling emails that fail SPF/DKIM checks**

```
Type: TXT
Name: _dmarc
Content: v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@fitfriendsclub.com; ruf=mailto:dmarc-failures@fitfriendsclub.com; sp=quarantine; adkim=r; aspf=r
TTL: 300
```

### 4. MTA-STS Record (Mail Transfer Agent Strict Transport Security)
**Enforces encrypted email delivery**

```
Type: TXT
Name: _mta-sts
Content: v=STSv1; id=202509261200;
TTL: 300
```

### 5. TLS-RPT Record (TLS Reporting)
**Reports TLS issues for email delivery**

```
Type: TXT
Name: _smtp._tls
Content: v=TLSRPTv1; rua=mailto:tls-reports@fitfriendsclub.com
TTL: 300
```

## Quick Setup Instructions

### For Cloudflare Users:
1. Login to Cloudflare Dashboard
2. Select: fitfriendsclub.com
3. Go to: DNS → Records
4. Add each TXT record above

### Verification Commands:
```bash
# Check SPF record
dig fitfriendsclub.com TXT | grep spf

# Check DMARC record
dig _dmarc.fitfriendsclub.com TXT

# Check DKIM record (after setup)
dig google._domainkey.fitfriendsclub.com TXT

# Test email security
# Use online tools:
# - https://mxtoolbox.com/dmarc.aspx
# - https://dmarcanalyzer.com
# - https://www.mail-tester.com
```

## Current Email Addresses to Secure:
- hello@fitfriendsclub.com
- support@fitfriendsclub.com
- dmarc-reports@fitfriendsclub.com (for DMARC reporting)
- dmarc-failures@fitfriendsclub.com (for DMARC failures)
- tls-reports@fitfriendsclub.com (for TLS reporting)

## Email Security Benefits:
✅ Prevents email spoofing attacks
✅ Improves email deliverability  
✅ Protects brand reputation
✅ Provides visibility into email threats
✅ Enforces secure email transmission
✅ Compliance with email security standards

## Implementation Priority:
1. **SPF Record** (Immediate - prevents spoofing)
2. **DMARC Record** (High - provides policy and reporting)  
3. **DKIM Record** (When setting up email provider)
4. **MTA-STS** (Advanced - enforces encryption)
5. **TLS-RPT** (Advanced - monitoring)

---

**Note**: Start with SPF and DMARC records immediately. Add DKIM when you configure your email provider (Google Workspace, etc.).