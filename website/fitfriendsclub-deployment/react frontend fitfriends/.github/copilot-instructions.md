# FitFriendsClubs Next.js Frontend - Copilot Instructions

## Project Overview
This is a Next.js/React frontend for the FitFriendsClubs fitness platform with TypeScript, Tailwind CSS, and API integration capabilities.

## Architecture
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React hooks (useState, useEffect) and Context API
- **API Integration**: Native fetch with existing Cloudflare Workers API
- **UI Components**: Custom components for clubs, trails, dashboard
- **Authentication**: Ready for future auth integration

## API Integration
- Base URL: https://fitfriendsclub-api.darnellroy2.workers.dev
- Endpoints: /, /test/clubs, /test/trails, /test/all
- Error handling and retry logic included
- Loading states for better UX

## Development Guidelines
- Use TypeScript interfaces for API responses
- Implement proper error boundaries
- Follow React best practices for hooks
- Use Tailwind for consistent styling
- Maintain responsive design principles
- Keep components modular and reusable

## Project Status: Setting up workspace infrastructure
- ✅ Created .github directory and copilot-instructions.md
- 🔄 Next: Get project setup information
- ⏳ Scaffold Next.js project structure
- ⏳ Install dependencies and extensions
- ⏳ Configure development environment