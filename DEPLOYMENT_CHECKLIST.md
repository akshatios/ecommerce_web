# 🚀 Quick Deployment Checklist

Follow these steps in order to deploy your e-commerce application.

## ✅ Pre-Deployment Checklist

- [ ] All code is working locally
- [ ] Backend runs without errors
- [ ] Frontend connects to backend
- [ ] MongoDB is accessible
- [ ] Git is initialized
- [ ] GitHub account created

---

## 📋 Deployment Steps

### 1️⃣ MongoDB Atlas (5 minutes)
- [ ] Sign up at mongodb.com/cloud/atlas
- [ ] Create free M0 cluster
- [ ] Create database user (save password!)
- [ ] Allow access from anywhere (0.0.0.0/0)
- [ ] Copy connection string
- [ ] Test connection locally

**Connection String Format:**
```
mongodb+srv://username:password@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

---

### 2️⃣ GitHub Repository (3 minutes)
```bash
# In project root (d:\New folder (3))
git init
git add .
git commit -m "Initial commit"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-api.git
git branch -M main
git push -u origin main
```

- [ ] Repository created on GitHub
- [ ] Code pushed successfully
- [ ] Repository is public or private (your choice)

---

### 3️⃣ Backend - Render.com (10 minutes)
- [ ] Sign up at render.com
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Configure settings:
  - Name: `ecommerce-api`
  - Runtime: `Python 3`
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Instance: `Free`

- [ ] Add environment variables:
  - `MONGO_URI` = Your MongoDB connection string
  - `SECRET_KEY` = Generate with: `openssl rand -hex 32`
  - `ALGORITHM` = `HS256`
  - `ACCESS_TOKEN_EXPIRE_MINUTES` = `30`

- [ ] Click "Create Web Service"
- [ ] Wait for deployment (5-10 min)
- [ ] Test: Visit `https://your-app.onrender.com/docs`

**Your Backend URL:** `_________________________________`

---

### 4️⃣ Update CORS (2 minutes)
After getting your Vercel URL (next step), update `app/main.py`:

```python
origins = [
    "https://your-project.vercel.app",  # Add your Vercel URL
    "http://localhost:5173"
]
```

Then commit and push:
```bash
git add .
git commit -m "Update CORS for production"
git push
```

Render will auto-deploy the update.

---

### 5️⃣ Frontend - Vercel (5 minutes)
- [ ] Update `frontend/.env.production`:
  ```
  VITE_API_URL=https://your-backend.onrender.com
  ```

- [ ] Commit changes:
  ```bash
  git add .
  git commit -m "Add production API URL"
  git push
  ```

- [ ] Sign up at vercel.com
- [ ] Click "Add New Project"
- [ ] Import GitHub repository
- [ ] Configure:
  - Framework: `Vite`
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `dist`

- [ ] Add environment variable:
  - Key: `VITE_API_URL`
  - Value: `https://your-backend.onrender.com`

- [ ] Click "Deploy"
- [ ] Wait 2-3 minutes
- [ ] Test: Visit your Vercel URL

**Your Frontend URL:** `_________________________________`

---

## 🧪 Testing Checklist

### Backend Tests
- [ ] Visit `https://your-backend.onrender.com/docs`
- [ ] Swagger UI loads correctly
- [ ] Test `/register` endpoint
- [ ] Test `/login` endpoint
- [ ] Check MongoDB Atlas - data appears

### Frontend Tests
- [ ] Visit your Vercel URL
- [ ] Page loads without errors
- [ ] Open browser console (F12) - no errors
- [ ] Test user registration
- [ ] Test user login
- [ ] Test product listing (if implemented)

---

## 🎉 Post-Deployment

### Update CORS (Important!)
Go back to step 4️⃣ and update CORS with your Vercel URL.

### Optional Improvements
- [ ] Add custom domain on Vercel (free)
- [ ] Setup cron job to keep Render awake (cron-job.org)
- [ ] Add Google Analytics
- [ ] Setup error monitoring (Sentry)

---

## 📝 Save Your URLs

| Service | URL | Notes |
|---------|-----|-------|
| **Frontend** | `https://____________.vercel.app` | Main website |
| **Backend** | `https://____________.onrender.com` | API server |
| **API Docs** | `https://____________.onrender.com/docs` | Swagger UI |
| **MongoDB** | Atlas Dashboard | Database |

---

## 🐛 Common Issues

### Backend won't start
- Check Render logs for errors
- Verify all environment variables are set
- Check MongoDB connection string is correct

### Frontend can't connect to backend
- Check CORS settings in `app/main.py`
- Verify `VITE_API_URL` in Vercel environment variables
- Check browser console for errors

### MongoDB connection failed
- Verify connection string (check password)
- Ensure IP whitelist includes 0.0.0.0/0
- Check database user has correct permissions

---

## 🎊 Success!

Once all checkboxes are ticked, your application is live! 🚀

Share your URLs:
- **Website**: Your Vercel URL
- **API**: Your Render URL

---

## 📞 Need Help?

1. Check `DEPLOYMENT.md` for detailed instructions
2. Check Render/Vercel logs for errors
3. Test locally first to isolate issues

Good luck! 🍀
