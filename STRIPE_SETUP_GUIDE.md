# 💳 **Stripe Account Setup Guide for Khyrie3.0**

## 🚀 **Complete Payment Processing Setup**

This guide walks you through setting up Stripe to process payments for your Khyrie3.0 AI Fitness Platform subscriptions.

---

## 📋 **Step 1: Create Stripe Account**

### **1.1 Account Registration**
1. **Visit Stripe:** Go to [stripe.com](https://stripe.com)
2. **Click "Start now"** or "Sign up"
3. **Choose Account Type:** Business account (recommended)
4. **Enter Business Information:**
   - Business name: `Khyrie Fitness Platform` or your company name
   - Country: Select your country
   - Business type: `Software/SaaS`
   - Business description: `AI-powered fitness and wellness platform`

### **1.2 Business Verification**
- **Tax ID/EIN:** Provide your business tax identification number
- **Bank Account:** Add your business bank account for payouts
- **Business Address:** Your business/home office address
- **Representative Information:** Your personal details as business owner

### **1.3 Account Activation**
- **Identity Verification:** Upload government-issued ID
- **Business Documents:** Articles of incorporation (if applicable)
- **Bank Verification:** Stripe will make small test deposits

---

## 🏗️ **Step 2: Create Products and Pricing**

### **2.1 Navigate to Products**
1. Log into Stripe Dashboard
2. Go to **Products** in the left sidebar
3. Click **"+ Add product"**

### **2.2 Create Subscription Products**

#### **Premium Plan Product**
```
Product Information:
- Name: Khyrie Premium
- Description: AI-powered fitness recommendations and advanced analytics
- Image: Upload your Khyrie logo/fitness image
```

**Pricing Information:**
```
- Price: $9.99
- Billing: Monthly (recurring)
- Currency: USD
- Price ID: Will be generated (save this!)
```

#### **Pro Plan Product**
```
Product Information:
- Name: Khyrie Pro
- Description: Advanced features including form analysis and injury prevention
- Image: Upload your Khyrie logo/fitness image
```

**Pricing Information:**
```
- Price: $19.99
- Billing: Monthly (recurring)
- Currency: USD
- Price ID: Will be generated (save this!)
```

#### **Elite Plan Product**
```
Product Information:
- Name: Khyrie Elite
- Description: Complete fitness ecosystem with personal AI coach
- Image: Upload your Khyrie logo/fitness image
```

**Pricing Information:**
```
- Price: $39.99
- Billing: Monthly (recurring)
- Currency: USD
- Price ID: Will be generated (save this!)
```

### **2.3 Configure Trial Periods**
For each product:
1. Click on the price you created
2. Select **"Edit price"**
3. Under **"Trial period"**, set to **7 days**
4. Save changes

---

## 🔑 **Step 3: Get API Keys**

### **3.1 Test Mode Keys (Development)**
1. Go to **Developers** → **API keys**
2. Make sure you're in **"Test mode"** (toggle at top)
3. Copy these keys:

```
Publishable key: pk_test_xxxxx (starts with pk_test_)
Secret key: sk_test_xxxxx (starts with sk_test_)
```

### **3.2 Live Mode Keys (Production)**
1. Switch to **"Live mode"** using the toggle
2. Copy these keys (use for production only):

```
Publishable key: pk_live_xxxxx (starts with pk_live_)
Secret key: sk_live_xxxxx (starts with sk_live_)
```

**⚠️ Security Note:** Never commit secret keys to version control!

---

## 🔗 **Step 4: Configure Webhooks**

### **4.1 Create Webhook Endpoint**
1. Go to **Developers** → **Webhooks**
2. Click **"+ Add endpoint"**
3. **Endpoint URL:** `https://your-domain.com/api/subscriptions/webhook`
4. **Events to send:** Select these events:
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `checkout.session.completed`

### **4.2 Get Webhook Secret**
1. Click on your created webhook
2. Copy the **"Signing secret"** (starts with `whsec_`)
3. Save this for environment variables

---

## 🌐 **Step 5: Update Environment Variables**

### **5.1 Development Environment (.env)**
Create/update your `.env` file:

```bash
# Stripe Test Keys (Development)
STRIPE_SECRET_KEY=sk_test_your_actual_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_actual_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_actual_webhook_secret_here

# Stripe Price IDs (from Step 2)
STRIPE_PREMIUM_PRICE_ID=price_actual_premium_id_here
STRIPE_PRO_PRICE_ID=price_actual_pro_id_here
STRIPE_ELITE_PRICE_ID=price_actual_elite_id_here
```

### **5.2 Production Environment (.env.production)**
Update your production environment file:

```bash
# Stripe Live Keys (Production - DO NOT COMMIT)
STRIPE_SECRET_KEY=sk_live_your_actual_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_live_your_actual_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_actual_webhook_secret_here

# Stripe Price IDs (same as development)
STRIPE_PREMIUM_PRICE_ID=price_actual_premium_id_here
STRIPE_PRO_PRICE_ID=price_actual_pro_id_here
STRIPE_ELITE_PRICE_ID=price_actual_elite_id_here
```

---

## 🧪 **Step 6: Testing Setup**

### **6.1 Test Credit Cards**
Use these test cards in development:

```
Successful Payment:
Card Number: 4242 4242 4242 4242
Expiry: Any future date (e.g., 12/25)
CVC: Any 3 digits (e.g., 123)

Declined Payment:
Card Number: 4000 0000 0000 0002
Expiry: Any future date
CVC: Any 3 digits

3D Secure Required:
Card Number: 4000 0025 0000 3155
Expiry: Any future date
CVC: Any 3 digits
```

### **6.2 Test Subscription Flow**
1. Start your local server
2. Navigate to `/subscription` page
3. Try subscribing with test card numbers
4. Check Stripe dashboard for test payments

---

## 📊 **Step 7: Dashboard Configuration**

### **7.1 Business Settings**
1. Go to **Settings** → **Business settings**
2. Update:
   - Business name and description
   - Support email and phone
   - Business website URL
   - Terms of service and privacy policy URLs

### **7.2 Customer Portal**
1. Go to **Settings** → **Customer portal**
2. Enable customer portal
3. Configure:
   - Subscription cancellation
   - Payment method updates
   - Invoice history access
   - Billing address collection

### **7.3 Email Settings**
1. Go to **Settings** → **Emails**
2. Customize:
   - Receipt emails
   - Invoice emails
   - Failed payment emails
   - Subscription notifications

---

## 🔐 **Step 8: Security Configuration**

### **8.1 Webhook Security**
- Always verify webhook signatures
- Use HTTPS endpoints only
- Implement idempotency handling
- Store webhook events for debugging

### **8.2 API Key Security**
- Use environment variables for all keys
- Rotate keys periodically
- Use restricted API keys when possible
- Monitor API key usage in dashboard

### **8.3 Fraud Prevention**
1. Go to **Radar** → **Rules**
2. Enable Radar for fraud detection
3. Configure risk thresholds
4. Set up email notifications for suspicious activity

---

## 💰 **Step 9: Pricing and Fees**

### **9.1 Stripe Fees**
- **Standard rate:** 2.9% + $0.30 per successful charge
- **International cards:** Additional 1.5%
- **Currency conversion:** 1%
- **Disputes:** $15.00 per chargeback

### **9.2 Payout Schedule**
- **Default:** 2 business days after payment
- **Express:** Next business day (available for established accounts)
- **Custom:** Weekly or monthly payouts

---

## 📈 **Step 10: Analytics and Reporting**

### **10.1 Revenue Analytics**
- Monitor MRR (Monthly Recurring Revenue)
- Track churn rates
- Analyze payment success rates
- Review customer lifetime value

### **10.2 Key Metrics Dashboard**
Set up tracking for:
- New subscriptions
- Subscription upgrades/downgrades
- Failed payments and recovery
- Customer acquisition cost

---

## 🚀 **Step 11: Go Live Checklist**

### **Before Going Live:**
- [ ] Business verification completed
- [ ] Bank account connected and verified
- [ ] Products and prices created
- [ ] Webhooks configured and tested
- [ ] Test payments successful
- [ ] Environment variables updated
- [ ] Customer portal configured
- [ ] Email notifications set up
- [ ] Fraud protection enabled

### **After Going Live:**
- [ ] Monitor first real transactions
- [ ] Test customer portal functionality
- [ ] Verify webhook delivery
- [ ] Check payout schedule
- [ ] Monitor dashboard for issues

---

## 🎯 **Integration Code Examples**

### **Frontend Integration (subscription.html)**
Update your subscription page with real Stripe keys:

```javascript
// Replace test key with your actual publishable key
const stripe = Stripe('pk_live_your_actual_publishable_key');

// Real payment method creation
const { error, paymentMethod } = await stripe.createPaymentMethod({
    type: 'card',
    card: cardElement, // Use Stripe Elements for real card input
    billing_details: {
        name: customerName,
        email: customerEmail
    }
});
```

### **Backend Integration (subscription_routes.py)**
Your code is already set up to use environment variables:

```python
# This will automatically use your real keys from environment
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Price IDs will be loaded from environment
STRIPE_PREMIUM_PRICE_ID = os.getenv("STRIPE_PREMIUM_PRICE_ID")
```

---

## 🛡️ **Security Best Practices**

### **Environment Variables Security**
```bash
# Never commit these to Git
.env
.env.production
.env.local

# Add to .gitignore
echo ".env*" >> .gitignore
```

### **Production Deployment**
When deploying to Vercel/production:
```bash
# Set environment variables in your hosting platform
vercel env add STRIPE_SECRET_KEY production
vercel env add STRIPE_PUBLISHABLE_KEY production
vercel env add STRIPE_WEBHOOK_SECRET production
```

---

## 📞 **Support and Resources**

### **Stripe Resources**
- [Stripe Documentation](https://stripe.com/docs)
- [Subscription Billing Guide](https://stripe.com/docs/billing/subscriptions)
- [Webhooks Guide](https://stripe.com/docs/webhooks)
- [Testing Guide](https://stripe.com/docs/testing)

### **Khyrie Integration**
- Your subscription system is already built
- Environment variables are configured
- Webhook handling is implemented
- Error handling is included

### **Getting Help**
- **Stripe Support:** Available 24/7 via dashboard
- **Community Forum:** Stripe Developer Community
- **Documentation:** Comprehensive guides and examples

---

## ✅ **Quick Start Summary**

1. **Create Stripe account** → Complete business verification
2. **Set up products** → Create Premium, Pro, Elite plans  
3. **Get API keys** → Copy test and live keys
4. **Configure webhooks** → Set endpoint URL and events
5. **Update environment variables** → Add real keys to your app
6. **Test thoroughly** → Use test cards to verify flow
7. **Go live** → Switch to live keys when ready

**Your Khyrie3.0 platform is already built to handle Stripe payments - you just need to add your real keys and product IDs!** 🚀

---

**Need help with any of these steps? Each section includes detailed instructions to get you processing payments and generating revenue quickly.** 💰