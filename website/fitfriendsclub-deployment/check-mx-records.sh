#!/bin/bash

echo "==================================================="
echo "Cloudflare MX Record Configuration Helper"
echo "==================================================="
echo ""

echo "🔍 Current MX Records for fitfriendsclub.com:"
echo "--------------------------------------------"
MX_RECORDS=$(dig fitfriendsclub.com MX +short 2>/dev/null)
if [ -z "$MX_RECORDS" ]; then
    echo "❌ No MX records found - Email hosting not configured"
    echo ""
    echo "📧 REQUIRED MX RECORDS FOR CLOUDFLARE EMAIL ROUTING:"
    echo "---------------------------------------------------"
    echo "Add these in your Cloudflare Dashboard:"
    echo ""
    echo "Type: MX, Name: @, Content: isaac.mx.cloudflare.net, Priority: 46"
    echo "Type: MX, Name: @, Content: linda.mx.cloudflare.net, Priority: 92" 
    echo "Type: MX, Name: @, Content: amir.mx.cloudflare.net, Priority: 78"
    echo ""
    echo "🔗 Quick Setup URL:"
    echo "https://dash.cloudflare.com/$(dig fitfriendsclub.com NS +short | head -1 | sed 's/.*cloudflare.*/[YOUR-ZONE-ID]/')"
    echo ""
    echo "📝 STEP-BY-STEP INSTRUCTIONS:"
    echo "1. Go to: https://dash.cloudflare.com"
    echo "2. Select domain: fitfriendsclub.com" 
    echo "3. Click: DNS → Records"
    echo "4. Click: '+ Add record'"
    echo "5. Select: MX from dropdown"
    echo "6. Add each MX record above"
    echo ""
    echo "✨ EASIER METHOD - Use Email Routing:"
    echo "1. Go to: Email → Email Routing in Cloudflare"
    echo "2. Click: 'Enable Email Routing'"  
    echo "3. MX records are added automatically!"
    echo ""
else
    echo "✅ Found existing MX records:"
    echo "$MX_RECORDS"
    echo ""
fi

echo "📋 Required SPF Record:"
echo "----------------------"
SPF_RECORD=$(dig fitfriendsclub.com TXT +short 2>/dev/null | grep spf)
if [ -z "$SPF_RECORD" ]; then
    echo "❌ No SPF record found"
    echo "Add this TXT record:"
    echo "Type: TXT, Name: @, Content: v=spf1 include:_spf.mx.cloudflare.net ~all"
else
    echo "✅ SPF record found: $SPF_RECORD"
fi

echo ""
echo "🧪 Test After Setup:"
echo "-------------------"
echo "dig fitfriendsclub.com MX"
echo "dig fitfriendsclub.com TXT | grep spf"
echo ""
echo "📧 Email Addresses Ready After Setup:"
echo "------------------------------------" 
echo "• hello@fitfriendsclub.com"
echo "• support@fitfriendsclub.com"
echo ""
echo "==================================================="