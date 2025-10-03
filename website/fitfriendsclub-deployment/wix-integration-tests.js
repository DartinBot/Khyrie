// FitFriendsClubs Wix Integration Test Suite
// This file tests all the integration functions to ensure they work correctly

class WixIntegrationTester {
    constructor() {
        this.testResults = [];
        this.apiUrl = 'https://fitfriendsclub-api.darnellroy2.workers.dev';
    }

    // Run all tests
    async runAllTests() {
        console.log('🧪 Starting FitFriendsClubs Wix Integration Tests...');
        
        this.testResults = [];
        
        // API Connection Tests
        await this.testApiConnection();
        await this.testClubsEndpoint();
        await this.testTrailsEndpoint();
        await this.testDatabaseConnection();
        
        // Integration Function Tests
        await this.testWixElementPresence();
        await this.testNavigationFunctions();
        await this.testDataDisplayFunctions();
        
        // Auth System Tests
        await this.testAuthSystemInitialization();
        await this.testAuthUIElements();
        
        // Session Management Tests
        await this.testSessionManager();
        
        // Generate test report
        this.generateTestReport();
        
        return this.testResults;
    }

    // Test API connection
    async testApiConnection() {
        try {
            console.log('Testing API connection...');
            
            const response = await fetch(`${this.apiUrl}/`);
            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                this.addTestResult('API Connection', 'PASS', 'API is accessible and responding');
            } else {
                this.addTestResult('API Connection', 'FAIL', `API returned error: ${data.message}`);
            }
        } catch (error) {
            this.addTestResult('API Connection', 'FAIL', `Connection failed: ${error.message}`);
        }
    }

    // Test clubs endpoint
    async testClubsEndpoint() {
        try {
            console.log('Testing clubs endpoint...');
            
            const response = await fetch(`${this.apiUrl}/test/clubs`);
            const data = await response.json();
            
            if (response.ok && data.status === 'success' && data.data && data.data.clubs) {
                this.addTestResult('Clubs Endpoint', 'PASS', `Retrieved ${data.data.clubs.length} clubs`);
            } else {
                this.addTestResult('Clubs Endpoint', 'FAIL', 'Failed to retrieve clubs data');
            }
        } catch (error) {
            this.addTestResult('Clubs Endpoint', 'FAIL', `Error: ${error.message}`);
        }
    }

    // Test trails endpoint
    async testTrailsEndpoint() {
        try {
            console.log('Testing trails endpoint...');
            
            const response = await fetch(`${this.apiUrl}/test/trails`);
            const data = await response.json();
            
            if (response.ok && data.status === 'success' && data.data && data.data.trails) {
                this.addTestResult('Trails Endpoint', 'PASS', `Retrieved ${data.data.trails.length} trails`);
            } else {
                this.addTestResult('Trails Endpoint', 'FAIL', 'Failed to retrieve trails data');
            }
        } catch (error) {
            this.addTestResult('Trails Endpoint', 'FAIL', `Error: ${error.message}`);
        }
    }

    // Test database connection
    async testDatabaseConnection() {
        try {
            console.log('Testing database connection...');
            
            const response = await fetch(`${this.apiUrl}/test/database`);
            const data = await response.json();
            
            if (response.ok && data.status === 'success') {
                this.addTestResult('Database Connection', 'PASS', `Connected with ${data.data.responseTime} response time`);
            } else {
                this.addTestResult('Database Connection', 'FAIL', 'Database connection failed');
            }
        } catch (error) {
            this.addTestResult('Database Connection', 'FAIL', `Error: ${error.message}`);
        }
    }

    // Test Wix element presence
    testWixElementPresence() {
        console.log('Testing Wix element presence...');
        
        const requiredElements = [
            '#homePageContent',
            '#statusIndicator',
            '#loadingIcon',
            '#errorMessage',
            '#clubsContainer',
            '#trailsContainer',
            '#dashboardContainer'
        ];
        
        const missingElements = [];
        const presentElements = [];
        
        requiredElements.forEach(elementId => {
            if (typeof $w === 'undefined') {
                // Not in Wix environment, skip this test
                this.addTestResult('Wix Elements', 'SKIP', 'Not running in Wix environment');
                return;
            }
            
            try {
                const element = $w(elementId);
                if (element) {
                    presentElements.push(elementId);
                } else {
                    missingElements.push(elementId);
                }
            } catch (error) {
                missingElements.push(elementId);
            }
        });
        
        if (missingElements.length === 0) {
            this.addTestResult('Wix Elements', 'PASS', `All ${presentElements.length} required elements found`);
        } else {
            this.addTestResult('Wix Elements', 'WARN', `Missing elements: ${missingElements.join(', ')}`);
        }
    }

    // Test navigation functions
    testNavigationFunctions() {
        console.log('Testing navigation functions...');
        
        const navigationFunctions = [
            'initializeHomepage',
            'loadFitnessClubs',
            'loadVirtualTrails',
            'loadUserDashboard'
        ];
        
        let functionsFound = 0;
        
        navigationFunctions.forEach(funcName => {
            if (typeof window[funcName] === 'function') {
                functionsFound++;
            }
        });
        
        if (functionsFound === navigationFunctions.length) {
            this.addTestResult('Navigation Functions', 'PASS', 'All navigation functions available');
        } else {
            this.addTestResult('Navigation Functions', 'WARN', `${functionsFound}/${navigationFunctions.length} functions found`);
        }
    }

    // Test data display functions
    testDataDisplayFunctions() {
        console.log('Testing data display functions...');
        
        const displayFunctions = [
            'displayFitnessClubs',
            'displayVirtualTrails',
            'updateDashboardStats'
        ];
        
        let functionsFound = 0;
        
        displayFunctions.forEach(funcName => {
            if (typeof window[funcName] === 'function') {
                functionsFound++;
            }
        });
        
        if (functionsFound === displayFunctions.length) {
            this.addTestResult('Display Functions', 'PASS', 'All display functions available');
        } else {
            this.addTestResult('Display Functions', 'WARN', `${functionsFound}/${displayFunctions.length} functions found`);
        }
    }

    // Test auth system initialization
    testAuthSystemInitialization() {
        console.log('Testing auth system...');
        
        if (typeof authSystem !== 'undefined') {
            this.addTestResult('Auth System Init', 'PASS', 'Authentication system initialized');
            
            // Test auth methods
            if (typeof authSystem.isAuthenticated === 'function') {
                this.addTestResult('Auth Methods', 'PASS', 'Auth methods available');
            } else {
                this.addTestResult('Auth Methods', 'FAIL', 'Auth methods missing');
            }
        } else {
            this.addTestResult('Auth System Init', 'FAIL', 'Authentication system not found');
        }
    }

    // Test auth UI elements
    testAuthUIElements() {
        console.log('Testing auth UI elements...');
        
        if (typeof $w === 'undefined') {
            this.addTestResult('Auth UI Elements', 'SKIP', 'Not in Wix environment');
            return;
        }
        
        const authElements = [
            '#loginButton',
            '#registerButton',
            '#logoutButton',
            '#loginModal',
            '#registerModal'
        ];
        
        let elementsFound = 0;
        authElements.forEach(elementId => {
            try {
                if ($w(elementId)) {
                    elementsFound++;
                }
            } catch (error) {
                // Element not found
            }
        });
        
        if (elementsFound >= 3) {
            this.addTestResult('Auth UI Elements', 'PASS', `${elementsFound}/${authElements.length} auth elements found`);
        } else {
            this.addTestResult('Auth UI Elements', 'WARN', `Only ${elementsFound}/${authElements.length} auth elements found`);
        }
    }

    // Test session manager
    testSessionManager() {
        console.log('Testing session manager...');
        
        if (typeof sessionManager !== 'undefined') {
            this.addTestResult('Session Manager', 'PASS', 'Session manager available');
            
            // Test session methods
            const requiredMethods = ['startSession', 'endSession', 'startSessionTimer'];
            let methodsFound = 0;
            
            requiredMethods.forEach(method => {
                if (typeof sessionManager[method] === 'function') {
                    methodsFound++;
                }
            });
            
            if (methodsFound === requiredMethods.length) {
                this.addTestResult('Session Methods', 'PASS', 'All session methods available');
            } else {
                this.addTestResult('Session Methods', 'WARN', `${methodsFound}/${requiredMethods.length} methods found`);
            }
        } else {
            this.addTestResult('Session Manager', 'FAIL', 'Session manager not found');
        }
    }

    // Add test result
    addTestResult(testName, status, message) {
        this.testResults.push({
            test: testName,
            status: status,
            message: message,
            timestamp: new Date().toISOString()
        });
        
        // Log to console
        const statusSymbol = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
        console.log(`${statusSymbol} ${testName}: ${message}`);
    }

    // Generate test report
    generateTestReport() {
        const passed = this.testResults.filter(r => r.status === 'PASS').length;
        const failed = this.testResults.filter(r => r.status === 'FAIL').length;
        const warnings = this.testResults.filter(r => r.status === 'WARN').length;
        const skipped = this.testResults.filter(r => r.status === 'SKIP').length;
        
        console.log('\n📊 Test Report Summary:');
        console.log(`✅ Passed: ${passed}`);
        console.log(`❌ Failed: ${failed}`);
        console.log(`⚠️ Warnings: ${warnings}`);
        console.log(`⏭️ Skipped: ${skipped}`);
        console.log(`📈 Total: ${this.testResults.length}`);
        
        // Show in Wix UI if available
        if (typeof $w !== 'undefined' && $w('#testResults')) {
            this.displayTestResultsInWix();
        }
        
        return {
            summary: { passed, failed, warnings, skipped, total: this.testResults.length },
            details: this.testResults
        };
    }

    // Display test results in Wix UI
    displayTestResultsInWix() {
        try {
            if ($w('#testResultsRepeater')) {
                const testData = this.testResults.map((result, index) => ({
                    _id: `test-${index}`,
                    testName: result.test,
                    status: result.status,
                    message: result.message,
                    statusColor: this.getStatusColor(result.status)
                }));
                
                $w('#testResultsRepeater').data = testData;
                
                $w('#testResultsRepeater').onItemReady(($item, itemData) => {
                    $item('#testNameText').text = itemData.testName;
                    $item('#testStatusText').text = itemData.status;
                    $item('#testMessageText').text = itemData.message;
                    $item('#testStatusText').style.color = itemData.statusColor;
                });
            }
            
            // Update summary
            const summary = this.generateTestReport();
            if ($w('#testSummaryText')) {
                $w('#testSummaryText').text = 
                    `Tests: ${summary.summary.passed} passed, ${summary.summary.failed} failed, ${summary.summary.warnings} warnings`;
            }
        } catch (error) {
            console.error('Failed to display test results in Wix:', error);
        }
    }

    // Get status color for UI
    getStatusColor(status) {
        switch (status) {
            case 'PASS': return '#4CAF50';
            case 'FAIL': return '#F44336';
            case 'WARN': return '#FF9800';
            case 'SKIP': return '#9E9E9E';
            default: return '#000000';
        }
    }
}

// Integration Test Runner for Wix
function runWixIntegrationTests() {
    const tester = new WixIntegrationTester();
    return tester.runAllTests();
}

// Quick API connectivity test
async function quickApiTest() {
    try {
        const response = await fetch('https://fitfriendsclub-api.darnellroy2.workers.dev/test/all');
        const data = await response.json();
        
        console.log('🚀 Quick API Test Result:', data);
        
        if (typeof $w !== 'undefined' && $w('#quickTestResult')) {
            $w('#quickTestResult').text = 
                data.status === 'success' ? 'API Connection: ✅ Working' : 'API Connection: ❌ Failed';
        }
        
        return data;
    } catch (error) {
        console.error('Quick API test failed:', error);
        
        if (typeof $w !== 'undefined' && $w('#quickTestResult')) {
            $w('#quickTestResult').text = 'API Connection: ❌ Error';
        }
        
        return { status: 'error', message: error.message };
    }
}

// Manual test functions for debugging

// Test club loading manually
async function testClubLoading() {
    console.log('🧪 Manual Club Loading Test');
    try {
        if (typeof loadFitnessClubs === 'function') {
            await loadFitnessClubs();
            console.log('✅ Club loading completed');
        } else {
            console.log('❌ loadFitnessClubs function not found');
        }
    } catch (error) {
        console.log('❌ Club loading failed:', error);
    }
}

// Test trail loading manually
async function testTrailLoading() {
    console.log('🧪 Manual Trail Loading Test');
    try {
        if (typeof loadVirtualTrails === 'function') {
            await loadVirtualTrails();
            console.log('✅ Trail loading completed');
        } else {
            console.log('❌ loadVirtualTrails function not found');
        }
    } catch (error) {
        console.log('❌ Trail loading failed:', error);
    }
}

// Test authentication flow
function testAuthFlow() {
    console.log('🧪 Manual Auth Flow Test');
    try {
        if (typeof authSystem !== 'undefined') {
            console.log('Auth system status:', authSystem.isAuthenticated() ? 'Logged in' : 'Not logged in');
            console.log('Current user:', authSystem.getCurrentUser());
            console.log('✅ Auth system accessible');
        } else {
            console.log('❌ Auth system not found');
        }
    } catch (error) {
        console.log('❌ Auth test failed:', error);
    }
}

// Export test functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        WixIntegrationTester,
        runWixIntegrationTests,
        quickApiTest,
        testClubLoading,
        testTrailLoading,
        testAuthFlow
    };
} else if (typeof window !== 'undefined') {
    // Browser environment
    window.runWixIntegrationTests = runWixIntegrationTests;
    window.quickApiTest = quickApiTest;
    window.testClubLoading = testClubLoading;
    window.testTrailLoading = testTrailLoading;
    window.testAuthFlow = testAuthFlow;
}

// Auto-run quick test when page loads (if in Wix)
if (typeof $w !== 'undefined') {
    $w.onReady(() => {
        console.log('🔧 FitFriendsClubs Integration Loaded - Running quick test...');
        setTimeout(() => {
            quickApiTest();
        }, 2000); // Wait 2 seconds for everything to load
    });
}