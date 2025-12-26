# Quickstart Guide: Full-Stack Secure Todo Web Application

**Feature**: 1-secure-todo-app
**Date**: 2025-12-21

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Git installed
- Access to Neon PostgreSQL account

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Initialize the project structure
mkdir -p backend app
```

### 2. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv httpx

# Create basic project structure
mkdir -p src/{models,services,api,database}
touch src/{main.py,__init__.py}
touch src/models/{__init__.py,user.py,todo.py}
touch src/services/{__init__.py,auth.py,todo_service.py}
touch src/api/{__init__.py,auth.py,todos.py}
touch src/database/{__init__.py,database.py}
```

### 3. Frontend Setup (Next.js)

```bash
# Navigate to app directory
cd ../app

# Initialize Next.js project
npm init -y
npm install next react react-dom typescript @types/react @types/node @types/react-dom tailwindcss postcss autoprefixer

# Initialize Tailwind CSS
npx tailwindcss init -p

# Create basic project structure
mkdir -p src/{app,components,lib,styles}
mkdir -p src/app/{login,register,dashboard}
touch next.config.js tsconfig.json
touch src/styles/globals.css
touch src/lib/{api.ts,auth.ts}
touch src/components/{ui,todos,auth}/{Button.tsx,LoginForm.tsx,RegisterForm.tsx,TodoList.tsx}
```

### 4. Environment Configuration

Create `.env` file in the root directory:

```env
# Backend Configuration
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_app?sslmode=require"
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

### 5. Database Setup

```bash
# In backend directory
cd backend

# Install alembic for migrations
pip install alembic

# Initialize alembic
alembic init alembic

# Configure alembic.ini to use your database URL
```

### 6. Run the Application

**Backend**:
```bash
# In backend directory
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.main:app --reload --port 8000
```

**Frontend**:
```bash
# In app directory
cd ../app
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Documentation: http://localhost:8000/docs

## Deployment to Vercel

1. Create a `vercel.json` file in the root directory:

```json
{
  "version": 2,
  "name": "todo-app",
  "builds": [
    {
      "src": "app/next.config.js",
      "use": "@vercel/next"
    },
    {
      "src": "backend/src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/src/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "app/$1"
    }
  ]
}
```

2. Deploy using Vercel CLI:
```bash
npm i -g vercel
vercel --prod
```