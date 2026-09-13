# Quick Startup Guide - Patiya RedPulse

## 🚀 Getting Started (5 minutes)

### Step 1: Install Dependencies
```bash
pip install django
```

### Step 2: Database Setup
No database ships with this project (on purpose — see Security Notes below).
Create yours locally:
```bash
python manage.py migrate
```

### Step 3: Create Your Own Admin User
There is no default/demo account. Create your own the standard Django way:
```bash
python manage.py createsuperuser
```
You'll be prompted for a username, email, and password interactively — nothing
is hard-coded, and nothing gets printed to a log.

Prefer a non-interactive/scripted setup (e.g. in a deploy pipeline)? Use the
included helper instead, which reads everything from environment variables
and refuses to run if any of them are missing:
```bash
ADMIN_USERNAME=youradmin ADMIN_EMAIL=you@example.com ADMIN_PASSWORD='a-strong-unique-password' \
    python create_admin.py
```

### Step 4: Run the Server
```bash
python manage.py runserver
```

### Step 5: Access the Platform
- **Main Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Custom Admin:** http://127.0.0.1:8000/admin-panel/

## 🧪 Testing the Platform

### 1. Register as a Donor
- Go to http://127.0.0.1:8000/accounts/register/
- Fill in all required fields
- Use a date more than 90 days ago for "Last Blood Donation Date" to see eligibility

### 2. Search for Donors
- Go to http://127.0.0.1:8000/accounts/donors/
- Try searching by blood group, district (e.g., "Chattogram"), upazila (e.g., "Patiya")
- Click "Call" button to test phone functionality

### 3. Submit Blood Request
- Go to http://127.0.0.1:8000/submit-request/
- Fill patient details
- Try both "Normal" and "Emergency" priority levels

### 4. Admin Panel
- Login with admin credentials
- Access http://127.0.0.1:8000/admin-panel/
- View dashboard statistics
- Manage donors and requests

## 🔧 Common Commands

### Run Server
```bash
python manage.py runserver
```

### Create New Admin User
```bash
python manage.py createsuperuser
```

### Access Django Shell
```bash
python manage.py shell
```

### Database Operations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📱 Mobile Testing

To test on mobile devices:

1. **Find your computer's IP address:**
   ```bash
   # Linux/Mac
   ifconfig
   
   # Windows
   ipconfig
   ```

2. **Run server on all interfaces:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

3. **Access from mobile:**
   - Open phone browser
   - Go to: `http://YOUR_COMPUTER_IP:8000/`

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process using port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data!)
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python create_admin.py
```

### Missing Dependencies
```bash
pip install django
```

## 🔐 Security Notes

1. **No demo account ships with this project.** `db.sqlite3` is intentionally
   excluded from the project archive/repo so nobody's real personal data or a
   throwaway admin login ever gets redistributed by accident. Run `migrate`
   and `createsuperuser` yourself (Step 2–3 above) to create a real,
   private admin account.
2. `DEBUG` now defaults to **False**. Set the `DEBUG=True` environment
   variable only on your own machine while developing.
3. **Change `SECRET_KEY`** — set it via the `SECRET_KEY` environment variable
   in production; never reuse the development fallback value in the code.
4. **Configure `ALLOWED_HOSTS`** via the `ALLOWED_HOSTS` environment variable
   (comma-separated) once you have a real domain.
5. `db.sqlite3` is listed in `.gitignore` — if you fork/clone this project,
   keep it that way so donor phone numbers and emails never end up in
   version control or a shared zip file.

## 📊 Database Location

- **Database file:** `db.sqlite3`
- **Location:** Project root directory
- **Backup:** Copy this file to backup your data

## 🌐 Production Deployment

For production:
1. Use a proper web server (Gunicorn, uWSGI)
2. Set up Nginx/Apache
3. Configure SSL/HTTPS
4. Set up database backups
5. Monitor server logs

## 📞 Support

If you encounter issues:
1. Check the browser console for errors
2. Review Django server logs
3. Verify database connectivity
4. Check admin panel for user management

---

**Ready to save lives! 🩸**