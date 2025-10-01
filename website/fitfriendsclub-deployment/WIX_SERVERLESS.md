# Serverless Backend for Wix Frontend

## ⚡ Serverless Flask Deployment

### Platform Options for Serverless Flask

#### 1. Vercel (Recommended)
```python
# api/index.py - Main entry point
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow Wix domain

@app.route('/api/workouts', methods=['GET', 'POST'])
def workouts():
    if request.method == 'GET':
        # Return user workouts
        return jsonify({"workouts": []})
    elif request.method == 'POST':
        # Create new workout
        data = request.json
        return jsonify({"success": True, "id": "123"})

# Vercel requires this handler
def handler(event, context):
    return app(event, context)
```

```json
// vercel.json - Configuration
{
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" }
  ]
}
```

#### 2. AWS Lambda + API Gateway  
```python
# lambda_function.py
import json
from your_flask_app import app

def lambda_handler(event, context):
    # Convert AWS Lambda event to Flask request
    response = app.process_request(event)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://yoursite.wix.com',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
```

#### 3. Railway (Simple Deploy)
```dockerfile
# Dockerfile for Railway
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

### Wix Frontend Integration
```javascript
// Wix Code - Call serverless backend
import { fetch } from 'wix-fetch';

export async function createWorkout(workoutData) {
  try {
    const response = await fetch('https://your-api.vercel.app/api/workouts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(workoutData)
    });
    
    return await response.json();
  } catch (error) {
    console.error('Failed to create workout:', error);
    throw error;
  }
}

// Use in Wix page
$w.onReady(function () {
  $w('#submitButton').onClick(async () => {
    const workout = {
      title: $w('#titleInput').value,
      duration: $w('#durationInput').value
    };
    
    try {
      await createWorkout(workout);
      $w('#successMessage').show();
    } catch (error) {
      $w('#errorMessage').show();
    }
  });
});
```

### Database Options for Serverless
1. **Supabase** (PostgreSQL-compatible)
2. **PlanetScale** (MySQL-compatible) 
3. **MongoDB Atlas** (NoSQL)
4. **AWS RDS** (Traditional SQL)

### Cost Comparison
| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| Vercel | 100GB bandwidth | $20/month |
| Railway | $5 credit/month | $5+/month usage |
| AWS Lambda | 1M requests/month | Pay per request |
| Wix Premium | - | $16-35/month |

### Pros of Serverless Approach
✅ Keep existing Flask code (minimal changes)
✅ Wix drag-drop editor for frontend
✅ Serverless scaling (pay for usage)
✅ Multiple hosting options
✅ Can migrate gradually

### Cons of Serverless Approach
❌ More complex architecture
❌ CORS configuration needed
❌ Cold start delays possible
❌ Need to manage two platforms
❌ API endpoint management