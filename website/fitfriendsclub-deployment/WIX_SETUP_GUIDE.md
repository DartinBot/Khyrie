# FitFriendsClubs Wix Site Structure Guide

## Overview
This guide shows you exactly what elements to create in your Wix editor to work with the JavaScript integration code.

## Required Pages

### 1. Homepage (/)
**Elements needed:**
- `#homePageContent` - Main container for homepage content
- `#statusIndicator` - Text element for API connection status
- `#loadingIcon` - Loading animation/icon
- `#errorMessage` - Text element for error messages
- `#clubCountText` - Text showing number of clubs
- `#trailCountText` - Text showing number of trails  
- `#platformStatusText` - Overall platform status

**Navigation buttons:**
- `#homeButton` - Home navigation
- `#clubsButton` - Clubs page navigation
- `#trailsButton` - Trails page navigation
- `#dashboardButton` - Dashboard navigation

### 2. Clubs Page (/clubs)
**Elements needed:**
- `#clubsContainer` - Main container for clubs content
- `#clubsRepeater` - Wix repeater element for displaying clubs
- `#clubDetailsLightbox` - Lightbox for club details

**Repeater item elements (inside #clubsRepeater):**
- `#clubContainer` - Clickable container for each club
- `#clubNameText` - Club name
- `#clubCategoryText` - Club category
- `#equipmentTypeText` - Equipment type

**Lightbox elements (inside #clubDetailsLightbox):**
- `#clubDetailsTitle` - Club name in details
- `#clubDetailsCategory` - Category details
- `#clubDetailsEquipment` - Equipment details
- `#clubDetailsDescription` - Club description

### 3. Trails Page (/trails)
**Elements needed:**
- `#trailsContainer` - Main container for trails content
- `#trailsRepeater` - Wix repeater element for displaying trails
- `#trailDetailsLightbox` - Lightbox for trail details

**Repeater item elements (inside #trailsRepeater):**
- `#trailContainer` - Clickable container for each trail
- `#trailNameText` - Trail name
- `#locationText` - Trail location
- `#difficultyText` - Trail difficulty
- `#distanceText` - Trail distance

**Lightbox elements (inside #trailDetailsLightbox):**
- `#trailDetailsTitle` - Trail name in details
- `#trailDetailsLocation` - Location details
- `#trailDetailsDifficulty` - Difficulty details
- `#trailDetailsDistance` - Distance details
- `#trailDetailsDescription` - Trail description

### 4. Dashboard Page (/dashboard)
**Elements needed:**
- `#dashboardContainer` - Main container for dashboard
- `#dashboardStats` - Stats container
- `#dashboardRepeater` - Repeater for system status items

**Repeater item elements (inside #dashboardRepeater):**
- `#testNameText` - Test name
- `#statusText` - Status text
- `#messageText` - Status message

## Wix Editor Setup Instructions

### Step 1: Create Pages
1. Create 4 pages in Wix: Home, Clubs, Trails, Dashboard
2. Set URLs: `/`, `/clubs`, `/trails`, `/dashboard`

### Step 2: Add Elements to Each Page

#### Homepage Layout:
```
Header
├── Navigation Menu (buttons: Home, Clubs, Trails, Dashboard)
└── Status Indicator (#statusIndicator)

Main Content (#homePageContent)
├── Hero Section
│   ├── Title: "FitFriendsClubs"
│   ├── Subtitle: "Premium Virtual Fitness Experience"
│   └── Stats Row
│       ├── Club Count (#clubCountText)
│       ├── Trail Count (#trailCountText)
│       └── Platform Status (#platformStatusText)
├── Features Section
└── Call-to-Action Buttons

Footer

Global Elements:
├── Loading Icon (#loadingIcon) - Hidden by default
└── Error Message (#errorMessage) - Hidden by default
```

#### Clubs Page Layout:
```
Header (same navigation)

Main Content (#clubsContainer)
├── Page Title: "Premium Fitness Clubs"
├── Clubs Repeater (#clubsRepeater)
│   └── Club Item Template
│       ├── Club Container (#clubContainer) - Clickable
│       ├── Club Name (#clubNameText)
│       ├── Category (#clubCategoryText)
│       └── Equipment Type (#equipmentTypeText)

Lightbox (#clubDetailsLightbox)
├── Close Button
├── Club Title (#clubDetailsTitle)
├── Category (#clubDetailsCategory)
├── Equipment (#clubDetailsEquipment)
└── Description (#clubDetailsDescription)
```

#### Trails Page Layout:
```
Header (same navigation)

Main Content (#trailsContainer)
├── Page Title: "Virtual Trails"
├── Trails Repeater (#trailsRepeater)
│   └── Trail Item Template
│       ├── Trail Container (#trailContainer) - Clickable
│       ├── Trail Name (#trailNameText)
│       ├── Location (#locationText)
│       ├── Difficulty (#difficultyText)
│       └── Distance (#distanceText)

Lightbox (#trailDetailsLightbox)
├── Close Button
├── Trail Title (#trailDetailsTitle)
├── Location (#trailDetailsLocation)
├── Difficulty (#trailDetailsDifficulty)
├── Distance (#trailDetailsDistance)
└── Description (#trailDetailsDescription)
```

#### Dashboard Page Layout:
```
Header (same navigation)

Main Content (#dashboardContainer)
├── Page Title: "System Dashboard"
├── Dashboard Stats (#dashboardStats)
└── Status Repeater (#dashboardRepeater)
    └── Status Item Template
        ├── Test Name (#testNameText)
        ├── Status (#statusText) - Color-coded
        └── Message (#messageText)
```

### Step 3: Add JavaScript Code
1. Go to your Wix site's dashboard
2. Navigate to Settings > Custom Code
3. Add the `wix-integration.js` code to the site
4. Set it to load on all pages

### Step 4: Configure Element IDs
1. Select each element in the Wix editor
2. In the properties panel, set the ID to match the ones listed above
3. Make sure IDs are exactly as shown (including the # symbol in your references)

### Step 5: Test Integration
1. Preview your site
2. Open browser console (F12)
3. Look for "FitFriendsClubs Wix site loaded!" message
4. Check for any API connection messages
5. Navigate between pages to test functionality

## Styling Recommendations

### Color Scheme:
- Primary: #4CAF50 (Green - for success states)
- Secondary: #2196F3 (Blue - for actions)
- Error: #F44336 (Red - for errors)
- Warning: #FF9800 (Orange - for warnings)
- Background: #FAFAFA (Light gray)

### Fonts:
- Headlines: Bold, modern sans-serif
- Body text: Clean, readable font
- Status text: Monospace for technical info

### Layout:
- Use cards/containers for repeater items
- Add hover effects on clickable elements
- Ensure mobile responsiveness
- Include loading states and error handling

## API Endpoints Available:
- `/` - Health check and API info
- `/test/clubs` - Get fitness clubs data
- `/test/trails` - Get virtual trails data  
- `/test/database` - Database connection test
- `/test/all` - Run comprehensive tests
- `/debug/env` - Environment variables check

## Next Steps:
1. Create the Wix site with these elements
2. Add the JavaScript integration code
3. Test all functionality
4. Style the site to match your brand
5. Add user authentication (optional advanced feature)

Your API is live at: https://fitfriendsclub-api.darnellroy2.workers.dev