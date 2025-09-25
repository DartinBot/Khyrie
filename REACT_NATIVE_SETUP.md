# 🚀 React Native Project Setup Guide
*Step-by-step guide to initialize your Khyrie mobile app*

## 📋 **Prerequisites**

### **macOS Setup (for iOS development)**
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js (use LTS version)
brew install node

# Install Watchman (file watching service)
brew install watchman

# Install Xcode from App Store
# Install Xcode Command Line Tools
xcode-select --install

# Install CocoaPods (iOS dependency manager)
sudo gem install cocoapods
```

### **Development Environment**
```bash
# Verify installations
node --version        # Should be 18.x or higher
npm --version         # Should be 9.x or higher
watchman --version    # Should be 2023.x or higher
xcode-select -p       # Should show Xcode path

# Install React Native CLI globally
npm install -g @react-native-community/cli

# Verify React Native installation
npx react-native --version
```

---

## 🏗 **Project Initialization**

### **Step 1: Create New React Native Project**
```bash
# Navigate to your development directory
cd "/Users/darnellamcguire/Khyrie3.0/src/fitness_mcp/fitness app/fitness app2.0/fitness app 3.0"

# Create React Native project with TypeScript template
npx react-native init KhyrieApp --template react-native-template-typescript

# Navigate to project directory
cd KhyrieApp
```

### **Step 2: Install Essential Dependencies**
```bash
# Navigation libraries
npm install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/stack
npm install react-native-screens react-native-safe-area-context

# UI Components and Icons
npm install react-native-vector-icons react-native-elements
npm install react-native-gesture-handler react-native-reanimated

# Storage and Device Info
npm install @react-native-async-storage/async-storage
npm install react-native-keychain react-native-device-info

# HTTP and API
npm install axios react-query
npm install @react-native-community/netinfo

# State Management
npm install @reduxjs/toolkit react-redux redux-persist

# For iOS - install CocoaPods dependencies
cd ios && pod install && cd ..
```

### **Step 3: Configure Project Structure**
```bash
# Create organized folder structure
mkdir -p src/{components,screens,services,utils,hooks,types,store,assets}
mkdir -p src/screens/{Dashboard,Workouts,Family,Trainers,Profile,Auth}
mkdir -p src/components/{common,forms,workout,family}
mkdir -p src/services/{api,storage,notifications}
mkdir -p assets/{images,fonts,icons}

# Create index files for clean imports
touch src/components/index.ts
touch src/screens/index.ts
touch src/services/index.ts
touch src/utils/index.ts
```

---

## 🎨 **Basic App Structure**

### **App.tsx - Main Application Component**
```typescript
import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {Provider} from 'react-redux';
import {QueryClient, QueryClientProvider} from 'react-query';
import {store} from './src/store';
import {AppNavigator} from './src/navigation/AppNavigator';
import {StatusBar} from 'react-native';

const queryClient = new QueryClient();

const App = (): JSX.Element => {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <NavigationContainer>
          <StatusBar barStyle="dark-content" />
          <AppNavigator />
        </NavigationContainer>
      </QueryClientProvider>
    </Provider>
  );
};

export default App;
```

### **Navigation Structure - src/navigation/AppNavigator.tsx**
```typescript
import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createStackNavigator} from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialIcons';

// Import screens (to be created)
import DashboardScreen from '../screens/Dashboard/DashboardScreen';
import WorkoutsScreen from '../screens/Workouts/WorkoutsScreen';
import FamilyScreen from '../screens/Family/FamilyScreen';
import TrainersScreen from '../screens/Trainers/TrainersScreen';
import ProfileScreen from '../screens/Profile/ProfileScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Main Tab Navigator
const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({route}) => ({
        tabBarIcon: ({focused, color, size}) => {
          let iconName: string;

          switch (route.name) {
            case 'Dashboard':
              iconName = 'dashboard';
              break;
            case 'Workouts':
              iconName = 'fitness-center';
              break;
            case 'Family':
              iconName = 'people';
              break;
            case 'Trainers':
              iconName = 'school';
              break;
            case 'Profile':
              iconName = 'person';
              break;
            default:
              iconName = 'help';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#667eea',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}>
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Workouts" component={WorkoutsScreen} />
      <Tab.Screen name="Family" component={FamilyScreen} />
      <Tab.Screen name="Trainers" component={TrainersScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
};

// App Navigator with Stack Navigation
export const AppNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown: false}}>
      <Stack.Screen name="Main" component={TabNavigator} />
      {/* Add modal screens here later */}
    </Stack.Navigator>
  );
};
```

---

## 🔧 **Configuration Files**

### **Metro Configuration - metro.config.js**
```javascript
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 */
const config = {
  resolver: {
    assetExts: ['bin', 'txt', 'jpg', 'png', 'json', 'mp4', 'ttf', 'otf', 'woff', 'woff2'],
  },
  transformer: {
    getTransformOptions: async () => ({
      transform: {
        experimentalImportSupport: false,
        inlineRequires: true,
      },
    }),
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

### **TypeScript Configuration - tsconfig.json**
```json
{
  "extends": "@tsconfig/react-native/tsconfig.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@screens/*": ["src/screens/*"],
      "@services/*": ["src/services/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"],
      "@assets/*": ["assets/*"]
    }
  },
  "include": [
    "src/**/*",
    "**/*.ts",
    "**/*.tsx"
  ],
  "exclude": [
    "node_modules",
    "android",
    "ios"
  ]
}
```

---

## 📱 **Basic Screen Templates**

### **Dashboard Screen - src/screens/Dashboard/DashboardScreen.tsx**
```typescript
import React from 'react';
import {View, Text, StyleSheet, ScrollView} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';

const DashboardScreen: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>🏋️ Khyrie Dashboard</Text>
        <Text style={styles.subtitle}>Welcome to your fitness journey!</Text>
        
        {/* Dashboard components will go here */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Today's Workout</Text>
          <Text style={styles.cardText}>AI-Generated Upper Body Strength</Text>
        </View>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Family Activity</Text>
          <Text style={styles.cardText}>3 family members worked out today</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  content: {
    padding: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1a202c',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#4a5568',
    marginBottom: 24,
  },
  card: {
    backgroundColor: 'white',
    padding: 16,
    marginBottom: 12,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#2d3748',
    marginBottom: 4,
  },
  cardText: {
    fontSize: 14,
    color: '#718096',
  },
});

export default DashboardScreen;
```

### **Store Configuration - src/store/index.ts**
```typescript
import {configureStore} from '@reduxjs/toolkit';
import {persistStore, persistReducer} from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {combineReducers} from 'redux';

// Import reducers (to be created)
// import authSlice from './slices/authSlice';
// import workoutSlice from './slices/workoutSlice';
// import familySlice from './slices/familySlice';

const persistConfig = {
  key: 'root',
  storage: AsyncStorage,
  whitelist: ['auth', 'user'], // Only persist these reducers
};

const rootReducer = combineReducers({
  // auth: authSlice.reducer,
  // workout: workoutSlice.reducer,
  // family: familySlice.reducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

---

## 🎯 **Testing the Setup**

### **Run the Application**
```bash
# Start Metro bundler
npx react-native start

# Run on iOS simulator (in a new terminal)
npx react-native run-ios

# Run on Android emulator (in a new terminal)
npx react-native run-android
```

### **Verify Installation**
✅ **App launches successfully**  
✅ **Bottom tab navigation works**  
✅ **Dashboard screen displays**  
✅ **Navigation between tabs functions**  
✅ **No console errors or warnings**  

---

## 🚀 **Next Development Steps**

### **Phase 1.1: Enhanced UI Setup** (Week 1)
1. **Install additional UI libraries**
2. **Create design system components**  
3. **Set up theme configuration**
4. **Implement responsive layouts**

### **Phase 1.2: API Integration** (Week 1)
1. **Create API service layer**
2. **Implement authentication flow**
3. **Set up error handling**
4. **Add loading states**

### **Phase 1.3: Core Features** (Week 2)
1. **Dashboard functionality**
2. **Basic workout tracking**
3. **User profile management**
4. **Navigation enhancements**

---

## 🛠 **Troubleshooting Common Issues**

### **iOS Build Issues**
```bash
# Clean iOS build
cd ios && xcodebuild clean && cd ..
rm -rf ios/build
cd ios && pod install && cd ..
```

### **Android Build Issues**
```bash
# Clean Android build
cd android && ./gradlew clean && cd ..
npx react-native run-android --reset-cache
```

### **Metro Bundler Issues**
```bash
# Reset Metro cache
npx react-native start --reset-cache
```

### **Node Modules Issues**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

---

This setup gives you a solid foundation for your Khyrie mobile app! The project structure follows React Native best practices and is ready for the next phase of development.

**Ready to proceed with Phase 2 - Component Migration?** 🚀