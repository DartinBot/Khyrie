# 🤖 **OpenAI GPT-4 API Setup Guide**

## 🚀 **Complete Setup for Khyrie3.0 Premium AI Features**

Your Khyrie3.0 fitness platform uses OpenAI's GPT-4 for premium AI features. This guide walks you through setting up your API key and configuring the integration.

---

## 📋 **Step 1: Create OpenAI Account**

### **1.1 Visit OpenAI Platform**
1. Go to **[platform.openai.com](https://platform.openai.com)**
2. Click **"Sign up"** or **"Get Started"**
3. Choose **"Sign up with email"**

### **1.2 Account Registration**
```
Business Email: your-business-email@domain.com
Password: Create a strong password
Name: Your full name
Organization: Khyrie Fitness Platform (optional)
Use Case: AI-powered fitness coaching and recommendations
```

### **1.3 Phone Verification**
- OpenAI requires phone number verification
- Enter your phone number and verify with SMS code
- Complete account setup and email verification

---

## 💳 **Step 2: Set Up Billing (Required for GPT-4)**

### **2.1 Add Payment Method**
1. In OpenAI Dashboard, go to **"Settings"** → **"Billing"**
2. Click **"Add Payment Method"**
3. Enter your credit card information
4. Set up usage limits (recommended: $50/month to start)

### **2.2 Understand Pricing**
```
GPT-4 Pricing (as of 2025):
- Input tokens: $0.03 per 1K tokens
- Output tokens: $0.06 per 1K tokens

Typical Khyrie Usage (per interaction):
- Workout Generation: ~500 tokens = $0.015-0.030
- Injury Analysis: ~300 tokens = $0.009-0.018  
- Coach Chat: ~200 tokens = $0.006-0.012

Estimated Monthly Cost (1,000 users): $200-500
```

### **2.3 Set Usage Limits**
```bash
# Recommended monthly limits:
- Hard limit: $100/month (to prevent overspend)
- Soft limit: $50/month (get email alerts)
- Email notifications: Enable all billing alerts
```

---

## 🔑 **Step 3: Generate API Key**

### **3.1 Create API Key**
1. In OpenAI Dashboard, go to **"API Keys"**
2. Click **"+ Create new secret key"**
3. **Name:** `Khyrie-Production` (or `Khyrie-Development` for testing)
4. **Permissions:** All (default is fine)
5. Click **"Create secret key"**

### **3.2 Copy and Secure Your API Key**
```bash
# Your API key will look like this:
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

⚠️ CRITICAL SECURITY:
- Copy the key immediately (you can't view it again)
- Never share or commit to Git
- Store securely (treat like a password)
- Use environment variables only
```

### **3.3 Create Multiple Keys (Best Practice)**
```bash
# Create separate keys for different environments:
1. Khyrie-Development (for local testing)
2. Khyrie-Staging (for testing server)  
3. Khyrie-Production (for live platform)
```

---

## 🔧 **Step 4: Configure Environment Variables**

### **4.1 Local Development (.env)**
Create your local environment file:

```bash
# Create .env file (if it doesn't exist)
cp .env.template .env

# Edit the file and add your API key:
nano .env

# Add this line with your actual key:
OPENAI_API_KEY=sk-your-actual-development-key-here
```

### **4.2 Production Environment (.env.production)**
Your production file should already have the structure:

```bash
# OpenAI Configuration (Replace with your actual key)
OPENAI_API_KEY=sk-your-actual-production-key-here
```

### **4.3 Security Check**
```bash
# Verify .env files are not tracked by Git
git status
# Should not show .env files

# If they appear, add to .gitignore:
echo ".env*" >> .gitignore
```

---

## 🧪 **Step 5: Test Your Setup**

### **5.1 Run the Test Script**
```bash
# Make test script executable and run it
chmod +x test_openai_setup.py
python3 test_openai_setup.py
```

### **5.2 Expected Output**
```bash
🤖 OpenAI GPT-4 API Setup Verification
============================================================
🔍 Testing OpenAI API Configuration...
✅ API key format valid: sk-xxxxxxxxxxxxx...

🧪 Testing API connection...
📡 Making API request to GPT-4...
✅ API Test Successful!
📊 Response length: 245 characters
🔢 Tokens used: 156
💰 Estimated cost: $0.0047

📝 Sample GPT-4 Response:
------------------------------
Here's a simple 10-minute beginner workout...
------------------------------

⚙️  Verifying Environment Configuration...
✅ No conflicting Anthropic key found
✅ OPENAI_API_KEY configured
✅ STRIPE_SECRET_KEY configured
✅ DATABASE_URL configured

🏁 Test Results Summary
Tests passed: 2/2
🎉 All tests passed! Your OpenAI GPT-4 API is ready to use.
```

---

## 🎯 **Step 6: Test Premium Features**

### **6.1 Start Your Server**
```bash
# Start the Khyrie server
python3 main.py
```

### **6.2 Test Premium Workout Generation**
```bash
# Test via API (replace with actual auth token)
curl -X POST http://localhost:8000/api/premium/workout \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-test-token" \
  -d '{
    "workout_type": "strength",
    "fitness_level": "intermediate", 
    "available_time": 45,
    "available_equipment": ["dumbbells", "bench"],
    "goals": ["muscle_gain", "strength"]
  }'
```

### **6.3 Test AI Coach**
```bash
# Test AI coach conversation
curl -X POST http://localhost:8000/api/premium/coach \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-test-token" \
  -d '{
    "message": "I need motivation for my workout today",
    "context": "general_motivation"
  }'
```

---

## 📊 **Step 7: Monitor Usage and Costs**

### **7.1 OpenAI Dashboard Monitoring**
1. Visit **[platform.openai.com](https://platform.openai.com)**
2. Go to **"Usage"** section
3. Monitor:
   - Daily API calls and token usage
   - Monthly spending
   - Model usage breakdown (GPT-4 vs GPT-3.5)
   - Rate limit status

### **7.2 Set Up Billing Alerts**
```bash
# In OpenAI Dashboard → Settings → Billing:
- Email alerts at 75% of limit
- Email alerts at 90% of limit  
- Hard stop at monthly limit
- Daily spending notifications
```

### **7.3 Usage Optimization Tips**
```python
# Optimize your GPT-4 usage for cost efficiency:

1. Use GPT-3.5-turbo for simple tasks (10x cheaper)
2. Implement response caching for similar requests
3. Optimize prompt length (shorter = cheaper)
4. Set appropriate max_tokens limits
5. Use temperature wisely (lower = more consistent)
```

---

## 🚀 **Step 8: Deploy to Production**

### **8.1 Vercel Environment Variables**
```bash
# Set production API key in Vercel
vercel env add OPENAI_API_KEY production
# Enter your production API key when prompted

# Verify it's set
vercel env ls
```

### **8.2 Alternative Hosting**

#### **Heroku:**
```bash
heroku config:set OPENAI_API_KEY=sk-your-production-key
```

#### **Docker:**
```dockerfile
# In docker-compose.yml or Dockerfile
ENV OPENAI_API_KEY=sk-your-production-key
```

---

## 💰 **Cost Management & Optimization**

### **8.1 Estimated Costs for Khyrie3.0**
```
Premium Feature Usage (Monthly):

🏋️ Workout Generation:
- 1,000 premium users × 10 workouts = 10,000 requests
- ~500 tokens per request = 5M tokens
- Cost: 5M × $0.045/1K = $225/month

🩺 Injury Analysis:  
- 500 pro users × 5 analyses = 2,500 requests
- ~300 tokens per request = 750K tokens
- Cost: 750K × $0.045/1K = $34/month

🤖 AI Coach:
- 200 elite users × 50 chats = 10,000 requests  
- ~200 tokens per request = 2M tokens
- Cost: 2M × $0.045/1K = $90/month

Total Estimated: ~$350/month for 1,700 active premium users
```

### **8.2 Cost Optimization Strategies**
```python
# 1. Implement Smart Caching
import redis
cache = redis.Redis()

def cached_gpt_response(prompt_hash, prompt):
    cached = cache.get(f"gpt:{prompt_hash}")
    if cached:
        return json.loads(cached)
    
    response = openai.ChatCompletion.create(...)
    cache.setex(f"gpt:{prompt_hash}", 3600, json.dumps(response))
    return response

# 2. Use GPT-3.5 for Simple Tasks
def choose_model(complexity):
    return "gpt-4" if complexity == "high" else "gpt-3.5-turbo"

# 3. Optimize Token Usage
def optimize_prompt(user_input):
    # Remove unnecessary context, use abbreviations
    return truncated_prompt
```

---

## ❓ **Troubleshooting Common Issues**

### **API Key Problems**
```bash
❌ Invalid API key format
💡 Ensure key starts with "sk-" and is complete

❌ Authentication failed  
💡 Check key is active and not revoked in OpenAI dashboard

❌ Insufficient quota
💡 Add payment method and increase billing limits
```

### **Rate Limiting**
```bash
❌ Rate limit exceeded
💡 Implement exponential backoff in your code
💡 Upgrade to higher rate limits if needed
💡 Distribute requests across time
```

### **High Costs**
```bash
❌ Unexpected high usage
💡 Monitor token usage per request
💡 Implement caching for repeated requests
💡 Use GPT-3.5 for simpler tasks
💡 Set stricter max_tokens limits
```

---

## ✅ **Pre-Launch Checklist**

Before going live with premium features:

- [ ] ✅ OpenAI account created and phone verified
- [ ] ✅ Billing set up with payment method and limits
- [ ] ✅ API key generated for production
- [ ] ✅ Environment variables configured securely
- [ ] ✅ Test script passes all checks
- [ ] ✅ Premium features tested and working
- [ ] ✅ Usage monitoring and alerts configured
- [ ] ✅ Cost optimization strategies implemented
- [ ] ✅ Production deployment completed
- [ ] ✅ API key secured (never committed to Git)

---

## 🎉 **You're Ready to Generate Revenue!**

Your Khyrie3.0 platform is now powered by GPT-4 for:

🏋️ **Premium AI Workout Generation** ($9.99/month)
🩺 **Pro Injury Prevention Analysis** ($19.99/month)  
🤖 **Elite Personal AI Coach** ($39.99/month)

**Expected Revenue Potential:** $10,000-50,000/month
**AI Costs:** ~$350-700/month (1-2% of revenue)

---

## 📞 **Support Resources**

### **OpenAI Resources**
- **Documentation:** [platform.openai.com/docs](https://platform.openai.com/docs)
- **API Status:** [status.openai.com](https://status.openai.com)
- **Support:** [help.openai.com](https://help.openai.com)
- **Community:** [community.openai.com](https://community.openai.com)

### **Pricing & Billing**
- **Pricing Page:** [openai.com/pricing](https://openai.com/pricing)
- **Usage Dashboard:** [platform.openai.com/usage](https://platform.openai.com/usage)
- **Billing Settings:** [platform.openai.com/account/billing](https://platform.openai.com/account/billing)

**Your premium AI features are ready to generate revenue with GPT-4's powerful capabilities!** 🚀💰