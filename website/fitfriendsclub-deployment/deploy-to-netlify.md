# 🚀 Deploy FitFriendsClub to Netlify

## Quick Steps:
1. Go to https://netlify.com and login
2. Click "New site from Git"  
3. Connect to GitHub: https://github.com/DartinBot/Khyrie
4. Select the fitfriendsclub-deployment folder
5. Deploy settings:
   - Build command: (leave empty)
   - Publish directory: fitfriendsclub-deployment
6. Click "Deploy site"

## After deployment:
- You'll get: random-name.netlify.app
- Copy that URL for DNS setup

## Cloudflare DNS Setup:
1. Login to Cloudflare dashboard
2. Select fitfriendsclubs.com domain
3. Go to DNS > Records
4. Add these records:

Type: CNAME
Name: www
Content: [your-site].netlify.app
Proxy: Orange cloud (Proxied)

Type: CNAME
Name: @
Content: [your-site].netlify.app  
Proxy: Orange cloud (Proxied)

## In Netlify:
1. Site settings > Domain management
2. Add custom domain: fitfriendsclubs.com
3. Add custom domain: www.fitfriendsclubs.com
4. Enable SSL certificate (automatic)
