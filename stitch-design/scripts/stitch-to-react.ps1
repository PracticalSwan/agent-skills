<#
.SYNOPSIS
    Sets up a React project for Stitch component conversion.

.DESCRIPTION
    Creates a Vite + React + TypeScript project, installs Tailwind CSS and
    shadcn/ui, scaffolds the recommended directory structure, and generates
    starter files (mockData.ts, App.tsx).

.PARAMETER ProjectName
    Name of the project directory to create. Defaults to "stitch-app".

.EXAMPLE
    .\stitch-to-react.ps1 -ProjectName "FoodieHub"
#>
param(
    [Parameter(Position = 0)]
    [string]$ProjectName = "stitch-app"
)

$ErrorActionPreference = "Stop"

Write-Host "`n=== Stitch-to-React Project Setup ===" -ForegroundColor Cyan
Write-Host "Project: $ProjectName`n"

# Step 1: Create Vite + React + TypeScript project
Write-Host "[1/6] Creating Vite project..." -ForegroundColor Yellow
npm create vite@latest $ProjectName -- --template react-ts
Set-Location $ProjectName

# Step 2: Install dependencies
Write-Host "[2/6] Installing base dependencies..." -ForegroundColor Yellow
npm install

# Step 3: Install Tailwind CSS
Write-Host "[3/6] Installing Tailwind CSS..." -ForegroundColor Yellow
npm install -D tailwindcss @tailwindcss/vite

# Create Tailwind config
$tailwindContent = @"
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
"@
Set-Content -Path "vite.config.ts" -Value $tailwindContent

# Update CSS entry point
$cssContent = @"
@import "tailwindcss";

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"@
Set-Content -Path "src/index.css" -Value $cssContent

# Step 4: Install shadcn/ui dependencies
Write-Host "[4/6] Installing shadcn/ui dependencies..." -ForegroundColor Yellow
npm install tailwind-merge clsx class-variance-authority lucide-react
npm install -D @types/node

# Create lib/utils.ts for cn() helper
New-Item -ItemType Directory -Path "src/lib" -Force | Out-Null
$utilsContent = @"
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"@
Set-Content -Path "src/lib/utils.ts" -Value $utilsContent

# Create tsconfig path aliases
$tsconfigContent = @"
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
"@
Set-Content -Path "tsconfig.json" -Value $tsconfigContent

# Step 5: Create directory structure
Write-Host "[5/6] Creating project structure..." -ForegroundColor Yellow
$directories = @(
    "src/components/ui",
    "src/components/layout",
    "src/components/sections",
    "src/hooks",
    "src/data",
    "src/types",
    "src/styles",
    "public/images"
)
foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "  Created $dir" -ForegroundColor DarkGray
}

# Step 6: Generate starter files
Write-Host "[6/6] Generating starter files..." -ForegroundColor Yellow

# mockData.ts
$mockDataContent = @"
// Mock data extracted from Stitch design screens
// Replace with real data or API calls in production

export interface NavItem {
  label: string
  href: string
  icon?: string
}

export interface CardItem {
  id: string
  title: string
  description: string
  imageUrl: string
  tags: string[]
}

export const navigation: NavItem[] = [
  { label: "Home", href: "/", icon: "home" },
  { label: "Explore", href: "/explore", icon: "search" },
  { label: "Favorites", href: "/favorites", icon: "heart" },
  { label: "Profile", href: "/profile", icon: "user" },
]

export const featuredItems: CardItem[] = [
  {
    id: "1",
    title: "Sample Item",
    description: "A placeholder item from Stitch design.",
    imageUrl: "/images/placeholder.jpg",
    tags: ["Featured", "New"],
  },
]
"@
Set-Content -Path "src/data/mockData.ts" -Value $mockDataContent

# App.tsx scaffold
$appContent = @"
import "./index.css"

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <header className="border-b">
        <nav className="container mx-auto flex items-center justify-between px-4 py-3">
          <h1 className="text-xl font-bold">$ProjectName</h1>
          <div className="flex gap-4">
            <a href="/" className="text-sm text-muted-foreground hover:text-foreground">Home</a>
            <a href="/explore" className="text-sm text-muted-foreground hover:text-foreground">Explore</a>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <section className="text-center space-y-4">
          <h2 className="text-3xl font-bold">Welcome to $ProjectName</h2>
          <p className="text-muted-foreground max-w-md mx-auto">
            Converted from Stitch design. Replace this content with your
            actual components.
          </p>
        </section>

        {/* Card Grid - replace with shadcn Card components */}
        <section className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded-lg border bg-card p-6 shadow-sm">
              <div className="h-40 rounded-md bg-muted mb-4" />
              <h3 className="font-semibold">Card {i}</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Placeholder card from Stitch design.
              </p>
            </div>
          ))}
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t mt-16">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
          Built with Vite + React + Tailwind + shadcn/ui
        </div>
      </footer>
    </div>
  )
}

export default App
"@
Set-Content -Path "src/App.tsx" -Value $appContent

# DESIGN.md template
$designContent = @"
# $ProjectName — Design System

> Generated from Stitch project. Update tokens below to match your design.

## Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Primary | #1E293B | Buttons, links, headings |
| Secondary | #F1F5F9 | Backgrounds, cards |
| Accent | #3B82F6 | Highlights, active states |
| Destructive | #EF4444 | Errors, delete actions |
| Muted | #94A3B8 | Secondary text, borders |
| Background | #FFFFFF | Page background |

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Heading 1 | Inter | 2.25rem | 700 |
| Heading 2 | Inter | 1.5rem | 600 |
| Body | Inter | 1rem | 400 |
| Caption | Inter | 0.875rem | 400 |

## Spacing Scale

4px — 8px — 12px — 16px — 24px — 32px — 48px — 64px

## Components

Document component styles here as you convert Stitch screens.
"@
Set-Content -Path "DESIGN.md" -Value $designContent

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. cd $ProjectName"
Write-Host "  2. npx shadcn-ui@latest init"
Write-Host "  3. npx shadcn-ui@latest add button card dialog input"
Write-Host "  4. npm run dev"
Write-Host ""
