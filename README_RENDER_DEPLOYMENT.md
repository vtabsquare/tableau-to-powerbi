# Deploying to Render

This repository is pre-configured with a `render.yaml` Blueprint to automatically deploy both the frontend and backend services to Render.

## Deployment Steps

1. Push this entire repository to your GitHub account (which you have already done!).
2. Log in to [Render](https://render.com/).
3. Click on **New** -> **Blueprint**.
4. Connect your GitHub account and select this repository (`tableau-to-powerbi`).
5. Render will automatically detect the `render.yaml` file and prompt you to create the two services:
   - **t2pbi-backend**: The Python FastAPI service with a persistent 10GB disk for workspaces.
   - **t2pbi-frontend**: The Node.js React application served via `serve`.
6. Click **Apply** to deploy.

Render will automatically link the frontend to the backend using the environment variables defined in the Blueprint. Once both services show as "Live", you can open the frontend's Render URL in your browser!
