# Full-Stack Secure Todo Web Application

A modern, full-stack todo application with user authentication, built using Next.js 14+, FastAPI, and Neon PostgreSQL.

## Features

- User registration and secure login
- Create, read, update, and delete todos
- User-specific todo management (todos are private to each user)
- Responsive design with dark mode support
- Beautiful UI with Tailwind CSS
- Due date functionality
- Real-time notifications
- Protected routes and JWT authentication

## Tech Stack

- **Frontend**: Next.js 14+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python
- **Database**: Neon PostgreSQL (serverless)
- **Authentication**: JWT-based authentication
- **Styling**: Tailwind CSS with custom components
- **Deployment**: Vercel (full-stack deployment)

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Git installed
- Access to Neon PostgreSQL account

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to app directory
cd ../app

# Install dependencies
npm install
```

### 4. Environment Configuration

Create a `.env` file in the root directory with the following content:

```env
# Backend Configuration
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_app?sslmode=require"
SECRET_KEY="your-super-secret-key-here-changeme-for-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

> **Note**: For development, you can use a simple string for `SECRET_KEY`, but make sure to use a strong, randomly generated key for production.

### 5. Run the Application

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

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user
- `POST /api/auth/logout` - Logout a user

### Todos
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo

## Deployment to Vercel

1. Push your code to a GitHub repository
2. Go to [Vercel](https://vercel.com) and connect your GitHub account
3. Import your repository
4. Set the following environment variables in Vercel dashboard:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: A strong secret key for JWT
   - `ALGORITHM`: "HS256"
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: "30"
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API

## Security Features

- JWT-based authentication for all protected routes
- Passwords are hashed using bcrypt
- SQL injection prevention through SQLModel
- Input validation using Pydantic
- CORS configured for secure cross-origin requests

## Architecture

The application follows a monorepo structure:

```
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/         # SQLModel database models
│   │   ├── services/       # Business logic
│   │   ├── api/            # API routes
│   │   └── database/       # Database configuration
│   └── requirements.txt
├── app/                    # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and hooks
│   │   └── styles/        # Global styles
│   ├── package.json
│   └── next.config.js
├── .env                   # Environment variables
└── vercel.json            # Vercel deployment configuration
```

## Development

To run tests (when implemented):
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd app
npm run test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue in the GitHub repository.