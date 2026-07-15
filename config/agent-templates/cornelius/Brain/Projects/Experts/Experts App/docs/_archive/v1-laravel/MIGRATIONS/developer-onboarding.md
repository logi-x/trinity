---
title: "Developer Onboarding Guide"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/migrations"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# Developer Onboarding Guide

## 📋 Overview

Welcome to the Experts platform! This guide will help you set up your development environment and get started with the unified Next.js application and pnpm workspace setup.

## 🎯 What You Need to Know

### Recent Architecture Changes

The Experts platform recently underwent major improvements:

1. **Unified Application**: 4 separate Next.js apps consolidated into one
2. **Package Manager**: Migrated from Yarn to pnpm for better performance
3. **Docker Optimization**: Streamlined Docker builds and deployment
4. **Improved Performance**: 47% faster installs, 62% faster builds

### Key Technologies

- **Frontend**: Next.js 15+ (App Router), React 19, TypeScript
- **Styling**: TailwindCSS v4, HeroUI/shadcn components
- **Backend API**: Laravel 11+ PHP API
- **Package Manager**: pnpm 10+
- **Build System**: Turborepo for monorepo management
- **Authentication**: Laravel Passport OAuth2

## 🚀 Quick Start (15 minutes)

### Prerequisites

Before you begin, ensure you have:

- **Node.js**: v20.0.0 or higher
- **pnpm**: v10.0.0 or higher
- **Git**: Latest version
- **Docker**: For containerized development (optional)
- **Code Editor**: VS Code recommended

### Step 1: Install Node.js

```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20

# Verify installation
node --version  # Should show v20.x.x
```

### Step 2: Install pnpm

```bash
# Enable corepack (recommended)
corepack enable
corepack prepare pnpm@10.25.0 --activate

# Or install globally
npm install -g pnpm@10.25.0

# Verify installation
pnpm --version  # Should show 10.20.0
```

### Step 3: Clone Repository

```bash
# Clone the repository
git clone https://github.com/your-org/experts.git
cd experts

# Checkout develop branch
git checkout develop
```

### Step 4: Install Dependencies

```bash
# Install all workspace dependencies
pnpm install

# This will install dependencies for:
# - Root workspace
# - All apps (experts-app, experts-api, experts-server)
# - All packages (@experts/*)
```

### Step 5: Setup Environment Variables

```bash
# Copy example environment files
cp apps/experts-app/.env.example apps/experts-app/.env.local
cp apps/experts-api/.env.example apps/experts-api/.env

# Edit environment variables
# Update API URLs, database credentials, etc.
```

### Step 6: Start Development Server

```bash
# Start the unified Next.js app
pnpm run dev

# Or start specific app
pnpm --filter @logi-x/experts-app run dev

# Access at http://localhost:3000
```

### Step 7: Verify Setup

```bash
# Run type check
pnpm run type-check

# Run linting
pnpm run lint

# Run tests
pnpm run test

# If all pass, you're ready to develop!
```

## 📚 Detailed Setup Guide

### Development Environment Setup

#### VS Code Extensions (Recommended)

Install these extensions for best experience:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "unifiedjs.vscode-mdx",
    "prisma.prisma"
  ]
}
```

#### VS Code Settings

Add to `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

### Project Structure Understanding

```
experts/
├── apps/
│   ├── experts-app/          # Unified Next.js application
│   │   ├── src/app/
│   │   │   ├── (admin)/      # Admin routes
│   │   │   ├── (portal)/     # Portal routes
│   │   │   ├── auth/         # Auth routes
│   │   │   └── api/          # API routes
│   │   ├── public/
│   │   ├── package.json
│   │   └── next.config.js
│   ├── experts-api/          # Laravel API
│   └── experts-server/       # Node.js server
├── packages/
│   ├── ai/                   # AI utilities
│   ├── core/
│   │   ├── config/          # Shared configs
│   │   ├── theme/           # Theme system
│   │   └── types/           # TypeScript types
│   ├── ui/                   # UI components
│   ├── utilities/            # Utility functions
│   ├── hooks/                # React hooks
│   └── functions/            # Shared functions
├── pnpm-workspace.yaml       # Workspace config
├── package.json              # Root package.json
└── turbo.json                # Turborepo config
```

### Understanding Route Organization

The unified experts-app uses Next.js App Router with route groups:

```
src/app/
├── (admin)/                  # Admin section (URL: /*)
│   ├── dashboard/           # /dashboard
│   ├── users/               # /users
│   └── analytics/           # /analytics
├── (portal)/                 # Portal section (URL: /*)
│   ├── courses/             # /courses
│   ├── students/            # /students
│   └── analytics/           # /analytics
├── auth/                     # Auth section (URL: /auth/*)
│   ├── login/               # /auth/login
│   ├── register/            # /auth/register
│   └── callback/            # /auth/callback
└── api/                      # API routes (URL: /api/*)
    ├── auth/                # /api/auth
    └── courses/             # /api/courses
```

**Key Points:**

- Route groups `(admin)` and `(portal)` are **invisible** in URLs
- They provide logical organization without affecting routing
- Routes can share the same path (e.g., both have `/analytics`)
- Authentication and authorization happen at layout level

## 🔧 Common Development Tasks

### Working with Workspace Packages

#### Adding a Dependency

```bash
# Add to specific workspace
pnpm add lodash --filter=@logi-x/experts-app

# Add to multiple workspaces
pnpm add date-fns --filter=@experts/* --recursive

# Add workspace dependency
pnpm add @experts/ui --filter=@logi-x/experts-app
```

#### Removing a Dependency

```bash
# Remove from specific workspace
pnpm remove lodash --filter=@logi-x/experts-app

# Remove from all workspaces
pnpm remove unused-package --recursive
```

#### Updating Dependencies

```bash
# Update specific package
pnpm update react --filter=@logi-x/experts-app

# Update all dependencies
pnpm update --recursive

# Check for outdated packages
pnpm outdated --recursive
```

### Running Scripts

#### Development

```bash
# Start all apps in development mode
pnpm run dev

# Start specific app
pnpm --filter @logi-x/experts-app run dev

# Start with turbo (parallel execution)
pnpm turbo run dev
```

#### Building

```bash
# Build all apps
pnpm run build

# Build specific app
pnpm --filter @logi-x/experts-app run build

# Build with turbo
pnpm turbo run build
```

#### Testing

```bash
# Run all tests
pnpm run test

# Run tests for specific package
pnpm --filter @experts/ui run test

# Run tests in watch mode
pnpm run test --watch

# Run tests with coverage
pnpm run test --coverage
```

#### Code Quality

```bash
# Run linting
pnpm run lint

# Fix linting errors
pnpm run lint:fix

# Run type checking
pnpm run type-check

# Format code
pnpm run format
```

### Working with Git

#### Branch Naming Convention

```bash
# Features
git checkout -b feature/add-user-profile

# Bug fixes
git checkout -b fix/login-redirect-issue

# Chores
git checkout -b chore/update-dependencies

# Refactoring
git checkout -b refactor/authentication-flow
```

#### Commit Message Convention

```bash
# Format: <type>(<scope>): <description>

# Examples:
git commit -m "feat(auth): add OAuth2 login support"
git commit -m "fix(ui): resolve button alignment issue"
git commit -m "chore(deps): update dependencies"
git commit -m "docs(readme): update installation guide"
git commit -m "refactor(api): simplify user service logic"
```

### Docker Development

#### Running with Docker

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up experts-app

# View logs
docker-compose logs -f experts-app

# Restart service
docker-compose restart experts-app

# Stop all services
docker-compose down
```

#### Building Docker Images

```bash
# Build experts-app image
docker build -f apps/experts-app/Dockerfile.minimal -t experts-app .

# Build with cache
docker build --cache-from experts-app:latest -t experts-app:new .

# Run container
docker run -p 3000:3000 experts-app
```

## 🐛 Common Issues and Solutions

### Issue: pnpm command not found

```bash
# Solution: Install pnpm
corepack enable
corepack prepare pnpm@10.25.0 --activate
```

### Issue: Cannot find module '@experts/...'

```bash
# Solution: Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Issue: Port 3000 already in use

```bash
# Solution 1: Kill process using port
lsof -ti:3000 | xargs kill -9

# Solution 2: Use different port
PORT=3001 pnpm run dev
```

### Issue: TypeScript errors after pulling changes

```bash
# Solution: Reinstall and restart TypeScript server
pnpm install
# In VS Code: Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"
```

### Issue: Hot reload not working

```bash
# Solution: Clear cache and restart
rm -rf .next node_modules/.cache
pnpm run dev
```

## 📖 Learning Resources

### Internal Documentation

- [Next.js Consolidation](./nextjs-consolidation.md) - Architecture details
- [Yarn to pnpm Migration](./yarn-to-pnpm-migration.md) - Package manager guide
- [Docker Optimization](./docker-optimization.md) - Docker setup
- [Troubleshooting Guide](./troubleshooting-guide.md) - Common issues
- [Best Practices](./best-practices.md) - Development guidelines

### External Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [pnpm Documentation](https://pnpm.io/)
- [Turborepo Documentation](https://turbo.build/repo/docs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [React Documentation](https://react.dev/)

## 🤝 Getting Help

### Communication Channels

- **Slack**: #experts-development
- **GitHub**: Create issue for bugs
- **Email**: <dev-team@experts.com>
- **Wiki**: <https://wiki.experts.com>

### Code Review Process

1. **Create Feature Branch**: From `develop` branch
2. **Make Changes**: Follow coding standards
3. **Test Locally**: Run tests and type checking
4. **Commit Changes**: Use conventional commits
5. **Push Branch**: Push to origin
6. **Create Pull Request**: Against `develop` branch
7. **Address Feedback**: Make requested changes
8. **Merge**: After approval and passing CI/CD

### Before Asking for Help

1. **Check Documentation**: Review migration docs
2. **Search Issues**: Look for similar problems
3. **Try Troubleshooting**: Follow troubleshooting guide
4. **Gather Information**:
   - Error messages
   - Steps to reproduce
   - Your environment (OS, Node version, pnpm version)
   - Recent changes made

## ✅ Onboarding Checklist

### Day 1

- [ ] Install Node.js v20+
- [ ] Install pnpm v10+
- [ ] Clone repository
- [ ] Install dependencies
- [ ] Setup environment variables
- [ ] Start development server
- [ ] Verify setup with tests

### Week 1

- [ ] Read migration documentation
- [ ] Understand project structure
- [ ] Setup VS Code with recommended extensions
- [ ] Join Slack channels
- [ ] Meet the team
- [ ] Complete first small task

### Week 2

- [ ] Understand route organization
- [ ] Learn workspace package system
- [ ] Review coding standards
- [ ] Make first pull request
- [ ] Participate in code review
- [ ] Learn Docker setup

### Month 1

- [ ] Contribute to major feature
- [ ] Help with code reviews
- [ ] Share knowledge with team
- [ ] Suggest improvements
- [ ] Mentor new team member

## 🎯 Next Steps

Now that you're set up:

1. **Explore the Codebase**: Familiarize yourself with the unified structure
2. **Read Architecture Docs**: Understand the consolidation decisions
3. **Start with Small Tasks**: Begin with bug fixes or small features
4. **Ask Questions**: Don't hesitate to ask the team
5. **Contribute**: Share your ideas and improvements

## 🔗 Related Documentation

- [Next.js Consolidation](./nextjs-consolidation.md)
- [Yarn to pnpm Migration](./yarn-to-pnpm-migration.md)
- [Docker Optimization](./docker-optimization.md)
- [Performance Comparison](./performance-comparison.md)
- [Troubleshooting Guide](./troubleshooting-guide.md)
- [Best Practices](./best-practices.md)

---

**Welcome to the Team!** 🎉

**Last Updated**: October 29, 2025  
**Status**: ✅ Active Onboarding Guide  
**Questions**: Contact <dev-team@experts.com>
