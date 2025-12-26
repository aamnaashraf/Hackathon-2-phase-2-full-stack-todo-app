<!--
Sync Impact Report:
Version change: N/A → 1.0.0
Modified principles: None (new constitution)
Added sections: All sections added
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Todo Web Application Constitution

## Core Principles

### Tech Stack Adherence
<!-- I. Tech Stack -->
All development must strictly use the predetermined technology stack: Frontend - Next.js 14+ with App Router and Tailwind CSS for beautiful, responsive, modern UI (clean, minimal, dark mode support, professional look with gradients, cards, smooth animations). Backend - FastAPI (Python) with SQLModel for models and migrations. Database - Neon DB (PostgreSQL, serverless) for persistent storage. Authentication - Better Auth library (secure JWT-based, email/password register/login). Deployment - Entire app in one repo, deployable on Vercel (Next.js for frontend + serverless API routes for FastAPI if needed, or separate Vercel functions). Deviations from this stack require explicit justification and approval.

### Code Quality and Type Safety
<!-- II. Code Quality -->
All code must be type-safe using Pydantic/SQLModel, follow clean architecture principles, include comprehensive error handling, loading states, and responsive design (mobile-first). Code reviews must verify adherence to these standards before merge. All API contracts must be well-defined with proper validation and documentation.

### Extension of Phase 1 Functionality
<!-- III. Phase Continuation -->
The application must build upon the in-memory console Todo app logic from Phase 1, extending it to persistent database storage with per-user todos. All CRUD operations from Phase 1 must be preserved and enhanced with database persistence and user authentication. The core business logic must remain consistent while adding new persistence and security layers.

### Security and Authentication
<!-- IV. Security-First -->
All todo endpoints must be protected with JWT authentication via Better Auth. Protected routes must enforce proper authorization checks. Security best practices must be followed including secure password handling, proper session management, and protection against common vulnerabilities (XSS, CSRF, SQL injection). Authentication must be implemented before any feature that accesses user data.

### UI Excellence and User Experience
<!-- V. UX Focus -->
The application must provide an attractive dashboard with todo list (cards/grid), add/edit modal, complete toggle, delete functionality, optional due dates, and beautiful empty state. UI must be responsive, intuitive, and visually appealing with smooth animations and transitions. Dark mode support is mandatory. All user interactions must provide appropriate feedback.

### Hackathon Optimization
<!-- VI. Practical Delivery -->
No over-engineering: Keep the application simple but polished for hackathon demo. Features should be complete and functional rather than numerous and half-baked. Focus on delivering a cohesive, well-presented demo that showcases the core functionality elegantly rather than attempting to implement numerous complex features.

## Additional Technical Constraints

- Database migrations must be handled through SQLModel's migration system
- API endpoints must follow RESTful conventions with appropriate HTTP status codes
- Client-side state management must be properly integrated with backend API
- Form validation must occur both client-side and server-side
- Loading states must be implemented for all asynchronous operations
- Proper error messaging must be displayed to users when operations fail
- The application must be optimized for performance with efficient database queries

## Development Workflow

- All code changes must pass through peer review before merging
- New features must include basic manual test instructions in README
- Git commit messages must follow conventional format
- Branch names should reflect the feature or bug being addressed
- Pull requests must include a clear description of changes and testing performed
- Before merging, all functionality must be manually tested across different screen sizes
- Documentation updates must accompany new features or significant changes

## Governance

This constitution serves as the authoritative guide for all development decisions in the Todo Web Application project. All specifications, plans, tasks, and implementations must strictly comply with these principles. Any proposed changes to these core principles require explicit documentation, team approval, and a clear migration plan. All pull requests and code reviews must verify constitutional compliance before approval. Deviations from these principles must be justified with clear reasoning and documented appropriately.

**Version**: 1.0.0 | **Ratified**: 2025-12-21 | **Last Amended**: 2025-12-21
