"""CORS configuration for the Mimi backend API."""

# Allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js development server
    "http://localhost:3001",  # Alternative Next.js port
    "http://127.0.0.1:3000",  # Alternative localhost
    "http://127.0.0.1:3001",  # Alternative localhost
]

# Allowed methods
ALLOWED_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "PATCH",
]

# Allowed headers
ALLOWED_HEADERS = [
    "Accept",
    "Accept-Language",
    "Content-Language",
    "Content-Type",
    "Authorization",
    "X-Requested-With",
    "Origin",
    "Access-Control-Request-Method",
    "Access-Control-Request-Headers",
] 