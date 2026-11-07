import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In development the Vite server proxies API calls to the Spring Boot backend on :8080.
// `npm run build` writes to dist/, which the backend serves directly (see application.yaml).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { "/api": "http://localhost:8080" },
  },
});
