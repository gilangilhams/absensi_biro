# Setup Supabase untuk Sistem Absensi Biro

## Step 1: Buat Akun Supabase

1. Buka https://supabase.com
2. Klik "Start your project"
3. Sign up dengan GitHub atau email
4. Create organization (nama bebas, misal: "Sekolah")
5. Create project baru:
   - **Name**: `absensi_biro`
   - **Database Password**: Simpan password ini! (gunakan untuk migrate nanti)
   - **Region**: Indonesia (ap-southeast-1) atau region terdekat
   - Klik "Create new project" (tunggu 1-2 menit)

## Step 2: Dapatkan Connection String

1. Di dashboard Supabase, buka project Anda
2. Klik **Settings** → **Database**
3. Cari section "Connection string"
4. Pilih "Psycopg2" (bukan URI)
5. Copy connection string yang terlihat seperti:
```
postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres
```

## Step 3: Setup Local Environment

1. Buat file `.env` di folder project:
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
ADMIN_NAME=Administrator
```

2. Ganti `[PASSWORD]` dan `[PROJECT_ID]` dengan nilai sebenarnya

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
# atau
pip install psycopg2-binary python-dotenv
```

## Step 5: Migrate Data Lokal ke Supabase

Jika Anda punya data di SQLite lokal:

```bash
python migrate_to_supabase.py
```

Skrip ini akan:
- ✅ Buat semua tables di Supabase
- ✅ Pindahkan semua data dari SQLite
- ✅ Buat default admin account

## Step 6: Setup Streamlit Secrets untuk Cloud

1. Deploy app ke Streamlit Cloud
2. Di dashboard Streamlit Cloud, klik app Anda
3. Klik **Settings** → **Secrets**
4. Paste ini (ganti dengan nilai sebenarnya):

```toml
database_url = "postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres"
admin_username = "admin"
admin_password = "admin123"
admin_name = "Administrator"
```

## Step 7: Test

Run app locally:
```bash
streamlit run app.py
```

Akses dengan credentials:
- Username: `admin`
- Password: `admin123`

## Troubleshooting

### Error: "DATABASE_URL not found"
- Pastikan `.env` file ada dan filled dengan benar
- Atau setup di Streamlit Cloud Secrets

### Error: "Connection refused"
- Cek CONNECTION_STRING benar
- Pastikan Supabase project sudah fully initialized
- IP Anda mungkin di-block (Supabase allow all by default, tp cek network settings)

### Data tidak ter-migrate
- Run `python migrate_to_supabase.py` lagi
- Atau manual migrate via Supabase SQL Editor

## Info Penting

- Database Anda akan **persistent** - data tidak hilang saat restart
- Free tier Supabase sudah cukup untuk aplikasi ini
- **JANGAN commit `.env` ke GitHub!** (.gitignore sudah include
