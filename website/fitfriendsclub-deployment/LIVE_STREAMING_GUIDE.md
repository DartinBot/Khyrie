# Live Video Streaming for Group Sessions

## 🎥 **Overview**

FitFriendsClubs now supports **live video streaming** for group workout sessions! Instructors can broadcast their workouts in real-time while participants join from anywhere in the world. This creates an immersive, interactive fitness experience with live chat, real-time motivation, and community engagement.

## ✨ **Features**

### 🎬 **Live Streaming Capabilities**
- **HD/4K Video Quality** - Crisp, clear video for detailed instruction
- **Real-time Audio** - Crystal clear instructor guidance and motivational coaching
- **Multi-device Support** - Stream from phones, tablets, computers, or professional cameras
- **Low Latency** - Near real-time interaction between instructor and participants

### 👥 **Interactive Experience**
- **Live Chat** - Real-time messaging during workouts
- **Viewer Count** - See how many people are working out together
- **Participant Notifications** - Automatic alerts when streams start
- **Club Member Only** - Exclusive access for fitness club members

### 📊 **Stream Management**
- **Stream Analytics** - Track viewer engagement and session metrics
- **Capacity Control** - Set maximum viewer limits per stream
- **Session Integration** - Seamlessly integrated with group workout sessions
- **Quality Adaptation** - Automatic quality adjustment based on connection

## 🔌 **API Endpoints**

### **Create Streaming Session**
```http
POST /api/streaming/sessions
Content-Type: application/json
Authorization: Bearer <token>

{
  "group_session_id": 123,
  "stream_title": "HIIT Cardio Blast - Live Workout",
  "stream_description": "High-intensity interval training with bodyweight exercises",
  "max_viewers": 50,
  "stream_quality": "HD"
}
```

**Response:**
```json
{
  "success": true,
  "streaming_session": {
    "id": 456,
    "stream_key": "abc123-def456",
    "room_id": "room-xyz789"
  },
  "stream_config": {
    "rtmp_url": "rtmp://live.fitfriendsclubs.com/live/abc123-def456",
    "webrtc_url": "wss://stream.fitfriendsclubs.com/webrtc/room-xyz789",
    "hls_url": "https://stream.fitfriendsclubs.com/hls/room-xyz789/playlist.m3u8"
  }
}
```

### **Start Live Stream**
```http
POST /api/streaming/sessions/456/start
Authorization: Bearer <token>
```

### **Join Stream as Viewer**
```http
POST /api/streaming/sessions/456/join  
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "stream_urls": {
    "hls_url": "https://stream.fitfriendsclubs.com/hls/room-xyz789/playlist.m3u8",
    "webrtc_url": "wss://stream.fitfriendsclubs.com/webrtc/room-xyz789",
    "chat_url": "wss://chat.fitfriendsclubs.com/room/room-xyz789"
  },
  "stream_info": {
    "title": "HIIT Cardio Blast - Live Workout",
    "viewer_count": 23
  }
}
```

### **Get Stream Details**
```http
GET /api/streaming/sessions/456
Authorization: Bearer <token>
```

### **Get Streaming Token**
```http
POST /api/streaming/token
Content-Type: application/json
Authorization: Bearer <token>

{
  "room_id": "room-xyz789",
  "role": "viewer"
}
```

## 🛠 **Implementation Guide**

### **1. Instructor Setup (Streaming)**

#### **Mobile App Streaming**
```javascript
// Connect to streaming session
const streamResponse = await fetch('/api/streaming/sessions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    group_session_id: sessionId,
    stream_title: 'Morning Yoga Flow',
    max_viewers: 30
  })
});

const { streaming_session, stream_config } = await streamResponse.json();

// Start camera and microphone
const stream = await navigator.mediaDevices.getUserMedia({ 
  video: { width: 1280, height: 720 }, 
  audio: true 
});

// Connect to WebRTC for live streaming
const peerConnection = new RTCPeerConnection({
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'turn:turn.fitfriendsclubs.com:3478' }
  ]
});

stream.getTracks().forEach(track => {
  peerConnection.addTrack(track, stream);
});
```

#### **Professional Camera Setup (RTMP)**
```bash
# Using OBS Studio or similar streaming software
RTMP URL: rtmp://live.fitfriendsclubs.com/live/
Stream Key: abc123-def456

# Or using FFmpeg
ffmpeg -f v4l2 -i /dev/video0 -f alsa -i default \
  -c:v libx264 -preset veryfast -b:v 2500k \
  -c:a aac -b:a 128k \
  -f flv rtmp://live.fitfriendsclubs.com/live/abc123-def456
```

### **2. Participant Setup (Viewing)**

#### **Web Browser Viewing**
```javascript
// Join streaming session
const joinResponse = await fetch(`/api/streaming/sessions/${sessionId}/join`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});

const { stream_urls } = await joinResponse.json();

// Load HLS stream for web playback
const video = document.getElementById('stream-video');
if (Hls.isSupported()) {
  const hls = new Hls();
  hls.loadSource(stream_urls.hls_url);
  hls.attachMedia(video);
} else if (video.canPlayType('application/vnd.apple.mpegurl')) {
  video.src = stream_urls.hls_url;
}

// Connect to live chat
const chatSocket = new WebSocket(stream_urls.chat_url);
chatSocket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  displayChatMessage(message);
};
```

#### **Mobile App Viewing**
```javascript
// React Native example
import Video from 'react-native-video';

<Video
  source={{ uri: stream_urls.hls_url }}
  style={styles.video}
  controls={true}
  resizeMode="contain"
  onLoad={() => console.log('Stream loaded')}
  onError={(error) => console.log('Stream error:', error)}
/>
```

### **3. Live Chat Integration**
```javascript
// Send chat message
const sendMessage = (message) => {
  chatSocket.send(JSON.stringify({
    type: 'chat_message',
    message: message,
    user_id: currentUserId,
    timestamp: Date.now()
  }));
};

// Receive and display messages
const displayChatMessage = (messageData) => {
  const chatContainer = document.getElementById('chat-messages');
  const messageElement = document.createElement('div');
  messageElement.innerHTML = `
    <span class="username">${messageData.username}</span>: 
    <span class="message">${messageData.message}</span>
  `;
  chatContainer.appendChild(messageElement);
  chatContainer.scrollTop = chatContainer.scrollHeight;
};
```

## 🏗 **Technical Architecture**

### **Streaming Infrastructure**
- **RTMP Ingest** - Receive streams from broadcasting software
- **WebRTC** - Low-latency browser-to-browser streaming  
- **HLS Distribution** - Scalable video delivery for viewers
- **Edge CDN** - Global content delivery network
- **Chat Server** - Real-time WebSocket messaging

### **Video Quality Options**
- **4K** - 3840x2160 @ 30fps (4-8 Mbps)
- **HD** - 1280x720 @ 30fps (2-4 Mbps)  
- **SD** - 854x480 @ 30fps (1-2 Mbps)
- **Auto** - Adaptive bitrate based on connection

### **Supported Devices**
- **Instructor Broadcasting**: Smartphones, tablets, webcams, professional cameras
- **Viewer Playback**: Web browsers, mobile apps, smart TVs, tablets

## 📱 **User Experience Flow**

### **For Instructors:**
1. Create group workout session in fitness club
2. Set up live streaming for the session
3. Start broadcasting from device/camera
4. Interact with participants via live chat
5. Monitor viewer count and engagement
6. End stream when workout completes

### **For Participants:**
1. Join fitness club and group session
2. Receive notification when stream goes live
3. Click to join live stream
4. Watch instructor in real-time
5. Chat with other participants
6. Follow along with workout

## 🔒 **Security & Privacy**

- **Club Member Only** - Streams limited to fitness club members
- **Encrypted Connections** - All video/audio encrypted in transit
- **Secure Tokens** - Time-limited access tokens for stream access
- **Content Moderation** - Chat filtering and reporting tools
- **GDPR Compliant** - Privacy controls and data protection

## 📊 **Analytics & Insights**

### **Stream Metrics**
- Total viewers per session
- Peak concurrent viewers  
- Average watch time
- Chat engagement rate
- Geographic viewer distribution

### **Instructor Dashboard**
- Live viewer count
- Real-time chat activity
- Session recording options
- Performance analytics
- Engagement insights

## 🚀 **Deployment Requirements**

### **Infrastructure Setup**
```bash
# Required services for full streaming functionality
- RTMP server (Nginx with RTMP module)
- WebRTC signaling server  
- HLS packaging and distribution
- WebSocket chat server
- TURN/STUN servers for NAT traversal
```

### **Environment Variables**
```bash
TURN_SERVER_SECRET=your_turn_server_secret
STREAMING_CDN_URL=https://stream.fitfriendsclubs.com
CHAT_SERVER_URL=wss://chat.fitfriendsclubs.com
```

## 💡 **Usage Examples**

### **Morning Yoga Class**
```
Title: "Sunrise Yoga Flow - Live from Bali"  
Description: "Start your day with gentle stretches and mindfulness"
Max Viewers: 25
Quality: HD
Duration: 45 minutes
```

### **HIIT Training Session**  
```
Title: "30-Min Fat Burning HIIT - No Equipment Needed"
Description: "High-intensity bodyweight workout for all fitness levels"
Max Viewers: 50  
Quality: HD
Duration: 30 minutes
```

### **Strength Training Workshop**
```
Title: "Proper Deadlift Form Masterclass"
Description: "Learn perfect technique with detailed instruction"
Max Viewers: 15
Quality: 4K (for detailed form viewing)
Duration: 60 minutes
```

---

**Ready to go live?** Set up your streaming infrastructure and start broadcasting immersive fitness experiences to your FitFriendsClubs community! 🎥💪