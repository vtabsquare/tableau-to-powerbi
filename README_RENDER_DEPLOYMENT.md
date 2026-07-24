# Deploying to Render

You can deploy this repository to Render using either the **Automated Blueprint** (recommended) or manually via **Web Services**.

## Option 1: Automated Blueprint (Recommended)

1. Log in to [Render](https://render.com/).
2. Click on **New** -> **Blueprint**.
3. Connect your GitHub account and select this repository (`tableau-to-powerbi`).
4. Render will automatically detect the `render.yaml` file and prompt you to create both the backend and frontend.
5. Click **Apply** to deploy.

## Option 2: Manual Web Services

If you prefer not to use the Blueprint, you can create the services manually from the Render dashboard.

### Step 1: Create the Backend Service
1. In Render, click **New** -> **Web Service**.
2. Select your `tableau-to-powerbi` repository.
3. Configure the service:
   - **Name**: `t2pbi-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Click **Advanced** and add an Environment Variable:
   - Key: `PYTHON_VERSION`, Value: `3.11.0`
5. (Optional) To persist files, click **Disks**, add a disk named `workspace`, mount path `/data`, and add an Env Var `T2PBI_WORKSPACE = /data/workspace`.
6. Click **Create Web Service**. Once it deploys, copy its public URL (e.g., `https://t2pbi-backend.onrender.com`).

### Step 2: Create the Frontend Service
1. Click **New** -> **Web Service** (or Static Site, which is free).
2. Select your `tableau-to-powerbi` repository.
3. Configure the service:
   - **Name**: `t2pbi-frontend`
   - **Root Directory**: `frontend`
   - **Environment**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s dist -l $PORT` *(Note: if you chose Static Site, the start command isn't needed, just set Publish Directory to `dist`)*
4. Click **Advanced** and add these Environment Variables:
   - Key: `NODE_VERSION`, Value: `20`
   - Key: `VITE_API_BASE_URL`, Value: `[Paste your Backend URL here]`
5. Click **Create Web Service**.
