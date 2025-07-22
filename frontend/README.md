# Frontend - Next.js Application

This directory contains the Next.js frontend application with TypeScript and React.

## Features

- **Next.js 14** with App Router
- **React 18** components with TypeScript
- **Axios** for API communication
- **Modern responsive design** with custom CSS
- **Budget input form** with validation
- **Real-time API integration** with FastAPI backend

## Local Development

To run the frontend locally (without Docker):

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Main page
│   └── components/
│       └── BudgetForm.tsx   # Budget form component
├── public/                  # Static assets
├── Dockerfile              # Production Docker config
├── Dockerfile.dev          # Development Docker config
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
└── next.config.js          # Next.js configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Docker

The frontend is containerized and can be run as part of the full-stack application. See the root directory README for Docker commands.
