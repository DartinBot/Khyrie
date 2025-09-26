# DNS Configuration for fitfriendsclub.com

## Required DNS Records

### 1. A Records (IPv4)
```
Type: A
Name: @
Value: [YOUR_SERVER_IP_ADDRESS]
TTL: 300 (or default)

Type: A  
Name: www
Value: [YOUR_SERVER_IP_ADDRESS]
TTL: 300 (or default)
```

### 2. AAAA Records (IPv6) - Optional
```
Type: AAAA
Name: @
Value: [YOUR_IPv6_ADDRESS]
TTL: 300 (or default)

Type: AAAA
Name: www  
Value: [YOUR_IPv6_ADDRESS]
TTL: 300 (or default)
```

### 3. CNAME Records
```
Type: CNAME
Name: api
Value: fitfriendsclub.com
TTL: 300 (or default)
```

### 4. MX Records (Email)
```
Type: MX
Name: @
Value: mail.fitfriendsclub.com
Priority: 10
TTL: 300 (or default)

Type: MX
Name: @
Value: mail2.fitfriendsclub.com  
Priority: 20
TTL: 300 (or default)
```

### 5. TXT Records
```
Type: TXT
Name: @
Value: "v=spf1 include:_spf.google.com ~all"
TTL: 300 (or default)

Type: TXT
Name: _dmarc
Value: "v=DMARC1; p=quarantine; rua=mailto:dmarc@fitfriendsclub.com"
TTL: 300 (or default)
```

## Common DNS Hosting Providers

### Cloudflare
1. Login to Cloudflare dashboard
2. Select your domain: fitfriendsclub.com
3. Go to DNS > Records
4. Add the above records

### AWS Route 53
1. Login to AWS Console
2. Go to Route 53 > Hosted Zones
3. Select fitfriendsclub.com
4. Create the above record sets

### GoDaddy
1. Login to GoDaddy account
2. Go to My Products > DNS
3. Select fitfriendsclub.com
4. Add the above records

### Namecheap
1. Login to Namecheap account
2. Go to Domain List
3. Click "Manage" next to fitfriendsclub.com
4. Go to Advanced DNS tab
5. Add the above records

## SSL/TLS Certificate
After DNS propagation, obtain an SSL certificate:

### Using Let's Encrypt (Recommended)
```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot --nginx -d fitfriendsclub.com -d www.fitfriendsclub.com
```

### Using Cloudflare (If using Cloudflare)
- Enable "Always Use HTTPS" in SSL/TLS settings
- Set SSL mode to "Full (Strict)"

## Verification Commands

### Check DNS Propagation
```bash
# Check A record
nslookup fitfriendsclub.com

# Check from different DNS servers
dig @8.8.8.8 fitfriendsclub.com
dig @1.1.1.1 fitfriendsclub.com

# Check MX records
dig MX fitfriendsclub.com

# Check TXT records
dig TXT fitfriendsclub.com
```

### Online Tools
- https://dnschecker.org
- https://whatsmydns.net
- https://mxtoolbox.com

## API Endpoints Configuration

Based on your website's JavaScript configuration, ensure these endpoints are configured:

```
https://fitfriendsclub.com/api/contact
https://fitfriendsclub.com/api/membership  
https://fitfriendsclub.com/api/newsletter
```

## Email Configuration

Your website references these email addresses:
- hello@fitfriendsclub.com
- support@fitfriendsclub.com

Make sure to configure email hosting/forwarding for these addresses.

## Notes

1. DNS propagation can take 24-48 hours globally
2. Start with lower TTL values (300s) for faster updates during setup
3. Increase TTL to 3600s or higher once stable
4. Always backup existing DNS records before making changes
5. Test website functionality after DNS changes

## Security Recommendations

1. Enable DNSSEC if supported by your registrar
2. Use CAA records to restrict certificate authorities
3. Implement proper SPF, DKIM, and DMARC for email security
4. Consider using Cloudflare for DDoS protection and CDN

```
Type: CAA
Name: @
Value: 0 issue "letsencrypt.org"
TTL: 300
```

## Monitoring

Set up monitoring for:
- Website uptime
- DNS resolution
- SSL certificate expiration
- Email delivery

---

**Important**: Replace [YOUR_SERVER_IP_ADDRESS] and [YOUR_IPv6_ADDRESS] with your actual server IP addresses before configuring DNS records.