# 🔑 **Anthropic API Key Setup Guide**

## 🚀 **Step-by-Step Setup Process**

Follow these steps to get your Anthropic API key and configure it for your Khyrie3.0 platform.

---

## 📋 **Step 1: Create Anthropic Account**

### **1.1 Visit Anthropic Console**
1. Go to **[console.anthropic.com](https://console.anthropic.com)**
2. Click **"Sign Up"** or **"Get Started"**
3. Choose **"Sign up with email"**

### **1.2 Account Registration**
```
Business Email: your-business-email@domain.com
Password: Create a strong password
Name: Your full name
Company: Khyrie Fitness Platform (or your company name)
Use Case: AI-powered fitness coaching and recommendations
```

### **1.3 Email Verification**
- Check your email for verification link
- Click the verification link
- Complete account setup

---

## 💳 **Step 2: Set Up Billing (Required for API Access)**

### **2.1 Add Payment Method**
1. In the Anthropic Console, go to **"Billing"**
2. Click **"Add Payment Method"**
3. Enter your credit card information
4. Set up billing alerts (recommended: $50/month)

### **2.2 Choose Pricing Plan**
```
💡 Recommended for Khyrie3.0:
- Start with Pay-as-you-go (no monthly fee)
- Claude 3.5 Sonnet: $3/$15 per million input/output tokens
- Typical cost: $30-100/month for 1,000 active users
```

### **2.3 Set Usage Limits**
```bash
# Recommended monthly limits to start:
- Monthly spend limit: $100
- Daily spend limit: $10
- Rate limit: 1000 requests/minute
```

---

## 🔑 **Step 3: Generate API Key**

### **3.1 Create API Key**
1. In Anthropic Console, go to **"API Keys"**
2. Click **"Create Key"**
3. **Name:** `Khyrie-Production` (for production) or `Khyrie-Development` (for testing)
4. **Permissions:** Full access (default)
5. Click **"Create Key"**

### **3.2 Copy and Secure Your API Key**
```bash
# Your API key will look like this:
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

⚠️ IMPORTANT:
- Copy the key immediately (you can't view it again)
- Store it securely (never commit to Git)
- Treat it like a password
```

### **3.3 Create Multiple Keys (Recommended)**
```bash
# Create separate keys for different environments:
1. Khyrie-Development (for local testing)
2. Khyrie-Staging (for testing server)  
3. Khyrie-Production (for live platform)
```

---

## 🔧 **Step 4: Configure Environment Variables**

### **4.1 Local Development (.env)**
Create or update your local `.env` file:

```bash
# Create/edit .env file
nano .env

# Add this content:
# Anthropic Claude Configuration
ANTHROPIC_API_KEY=sk-ant-api03-your-development-key-here

# Remove old OpenAI key (if exists)
# OPENAI_API_KEY=sk-your-old-openai-key
```

### **4.2 Production Environment (.env.production)**
Update your production environment file:

```bash
# Edit production environment
nano .env.production

# Update the Anthropic section:
# Anthropic Claude Configuration (Replace with your actual key)
ANTHROPIC_API_KEY=sk-ant-api03-your-production-key-here
```

### **4.3 Staging Environment (Optional)**
```bash
# .env.staging
ANTHROPIC_API_KEY=sk-ant-api03-your-staging-key-here
```

---

## 🧪 **Step 5: Test API Integration**

### **5.1 Test Script**
Create a test file to verify your API key works:

```python
# test_claude_api.py
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_anthropic_api():
    """Test Anthropic API key and integration."""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment variables")
        return False
    
    if not api_key.startswith("sk-ant-"):
        print("❌ Invalid API key format")
        return False
    
    # Test API call
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 100,
        "messages": [
            {
                "role": "user", 
                "content": "Create a simple 10-minute beginner workout routine."
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            workout = result["content"][0]["text"]
            print("✅ API Test Successful!")
            print("📝 Sample Response:")
            print(workout[:200] + "...")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_anthropic_api()
```

### **5.2 Run the Test**
```bash
# Create and run the test
cd /Users/darnellamcguire/Khyrie3.0/src/fitness_mcp/fitness\ app/fitness\ app2.0/fitness\ app\ 3.0/

# Create test file
cat > test_claude_api.py << 'EOF'
# [Paste the test script above]
EOF

# Run the test
python3 test_claude_api.py
```

---

## 🔐 **Step 6: Security Configuration**

### **6.1 Secure Key Storage**
```bash
# Add .env files to .gitignore (if not already there)
echo ".env*" >> .gitignore
echo "test_claude_api.py" >> .gitignore

# Verify sensitive files are ignored
git status
# Should not show .env files as modified
```

### **6.2 Environment Variable Verification**
```python
# Add to your main.py or create verify_config.py
import os
from dotenv import load_dotenv

load_dotenv()

def verify_anthropic_config():
    """Verify Anthropic configuration is properly set up."""
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise ValueError("❌ ANTHROPIC_API_KEY not set in environment variables")
    
    if not api_key.startswith("sk-ant-"):
        raise ValueError("❌ Invalid ANTHROPIC_API_KEY format")
    
    if len(api_key) < 50:  # Anthropic keys are quite long
        raise ValueError("❌ ANTHROPIC_API_KEY appears to be incomplete")
    
    print("✅ Anthropic API key configuration verified")
    return True

# Run verification
verify_anthropic_config()
```

---

## 🚀 **Step 7: Deploy to Production**

### **7.1 Vercel Environment Variables**
If you're using Vercel for deployment:

```bash
# Set environment variables in Vercel
vercel env add ANTHROPIC_API_KEY production
# Paste your production API key when prompted

# Verify it's set
vercel env ls
```

### **7.2 Alternative Hosting Platforms**

#### **Heroku:**
```bash
heroku config:set ANTHROPIC_API_KEY=sk-ant-api03-your-production-key
```

#### **AWS/Digital Ocean:**
```bash
# Add to your deployment script or dashboard
export ANTHROPIC_API_KEY=sk-ant-api03-your-production-key
```

#### **Docker:**
```dockerfile
# In your Dockerfile or docker-compose.yml
ENV ANTHROPIC_API_KEY=sk-ant-api03-your-production-key
```

---

## 📊 **Step 8: Monitor Usage and Costs**

### **8.1 Anthropic Console Monitoring**
1. Go to **console.anthropic.com**
2. Navigate to **"Usage"** tab
3. Monitor:
   - Daily/monthly token usage
   - API call frequency  
   - Cost breakdown
   - Error rates

### **8.2 Set Up Alerts**
```bash
# Recommended alerts in Anthropic Console:
- 80% of monthly budget reached
- 90% of monthly budget reached
- Unusual spike in usage
- High error rate detected
```

### **8.3 Usage Tracking in Your App**
```python
# Add to premium_ai_features.py
import logging

async def log_claude_usage(user_id: int, feature: str, tokens_used: int):
    """Log Claude API usage for monitoring."""
    
    # Estimate cost (Claude 3.5 Sonnet pricing)
    input_cost = (tokens_used * 0.5) * (3.00 / 1_000_000)  # $3 per million input tokens
    output_cost = (tokens_used * 0.5) * (15.00 / 1_000_000)  # $15 per million output tokens
    total_cost = input_cost + output_cost
    
    logging.info(f"Claude API usage - User: {user_id}, Feature: {feature}, "
                f"Tokens: {tokens_used}, Cost: ${total_cost:.4f}")
    
    # Store in database for analytics
    # await save_api_usage(user_id, feature, tokens_used, total_cost)
```

---

## 🎯 **Step 9: Test Premium Features**

### **9.1 Test Workout Generation**
```bash
# Test the premium workout generation feature
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

### **9.2 Test AI Coach**
```bash
# Test the AI coach conversation feature
curl -X POST http://localhost:8000/api/premium/coach \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-test-token" \
  -d '{
    "message": "I am feeling unmotivated to workout today. Can you help?",
    "context": "general_motivation"
  }'
```

### **9.3 Test Injury Prevention**
```bash
# Test the injury prevention analysis
curl -X POST http://localhost:8000/api/premium/injury-analysis \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-test-token" \
  -d '{
    "sleep_quality": 7,
    "stress_level": 6,
    "current_soreness": 4,
    "pain_areas": ["lower_back"]
  }'
```

---

## ❓ **Troubleshooting Common Issues**

### **API Key Not Working**
```bash
# Check these common issues:
1. Key copied incorrectly (missing characters)
2. Key has wrong permissions
3. Billing not set up in Anthropic Console
4. Account not verified
5. Environment variable not loaded properly
```

### **Rate Limiting**
```bash
# If you get rate limit errors:
1. Check your rate limits in Anthropic Console
2. Implement exponential backoff in your code
3. Consider upgrading your rate limits
4. Cache common responses
```

### **High Costs**
```bash
# If costs are higher than expected:
1. Monitor token usage per request
2. Implement response caching
3. Optimize prompt length
4. Set stricter usage limits
5. Use shorter max_tokens for simple requests
```

---

## ✅ **Verification Checklist**

Before going live, verify:

- [ ] ✅ Anthropic account created and verified
- [ ] ✅ Billing set up with payment method
- [ ] ✅ API key generated and securely stored
- [ ] ✅ Environment variables configured (.env and .env.production)
- [ ] ✅ Test script runs successfully
- [ ] ✅ Premium features work with Claude API
- [ ] ✅ Usage monitoring set up
- [ ] ✅ Cost alerts configured
- [ ] ✅ API key not committed to Git
- [ ] ✅ Production environment variables deployed

---

## 🎉 **You're Ready!**

Once all steps are complete, your Khyrie3.0 platform will be powered by Claude 3.5 Sonnet for:

🏋️ **Premium Workout Generation** ($9.99/month)
🩺 **Pro Injury Prevention Analysis** ($19.99/month)  
🤖 **Elite Personal AI Coach** ($39.99/month)

**Your premium AI features are now ready to generate revenue with Claude's superior capabilities!** 💰🚀

---

## 📞 **Support Resources**

- **Anthropic Documentation:** [docs.anthropic.com](https://docs.anthropic.com)
- **API Status:** [status.anthropic.com](https://status.anthropic.com)
- **Support:** [support@anthropic.com](mailto:support@anthropic.com)
- **Pricing:** [anthropic.com/pricing](https://www.anthropic.com/pricing)