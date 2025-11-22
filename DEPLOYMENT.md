# 🚀 E-commerce API Deployment Guide

Complete guide to deploy your FastAPI + React e-commerce application for **FREE**.

## 📋 Architecture

- **Frontend**: React + Vite → Vercel
- **Backend**: FastAPI → Render.com
- **Database**: MongoDB → MongoDB Atlas

---

## 🗄️ Step 1: Setup MongoDB Atlas (Database)

### 1.1 Create Account
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Click **"Try Free"** and sign up
3. Choose **FREE tier** (M0 Sandbox)

### 1.2 Create Cluster
1. Select **AWS** or **Google Cloud**
2. Choose closest region (e.g., Mumbai for India)
3. Cluster Name: `ecommerce-cluster`
4. Click **"Create Cluster"**

### 1.3 Setup Database Access
1. Go to **Database Access** (left sidebar)
2. Click **"Add New Database User"**
3. Username: `ecommerce_user`
4. Password: Generate secure password (save it!)
5. Database User Privileges: **Read and write to any database**
6. Click **"Add User"**

### 1.4 Setup Network Access
1. Go to **Network Access** (left sidebar)
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
4. Click **"Confirm"**

### 1.5 Get Connection String
1. Go to **Database** → Click **"Connect"**
2. Choose **"Connect your application"**
3. Copy the connection string:
   ```
   mongodb+srv://ecommerce_user:<password>@ecommerce-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. **Save this connection string** - you'll need it!

---

## 🔧 Step 2: Deploy Backend to Render.com

### 2.1 Prepare Git Repository
```bash
# Initialize git (if not already done)
cd "d:\New folder (3)"
git init
git add .
git commit -m "Initial commit - E-commerce API"
```

### 2.2 Push to GitHub
1. Create new repository on [github.com](https://github.com/new)
2. Repository name: `ecommerce-api`
3. Make it **Public** or **Private**
4. Don't initialize with README (we already have files)
5. Copy the commands and run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/ecommerce-api.git
   git branch -M main
   git push -u origin main
   ```

### 2.3 Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `ecommerce-api` repository
5. Configure:
   - **Name**: `ecommerce-api`
   - **Region**: Singapore (closest to India)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

### 2.4 Add Environment Variables
In Render dashboard, go to **Environment** tab and add:

| Key | Value |
|-----|-------|
| `MONGO_URI` | Your MongoDB Atlas connection string |
| `SECRET_KEY` | Generate random string (e.g., `openssl rand -hex 32`) |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Your API will be live at: `https://ecommerce-api-xxxx.onrender.com`

### 2.5 Test Your API
Visit: `https://your-backend-url.onrender.com/docs`

You should see the FastAPI Swagger documentation! 🎉

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Update API URL
1. Open `frontend/.env.production`
2. Replace with your Render backend URL:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com
   ```

### 3.2 Update Frontend Code (if needed)
Make sure your frontend uses environment variables for API calls:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### 3.3 Commit Changes
```bash
git add .
git commit -m "Update production API URL"
git push
```

### 3.4 Deploy on Vercel
1. Go to [vercel.com](https://vercel.com) and sign up
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-url.onrender.com`
6. Click **"Deploy"**
7. Wait 2-3 minutes
8. Your site will be live at: `https://your-project.vercel.app`

---

## ✅ Step 4: Verify Deployment

### Backend Checks
- [ ] Visit `https://your-backend.onrender.com/docs`
- [ ] Test `/register` endpoint
- [ ] Test `/login` endpoint
- [ ] Check MongoDB Atlas - data should appear

### Frontend Checks
- [ ] Visit your Vercel URL
- [ ] Open browser console (F12)
- [ ] Check for API connection errors
- [ ] Test registration
- [ ] Test login

---

## 🔒 Security Notes

1. **Never commit `.env` file** - it's in `.gitignore`
2. **Use strong SECRET_KEY** - generate with `openssl rand -hex 32`
3. **Change MongoDB password** - use strong password
4. **Enable CORS properly** - update `app/main.py` with your Vercel URL:
   ```python
   origins = [
       "https://your-project.vercel.app",
       "http://localhost:5173"  # for local development
   ]
   ```

---

## 🐛 Troubleshooting

### Backend Issues
- **500 Error**: Check Render logs for errors
- **MongoDB Connection Failed**: Verify connection string and IP whitelist
- **Module Not Found**: Check `requirements.txt` has all dependencies

### Frontend Issues
- **API Not Connecting**: Check CORS settings in backend
- **404 Errors**: Verify API URL in `.env.production`
- **Build Failed**: Check Node version (use Node 18+)

---

## 🎉 Success!

Your e-commerce application is now live and accessible worldwide!

- **Frontend**: `https://your-project.vercel.app`
- **Backend API**: `https://your-backend.onrender.com`
- **API Docs**: `https://your-backend.onrender.com/docs`

---

## 📝 Important Notes

### Render Free Tier Limitations
- **Sleeps after 15 minutes** of inactivity
- **First request takes 30-60 seconds** to wake up
- **750 hours/month** free (enough for one service)

### Solutions for Sleep Issue
1. Use **cron-job.org** to ping your API every 14 minutes
2. Upgrade to Render paid plan ($7/month for always-on)
3. Use **Railway.app** ($5 free credit monthly)

### MongoDB Atlas Free Tier
- **512 MB storage** (plenty for starting)
- **Shared cluster** (good performance)
- **No credit card required**

---

## 🚀 Next Steps

1. **Custom Domain**: Add your own domain on Vercel (free)
2. **SSL Certificate**: Automatic on both Render and Vercel
3. **CI/CD**: Auto-deploy on git push (already configured!)
4. **Monitoring**: Use Render dashboard for logs
5. **Analytics**: Add Google Analytics to frontend

---

## 📞 Support

If you face any issues:
1. Check Render logs: Dashboard → Logs
2. Check Vercel logs: Deployment → Function Logs
3. Check MongoDB Atlas: Metrics → Performance

Happy Deploying! 🎊
