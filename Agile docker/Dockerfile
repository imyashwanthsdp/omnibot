# Stage 1: Build & Dependencies
FROM node:22-alpine AS builder

WORKDIR /app

# Copy dependency manifests
COPY package.json ./

# Install production dependencies
RUN npm install --only=production

# Copy application source code
COPY . .

# Stage 2: Runtime Container Image
FROM node:22-alpine

WORKDIR /app

# Copy built app from builder stage
COPY --from=builder /app /app

# Expose server port
EXPOSE 3000

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Health check instructions
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/api/health || exit 1

# Start chatbot server
CMD ["npm", "start"]
