# Cloudflare MX Records for fitfriendsclub.com

## MX Records to Add in Cloudflare Dashboard

Navigate to: **Cloudflare Dashboard → fitfriendsclub.com → DNS → Records**

### Add these MX Records:

```
Type: MX
Name: @ 
Content: isaac.mx.cloudflare.net
Priority: 46
TTL: Auto

Type: MX  
Name: @
Content: linda.mx.cloudflare.net
Priority: 92
TTL: Auto

Type: MX
Name: @
Content: amir.mx.cloudflare.net  
Priority: 78
TTL: Auto
```

## Required TXT Record (SPF):

```
Type: TXT
Name: @
Content: v=spf1 include:_spf.mx.cloudflare.net ~all
TTL: Auto
```

## Step-by-Step Instructions:

### 1. Login to Cloudflare
- Go to: https://dash.cloudflare.com
- Login with your account
- Select: **fitfriendsclub.com**

### 2. Navigate to DNS
- Click: **DNS** in the left sidebar
- Click: **Records** tab

### 3. Add MX Records
For each MX record above:
- Click: **+ Add record**
- Select: **MX** from dropdown
- Name: **@** (represents your root domain)
- Mail server: **[Content from above]**
- Priority: **[Priority number from above]**
- TTL: **Auto**
- Click: **Save**

### 4. Add SPF Record
- Click: **+ Add record**
- Select: **TXT** from dropdown  
- Name: **@**
- Content: **v=spf1 include:_spf.mx.cloudflare.net ~all**
- TTL: **Auto**
- Click: **Save**

## Alternative: Use Cloudflare Email Routing (Automatic)

**EASIER METHOD**: Instead of manually adding MX records, use Cloudflare's Email Routing feature:

1. Go to: **Email** → **Email Routing** in Cloudflare dashboard
2. Click: **Enable Email Routing**
3. Cloudflare will **automatically add all MX records**
4. You just need to configure forwarding addresses

## Verification Commands

After adding records, verify with these commands:

```bash
# Check MX records
dig fitfriendsclub.com MX

# Check SPF record
dig fitfriendsclub.com TXT | grep spf

# Check all DNS records
dig fitfriendsclub.com ANY
```

## Expected Results After Setup:

```bash
$ dig fitfriendsclub.com MX +short
46 isaac.mx.cloudflare.net.
78 amir.mx.cloudflare.net.
92 linda.mx.cloudflare.net.
```

---

**RECOMMENDATION**: Use the **Email Routing** feature instead of manually adding MX records - it's easier and automatically configured!