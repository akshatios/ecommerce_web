# 🗄️ MongoDB Atlas - Data Verification Guide

## ✅ How to Check Your Data in MongoDB Atlas

### Step 1: Login to MongoDB Atlas
1. Visit: https://cloud.mongodb.com
2. Login with your credentials
3. You'll see your cluster: `SkillobalBackend`

---

### Step 2: Browse Collections
1. Click on **"Browse Collections"** button
2. Select database: **`Ecommerce`**
3. You'll see collections:
   - `users` - All registered users
   - `products` - All products (when created)
   - `orders` - All orders (when created)

---

### Step 3: View Data

#### Users Collection
```
Database: Ecommerce
Collection: users

Sample Document:
{
  "_id": ObjectId("69219be4fb684e3dde384058"),
  "username": "admin",
  "email": "admin@test.com",
  "password": "$2b$12$...", // hashed password
  "is_active": true
}
```

#### Products Collection (after adding products)
```
Database: Ecommerce
Collection: products

Sample Document:
{
  "_id": ObjectId("..."),
  "name": "iPhone 15 Pro",
  "description": "Latest iPhone with A17 chip",
  "price": 999.99,
  "category": "Electronics",
  "image_url": "https://example.com/iphone.jpg",
  "stock": 50,
  "created_at": ISODate("2025-11-22T11:00:00Z")
}
```

#### Orders Collection (after creating orders)
```
Database: Ecommerce
Collection: orders

Sample Document:
{
  "_id": ObjectId("..."),
  "user_id": "69219be4fb684e3dde384058",
  "items": [
    {
      "product_id": "...",
      "quantity": 2
    }
  ],
  "total_amount": 1999.98,
  "status": "pending",
  "created_at": ISODate("2025-11-22T11:30:00Z")
}
```

---

## 🧪 Testing Data Flow

### Test 1: User Registration
**Action:**
```bash
POST /register
{
  "username": "john",
  "email": "john@example.com",
  "password": "john123"
}
```

**Verify in Atlas:**
1. Go to `Ecommerce` → `users` collection
2. You should see new user document
3. Password will be hashed (bcrypt)

---

### Test 2: Product Creation
**Action:**
```bash
POST /products (with auth token)
{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 1299.99,
  "category": "Electronics",
  "stock": 10
}
```

**Verify in Atlas:**
1. Go to `Ecommerce` → `products` collection
2. New product document will appear
3. `created_at` timestamp will be added automatically

---

### Test 3: Order Creation
**Action:**
```bash
POST /orders (with auth token)
{
  "items": [
    {
      "product_id": "...",
      "quantity": 2
    }
  ],
  "total_amount": 2599.98
}
```

**Verify in Atlas:**
1. Go to `Ecommerce` → `orders` collection
2. New order document will appear
3. Linked with `user_id`

---

## 🔍 Real-time Monitoring

### Atlas Features:
1. **Real-time Updates**: Refresh collection to see new data
2. **Search**: Use filters to find specific documents
3. **Edit**: Can manually edit documents (for testing)
4. **Delete**: Can delete test data

### Example Filters:
```javascript
// Find user by email
{ "email": "admin@test.com" }

// Find products by category
{ "category": "Electronics" }

// Find orders by user
{ "user_id": "69219be4fb684e3dde384058" }

// Find products with low stock
{ "stock": { "$lt": 10 } }
```

---

## 📊 Data Consistency Across Environments

### Important: Same Database for All!

```
Local Development (localhost:8000)
    ↓
    Uses MongoDB Atlas
    ↑
Production (Render)
```

**Both use the SAME database**: `Ecommerce` on MongoDB Atlas

This means:
- ✅ Data added locally will show on production
- ✅ Data added on production will show locally
- ✅ All environments share same data

---

## ⚠️ Best Practice: Separate Databases

For production apps, you should have:

### Development Database
```
MONGO_URI=mongodb+srv://...@cluster.mongodb.net/Ecommerce_Dev
```

### Production Database
```
MONGO_URI=mongodb+srv://...@cluster.mongodb.net/Ecommerce_Prod
```

**Current Setup**: Both use `Ecommerce` database (fine for learning/testing)

---

## 🛠️ Useful MongoDB Atlas Features

### 1. **Metrics**
- Monitor database performance
- See read/write operations
- Track storage usage

### 2. **Charts**
- Visualize your data
- Create dashboards
- Track trends

### 3. **Triggers**
- Auto-execute functions on data changes
- Send notifications
- Sync with other services

### 4. **Backup**
- Automatic daily backups (paid tier)
- Point-in-time recovery
- Download backups

---

## 🧪 Quick Verification Checklist

After deploying, verify:

- [ ] Visit MongoDB Atlas dashboard
- [ ] Check `Ecommerce` database exists
- [ ] Check `users` collection has data
- [ ] Register new user via API
- [ ] Refresh Atlas - new user appears
- [ ] Create product via API (with auth)
- [ ] Refresh Atlas - new product appears
- [ ] Create order via API
- [ ] Refresh Atlas - new order appears

---

## 📱 MongoDB Compass (Optional)

For better visualization, download **MongoDB Compass**:

1. Download: https://www.mongodb.com/try/download/compass
2. Connect using your connection string
3. Visual interface to browse data
4. Better than web interface for development

---

## 🎯 Summary

| Action | Where to Check | What to See |
|--------|---------------|-------------|
| **User registers** | Atlas → `users` | New user document |
| **Product created** | Atlas → `products` | New product document |
| **Order placed** | Atlas → `orders` | New order document |
| **Data updated** | Atlas → Refresh | Updated fields |
| **Data deleted** | Atlas → Refresh | Document removed |

---

## 💡 Pro Tips

1. **Keep Atlas dashboard open** while testing
2. **Use filters** to find specific data quickly
3. **Export data** as JSON for backup
4. **Monitor metrics** to track usage
5. **Set up alerts** for storage limits

---

**Your current user in database:**
```json
{
  "_id": "69219be4fb684e3dde384058",
  "username": "admin",
  "email": "admin@test.com",
  "is_active": true
}
```

Go check it in Atlas now! 🚀
