# 🚀 Your Deployment Configuration

## ✅ What's Already Done

- ✅ GitHub Repository: https://github.com/akshatios/ecommerce_web
- ✅ MongoDB Atlas: Connected and tested successfully
- ✅ Database Name: `Ecommerce`
- ✅ Local testing: Working perfectly

---

## 📋 Environment Variables for Render.com

When deploying to Render, add these **exact** environment variables:

### 1. MONGO_URI
```
mongodb+srv://akshatios:Akshatau1138%40%40%23%23@skillobalbackend.0oy0xhp.mongodb.net/Ecommerce?retryWrites=true&w=majority&appName=SkillobalBackend
```

### 2. SECRET_KEY
```
b86141557ebe20a6d7190576cc90dac8e37df52e065df35356c8d6362cafa153
```

### 3. ALGORITHM
```
HS256
```

### 4. ACCESS_TOKEN_EXPIRE_MINUTES
```
30
```

---

## 🔧 Render.com Deployment Steps

### Step 1: Go to Render.com
1. Visit: https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**

### Step 2: Connect Repository
1. Select: `akshatios/ecommerce_web`
2. Click **"Connect"**

### Step 3: Configure Service
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `ecommerce-api` (or any name you like) |
| **Region** | Singapore (closest to India) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### Step 4: Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add all 4 variables from above (copy-paste exactly as shown).

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Your API will be live! 🎉

### Step 6: Test Your API
Once deployed, visit:
```
https://your-app-name.onrender.com/docs
```

You should see the Swagger documentation!

---

## 🎨 Vercel Deployment (Frontend)

### Step 1: Update Frontend API URL

**IMPORTANT**: First get your Render backend URL, then:

1. Open `frontend/.env.production`
2. Update with your Render URL:
   ```
   VITE_API_URL=https://your-app-name.onrender.com
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "Update production API URL"
   git push
   ```

### Step 2: Deploy to Vercel
1. Visit: https://vercel.com
2. Sign up with GitHub
3. Click **"Add New Project"**
4. Select: `akshatios/ecommerce_web`

### Step 3: Configure
| Setting | Value |
|---------|-------|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

### Step 4: Add Environment Variable
- **Key**: `VITE_API_URL`
- **Value**: `https://your-render-url.onrender.com`

### Step 5: Deploy
Click **"Deploy"** and wait 2-3 minutes!

---

## 🧪 Testing Checklist

### After Backend Deployment
- [ ] Visit `https://your-app.onrender.com/docs`
- [ ] Test `/register` endpoint in Swagger UI
- [ ] Test `/login` endpoint
- [ ] Check MongoDB Atlas - data should appear in `Ecommerce` database

### After Frontend Deployment
- [ ] Visit your Vercel URL
- [ ] Open browser console (F12) - check for errors
- [ ] Test registration form
- [ ] Test login form
- [ ] Verify API calls are working

---

## 📝 Your Deployment URLs

Save these as you deploy:

| Service | URL | Status |
|---------|-----|--------|
| **GitHub** | https://github.com/akshatios/ecommerce_web | ✅ Done |
| **MongoDB** | Atlas Dashboard | ✅ Connected |
| **Backend (Render)** | `https://__________.onrender.com` | ⏳ Pending |
| **Frontend (Vercel)** | `https://__________.vercel.app` | ⏳ Pending |

---

## 🐛 Common Issues & Solutions

### Issue: "Internal Server Error" on Render
**Solution**: Check Render logs for errors. Most common:
- MongoDB connection string incorrect
- Missing environment variables
- Wrong database name

### Issue: Frontend can't connect to backend
**Solution**:
1. Check CORS settings (currently set to allow all origins `["*"]`)
2. Verify `VITE_API_URL` in Vercel environment variables
3. Check browser console for CORS errors

### Issue: Render service sleeps
**Solution**: Free tier sleeps after 15 minutes. First request takes 30-60 seconds to wake up.
- Use cron-job.org to ping every 14 minutes (keeps it awake)
- Or upgrade to paid plan ($7/month)

---

## 🎉 Success Indicators

You'll know everything is working when:
1. ✅ Render shows "Live" status
2. ✅ `/docs` endpoint loads Swagger UI
3. ✅ Vercel deployment shows "Ready"
4. ✅ Frontend can register/login users
5. ✅ MongoDB Atlas shows new users in `Ecommerce.users` collection

---

## 🚀 Next Steps After Deployment

1. **Update CORS** (optional, for security):
   - Edit `app/main.py`
   - Replace `origins = ["*"]` with your Vercel URL
   - Commit and push (Render auto-deploys)

2. **Custom Domain** (optional):
   - Add custom domain on Vercel (free)
   - Add custom domain on Render (free)

3. **Monitoring**:
   - Check Render logs regularly
   - Monitor MongoDB Atlas metrics
   - Use Vercel analytics

---

## 📞 Need Help?

If you get stuck:
1. Check Render logs: Dashboard → Logs tab
2. Check Vercel logs: Deployment → Function Logs
3. Check MongoDB Atlas: Database → Collections

---

**Ready to deploy? Start with Render.com!** 🚀

Good luck! 🍀
