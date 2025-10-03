# FitFriendsClubs WordPress Plugin Installation Guide

## Overview
This WordPress plugin provides complete integration with the FitFriendsClubs API, allowing you to display fitness clubs, virtual trails, and dashboard statistics on your WordPress site using shortcodes.

## Features
✅ **Complete API Integration** - Connects to FitFriendsClubs Cloudflare Workers API
✅ **Shortcode Support** - Easy integration with any page or post
✅ **Admin Settings** - Configure API URL, debug mode, and auto-loading
✅ **Responsive Design** - Works on desktop, tablet, and mobile devices
✅ **Modal Popups** - Detailed views for clubs and trails
✅ **Error Handling** - Comprehensive error handling and retry logic
✅ **Debug Mode** - Built-in testing and debugging tools

## Installation

### Method 1: Manual Installation (Recommended)

1. **Download Files**
   - Ensure you have all three files:
     - `fitfriendsclubs-wordpress.php` (Main plugin file)
     - `assets/fitfriendsclubs.css` (Styles)
     - `assets/fitfriendsclubs.js` (JavaScript functionality)

2. **Upload to WordPress**
   - Create a folder named `fitfriendsclubs` in your `/wp-content/plugins/` directory
   - Upload all files maintaining the folder structure:
     ```
     /wp-content/plugins/fitfriendsclubs/
     ├── fitfriendsclubs-wordpress.php
     └── assets/
         ├── fitfriendsclubs.css
         └── fitfriendsclubs.js
     ```

3. **Activate the Plugin**
   - Go to WordPress Admin → Plugins
   - Find "FitFriendsClubs Integration" and click "Activate"

### Method 2: Create as Must-Use Plugin
- Place files in `/wp-content/mu-plugins/fitfriendsclubs/` for automatic activation

## Configuration

1. **Access Settings**
   - Go to WordPress Admin → Settings → FitFriendsClubs

2. **Configure Options**
   - **API URL**: `https://fitfriendsclub-api.darnellroy2.workers.dev` (default)
   - **Debug Mode**: Enable for development, disable for production
   - **Auto Load Content**: Automatically load content when shortcodes are displayed

3. **Test Connection**
   - Click "Test API" button in admin to verify connectivity

## Usage

### Shortcodes

#### Dashboard
```php
[fitfriendsclubs-dashboard]
```
Displays API connection status, system stats, and test interface.

#### Fitness Clubs
```php
[fitfriendsclubs-clubs limit="10"]
```
**Parameters:**
- `limit` - Number of clubs to display (default: 10)
- `show_details` - Enable detail modals (default: true)

#### Virtual Trails
```php
[fitfriendsclubs-trails limit="8" difficulty="all"]
```
**Parameters:**
- `limit` - Number of trails to display (default: 10) 
- `difficulty` - Filter by difficulty: "easy", "moderate", "hard", or "all" (default: all)

#### API Test
```php
[fitfriendsclubs-test]
```
Simple API connectivity test interface.

### Example Page Setup

Create a new page and add:
```php
<h2>FitFriendsClubs Dashboard</h2>
[fitfriendsclubs-dashboard]

<h2>Our Fitness Clubs</h2>
[fitfriendsclubs-clubs limit="6"]

<h2>Virtual Trails</h2>
[fitfriendsclubs-trails limit="4" difficulty="moderate"]
```

## Advanced Usage

### Custom Styling
Add custom CSS to your theme's `style.css`:
```css
/* Customize club cards */
.ff-club-card {
    border-color: #your-brand-color !important;
}

/* Customize loading animation */
.ff-load {
    border-top-color: #your-brand-color !important;
}
```

### JavaScript Integration
Access the plugin's JavaScript API:
```javascript
// Test API connection
window.FitFriendsClubs.runTest();

// Load specific number of clubs
window.FitFriendsClubs.loadClubs(5);

// Load trails by difficulty
window.FitFriendsClubs.loadTrails(10, 'easy');

// Access utilities
window.FitFriendsClubs.utils.showSuccess('Custom message');
```

### Keyboard Shortcuts (Debug Mode)
- **Escape** - Close any open modal
- **Ctrl+T** - Run API test
- **Ctrl+D** - Show debug information in console

## Troubleshooting

### Common Issues

**Plugin not loading?**
- Check file permissions (should be 644 for files, 755 for directories)
- Verify all files are uploaded correctly
- Check WordPress error logs

**API connection failed?**
- Test the API URL directly: `https://fitfriendsclub-api.darnellroy2.workers.dev`
- Check firewall/proxy settings
- Enable debug mode for detailed error messages

**Shortcodes not working?**
- Ensure plugin is activated
- Check for JavaScript errors in browser console
- Verify shortcode syntax is correct

**Styling issues?**
- Check for CSS conflicts with theme
- Use browser developer tools to inspect elements
- Add custom CSS with higher specificity

### Debug Mode
Enable debug mode in settings for:
- Detailed console logging
- API call timing information
- Error stack traces
- Keyboard shortcuts for testing

## API Integration Details

### Endpoints Used
- `GET /` - Health check
- `GET /test/clubs` - Retrieve fitness clubs
- `GET /test/trails` - Retrieve virtual trails  
- `GET /test/all` - Run comprehensive tests

### Data Structure
**Clubs:**
```json
{
  "name": "Morning Runners Club",
  "category": "Running",
  "equipment_type": "Minimal",
  "location": "Virtual",
  "member_count": 150,
  "description": "Early morning running group"
}
```

**Trails:**
```json
{
  "name": "Mountain Peak Trail",
  "location": "Rocky Mountains",
  "difficulty": "Hard",
  "distance_km": 12.5,
  "estimated_time": "3-4 hours",
  "elevation_gain": "High",
  "description": "Challenging mountain trail"
}
```

## Performance Optimization

### Caching
The plugin includes:
- Automatic retry logic for failed requests
- 15-second timeout on API calls
- Error handling to prevent site crashes

### Best Practices
- Use specific limits on shortcodes to avoid loading too much data
- Enable caching plugins for better performance
- Disable debug mode in production
- Consider using a CDN for static assets

## Security

### Data Handling
- All API responses are sanitized
- User inputs are escaped and validated
- CSRF protection using WordPress nonces
- No sensitive data stored in database

### Permissions
- Admin settings require 'manage_options' capability
- Plugin follows WordPress coding standards
- Secure AJAX handling for admin functions

## Updates and Maintenance

### Updating the Plugin
1. Deactivate the current version
2. Replace files with new versions
3. Reactivate the plugin
4. Check settings and test functionality

### Backup Recommendations
- Always backup your site before installing/updating plugins
- Test on staging site first
- Export plugin settings before major updates

## Support and Development

### Custom Development
The plugin structure allows for easy customization:
- Add new shortcode parameters
- Create custom API endpoints
- Extend styling and functionality
- Add multilingual support

### Contributing
- Follow WordPress coding standards
- Test thoroughly before deployment
- Document any changes or additions
- Consider backwards compatibility

## Technical Specifications

### Requirements
- WordPress 5.0 or higher
- PHP 7.4 or higher
- Modern web browser with JavaScript enabled
- Internet connection for API access

### Browser Support
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

### File Structure
```
fitfriendsclubs/
├── fitfriendsclubs-wordpress.php    # Main plugin file
└── assets/
    ├── fitfriendsclubs.css          # Plugin styles
    └── fitfriendsclubs.js           # Plugin JavaScript
```

This WordPress integration provides the same functionality as the Wix version but with the flexibility and power of WordPress, unlimited customization options, and no character limits!