# FitFriendsClubs Wix Integration - Installation Guide

## 📁 File Structure Overview

Your Wix integration is now broken down into three optimized sections:

### 1. **HEAD Section** (`wix-head-section.html`)
- **Location**: Settings → Custom Code → Add to HEAD
- **Purpose**: Early loading configuration, styles, and API settings
- **Contains**: CSS styles, configuration object, feature flags

### 2. **BODY Section** (`wix-body-section.js`)
- **Location**: Site Code → Site tab (for all pages) OR individual Page Code
- **Purpose**: Main application logic and API integration
- **Contains**: API class, data loading, display functions, main $w.onReady()

### 3. **END Section** (`wix-end-section.html`)
- **Location**: Settings → Custom Code → Add to END of BODY
- **Purpose**: Utilities, lightboxes, error handling, cleanup
- **Contains**: Utility functions, lightbox controls, debugging tools

## 🚀 Installation Steps

### Step 1: Install HEAD Section
1. Go to **Settings** → **Custom Code**
2. Click **+ Add Custom Code**
3. Name: `FitFriendsClubs HEAD`
4. Select **All Pages**
5. Choose **Head**
6. Copy entire content from `wix-head-section.html`
7. Click **Apply**

### Step 2: Install BODY Section
1. Go to **Site Structure** → **Site Code**
2. Click on **Site** tab (for site-wide) OR go to specific page
3. Copy entire content from `wix-body-section.js`
4. Paste into the code editor
5. Save

### Step 3: Install END Section
1. Go to **Settings** → **Custom Code**
2. Click **+ Add Custom Code**
3. Name: `FitFriendsClubs END`
4. Select **All Pages**
5. Choose **Body - end**
6. Copy entire content from `wix-end-section.html`
7. Click **Apply**

## ⚙️ Configuration Options

### In HEAD Section (`window.FitFriendsConfig`):

```javascript
// API Configuration
API_URL: 'https://fitfriendsclub-api.darnellroy2.workers.dev'

// Debug Settings
DEBUG_MODE: true  // Set to false for production

// Feature Flags
FEATURES: {
    CLUBS: true,        // Enable clubs functionality
    TRAILS: true,       // Enable trails functionality
    DASHBOARD: true,    // Enable dashboard
    LIGHTBOXES: true,   // Enable detail popups
    AUTO_REFRESH: false // Auto-refresh API status
}
```

## 🎯 Required Wix Elements

### For All Pages:
- `#loadingIcon` - Loading spinner
- `#errorMessage` - Error display
- `#statusIndicator` - API status display

### For Navigation:
- `#homeButton` - Home navigation
- `#clubsButton` - Clubs page navigation
- `#trailsButton` - Trails page navigation
- `#dashboardButton` - Dashboard navigation
- `#testApiButton` - API testing button

### For Homepage:
- `#clubCountText` - Display club count
- `#trailCountText` - Display trail count
- `#platformStatusText` - System status

### For Clubs Page:
- `#clubsContainer` - Clubs page container
- `#clubsRepeater` - Clubs data repeater
  - `#clubNameText` - Club name in repeater
  - `#clubCategoryText` - Club category in repeater
  - `#equipmentTypeText` - Equipment type in repeater
  - `#clubContainer` - Clickable club container

### For Trails Page:
- `#trailsContainer` - Trails page container
- `#trailsRepeater` - Trails data repeater
  - `#trailNameText` - Trail name in repeater
  - `#locationText` - Trail location in repeater
  - `#difficultyText` - Trail difficulty in repeater
  - `#distanceText` - Trail distance in repeater
  - `#trailContainer` - Clickable trail container

### For Dashboard Page:
- `#dashboardContainer` - Dashboard container
- `#dashboardRepeater` - Dashboard data repeater
  - `#testNameText` - Test name in repeater
  - `#statusText` - Test status in repeater
  - `#messageText` - Test message in repeater

### For Lightboxes (Optional):
- `#clubDetailsLightbox` - Club details popup
  - `#clubDetailsTitle` - Club title
  - `#clubDetailsCategory` - Club category
  - `#clubDetailsEquipment` - Club equipment
  - `#clubDetailsDescription` - Club description
  - `#closeClubDetails` - Close button

- `#trailDetailsLightbox` - Trail details popup
  - `#trailDetailsTitle` - Trail title
  - `#trailDetailsLocation` - Trail location
  - `#trailDetailsDifficulty` - Trail difficulty
  - `#trailDetailsDistance` - Trail distance
  - `#trailDetailsDescription` - Trail description
  - `#closeTrailDetails` - Close button

## 🧪 Testing & Debug Features

### Console Commands:
- `testFitFriendsAPI()` - Run full API test
- `FitFriendsClubs.loadClubs()` - Load clubs data
- `FitFriendsClubs.loadTrails()` - Load trails data
- `FitFriendsClubs.test()` - Quick API test

### Keyboard Shortcuts (Debug Mode):
- **Escape** - Close lightboxes
- **Ctrl/Cmd + T** - Quick API test

### Debug Panel:
- Shows in bottom-left when `DEBUG_MODE: true`
- Displays API status and last update time
- Includes quick test button

## 🎨 Styling Classes

### Status Classes:
- `.fitfriends-status-online` - Green online status
- `.fitfriends-status-offline` - Red offline status
- `.fitfriends-error` - Error message styling
- `.fitfriends-success` - Success message styling

### Component Classes:
- `.fitfriends-loading` - Loading spinner animation
- `.fitfriends-card` - Card component with hover effects
- `.fitfriends-badge` - Badge component
- `.fitfriends-difficulty-easy/moderate/hard` - Difficulty badges

## 📊 Performance Features

### Loading States:
- Automatic loading indicators
- Timeout protection (10-second default)
- Retry mechanism (3 attempts default)

### Error Handling:
- Global error boundary
- API error recovery
- User-friendly error messages
- Debug mode detailed errors

### Optimization:
- Feature flags for selective loading
- Performance monitoring in debug mode
- Auto-refresh capabilities
- Keyboard shortcuts for testing

## 🔧 Production Deployment

### Before Going Live:
1. Set `DEBUG_MODE: false` in HEAD section
2. Set `AUTO_REFRESH: false` unless needed
3. Test all pages and functionalities
4. Verify API connectivity
5. Test mobile responsiveness

### Performance Tips:
- Keep `LIGHTBOXES: true` only if using detail popups
- Enable `AUTO_REFRESH` only for high-activity sites
- Monitor console for any errors in production

## 🆘 Troubleshooting

### Common Issues:
1. **API not connecting**: Check `API_URL` in configuration
2. **Elements not found**: Verify element IDs match your Wix design
3. **Data not loading**: Check browser console for errors
4. **Styling issues**: Ensure HEAD section loaded properly

### Debug Steps:
1. Enable `DEBUG_MODE: true`
2. Open browser console
3. Run `testFitFriendsAPI()`
4. Check debug panel information
5. Verify all three sections are installed

Your FitFriendsClubs Wix integration is now modular, optimized, and production-ready! 🎉