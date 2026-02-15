# Deployment Guide - Cloud Gaming Optimizer

## Vercel Deployment (Recommended)

This project is configured for deployment on **Vercel**, a serverless platform perfect for Flask applications.

### Prerequisites
- GitHub account
- Vercel account (free at https://vercel.com)
- Repository pushed to GitHub

### Deployment Steps

#### 1. **Connect Repository to Vercel**
```bash
# Push your code to GitHub (already done)
git push origin main

# Create account at vercel.com if you haven't already
# Import project: https://vercel.com/new
# Select: GitHub > MRADUL142/cloudgamingoptimizer
```

#### 2. **Configure Environment**
In Vercel Dashboard:
- Go to Settings > Environment Variables
- Add:
  - `PYTHONPATH` = `.`
  - `FLASK_ENV` = `production`

#### 3. **Deploy**
Vercel will automatically:
- Install dependencies from `requirements.txt`
- Build the application
- Deploy to production

Your app will be live at: `https://cloudgamingoptimizer.vercel.app/`

### Local Development

#### 1. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. **Install Dependencies**
```bash
pip install -r cloud_gaming_optimizer/requirements.txt
```

#### 3. **Run Locally**
```bash
cd cloud_gaming_optimizer
python web_app.py
```

Access at: `http://localhost:5000`

### Available Endpoints

- `GET /` - Main dashboard (HTML)
- `GET /api/metrics` - Current network & system metrics (JSON)
- `GET /api/optimize` - Optimization recommendations (JSON)
- `GET /api/alerts` - Performance alerts (JSON)
- `GET /api/stats` - Performance statistics (JSON)
- `GET /api/history` - Metrics history (JSON)
- `GET /health` - Health check (JSON)

### Docker Deployment (Alternative)

To deploy using Docker:

#### 1. **Build Image**
```bash
docker build -t cloudgamingoptimizer .
```

#### 2. **Run Container**
```bash
docker run -p 5000:5000 cloudgamingoptimizer
```

### Troubleshooting

**Issue: 404 on Vercel**
- Check that `vercel.json` exists in root
- Verify `requirements.txt` is in `cloud_gaming_optimizer/` directory
- Check Vercel deployment logs in dashboard

**Issue: Import Errors**
- Ensure all dependencies are in `requirements.txt`
- Check that `sys.path` is correctly configured
- Verify all modules are properly initialized

**Issue: Slow Performance**
- Some metrics collection is CPU-intensive
- Consider caching results with shorter collection intervals
- Add rate limiting if needed

### Performance Notes

⚠️ **Important for Production:**
- Network metrics collection (speedtest) can take 1-2 minutes
- GPU metrics may not work in serverless environment
- Consider implementing caching for frequently called endpoints
- Use connection pooling for database if added

### Next Steps

1. ✅ Code is deployed and tested
2. 📊 Monitor performance in Vercel dashboard
3. 🔄 Set up CI/CD with GitHub Actions (optional)
4. 📈 Add database for historical data (optional)
5. 🔐 Add authentication for sensitive endpoints (optional)

---

**Status**: Ready for production ✅
**Last Updated**: 2026-02-15
