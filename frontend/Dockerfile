FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the React app for production
# REACT_APP_API_URL can be set at build time or use default
# This must succeed for the image to build
ARG REACT_APP_API_URL=http://localhost:5000
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# Verify build output exists
RUN test -d build || (echo "Build failed - build directory not found" && exit 1)

# Install serve globally
RUN npm install -g serve

# Expose port (Render will set PORT env var)
EXPOSE 3000

# Start serve - it binds to 0.0.0.0 by default
# Use PORT from environment, default to 3000
CMD ["sh", "-c", "serve -s build -l ${PORT:-3000}"]
