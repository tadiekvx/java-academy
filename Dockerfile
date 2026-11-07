# Java Engineering Academy for a single-learner host (Render). Needs a full JDK at run time:
# the platform compiles and runs learner code with javac.
FROM node:22-slim AS frontend
WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM maven:3.9-eclipse-temurin-25 AS backend
WORKDIR /build/backend
COPY backend/pom.xml ./
RUN mvn -q -B dependency:go-offline
COPY backend/src ./src
RUN mvn -q -B -DskipTests package && cp target/*.jar /build/app.jar

FROM eclipse-temurin:25-jdk
# Working directory is backend/ so the relative paths in application.yaml (../content, ../frontend/dist) resolve.
WORKDIR /app/backend
COPY --from=backend /build/app.jar /app/app.jar
COPY --from=frontend /build/frontend/dist /app/frontend/dist
COPY content/java /app/content/java
COPY docs/curriculum/sources.md /app/docs/curriculum/sources.md
RUN useradd --system --uid 10001 academy && chown -R academy /app
USER academy
EXPOSE 10000
# Render sets PORT; the container is sized for a small instance.
ENTRYPOINT ["sh", "-c", "exec java -XX:MaxRAMPercentage=60 -jar /app/app.jar --server.port=${PORT:-10000}"]
