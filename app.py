from flask import Flask, request, redirect, session, render_template_string
from database import db

app = Flask(__name__)
app.secret_key = "inventori123"

# ================= LAYOUT UTAMA: SIDEBAR & NAVBAR (AdminLTE Style) =================
def admin_lte_wrapper(title, content, active_menu="dashboard"):
    if "username" not in session:
        return content

    role_badge = "MANAJEMEN" if session.get("role") == "admin" else "PETUGAS"
    
    # Menentukan menu aktif untuk class CSS
    m_dash = "active bg-primary text-white" if active_menu == "dashboard" else "text-light"
    m_masuk = "active bg-primary text-white" if active_menu == "masuk" else "text-light"
    m_keluar = "active bg-primary text-white" if active_menu == "keluar" else "text-light"
    m_riwayat = "active bg-primary text-white" if active_menu == "riwayat" else "text-light"

    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - InventarisApp</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; }}
            .sidebar {{ width: 250px; height: 100vh; position: fixed; top: 0; left: 0; background-color: #212529; z-index: 1000; transition: all 0.3s; }}
            .navbar-top {{ margin-left: 250px; background-color: #ffffff; border-bottom: 1px solid #dee2e6; height: 56px; }}
            .main-content {{ margin-left: 250px; padding-top: 76px; min-height: 100vh; padding-right: 20px; padding-left: 20px; }}
            .nav-link-custom {{ padding: 12px 20px; display: block; text-decoration: none; border-radius: 4px; margin: 4px 10px; transition: 0.2s; }}
            .nav-link-custom:hover {{ background-color: rgba(255,255,255,0.1); color: #fff !important; }}
            @media print {{ .no-print {{ display: none !important; }} .main-content {{ margin-left: 0 !important; padding: 0 !important; }} }}
        </style>
    </head>
    <body>

        <div class="sidebar no-print">
            <div class="p-3 text-white border-bottom border-secondary d-flex align-items-center">
                <i class="fa-solid fa-boxes-stacked fa-xl me-2 text-primary"></i>
                <span class="fs-5 fw-bold">Inventaris<span class="text-primary">App</span></span>
            </div>
            
            <div class="p-3 text-white border-bottom border-secondary d-flex align-items-center">
                <div class="bg-secondary rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px;">
                    <i class="fa-solid fa-user text-white"></i>
                </div>
                <div>
                    <div class="text-white fw-bold small">{session.get('username', 'Admin')}</div>
                    <div class="text-success small" style="font-size: 12px;"><i class="fa-solid fa-circle text-success me-1" style="font-size: 9px;"></i> Online</div>
                </div>
            </div>

            <div class="mt-3">
                <small class="text-muted px-4 d-block mb-2" style="font-size: 10px; letter-spacing: 1px; font-weight: bold;">MAIN NAVIGATION</small>
                <a href="/dashboard" class="nav-link-custom {m_dash}"><i class="fa-solid fa-gauge me-2"></i> DASHBOARD</a>
                <a href="/masuk" class="nav-link-custom {m_masuk}"><i class="fa-solid fa-arrow-right-to-bracket me-2"></i> BARANG MASUK</a>
                <a href="/keluar" class="nav-link-custom {m_keluar}"><i class="fa-solid fa-arrow-right-from-bracket me-2"></i> BARANG KELUAR</a>
                <a href="/riwayat" class="nav-link-custom {m_riwayat}"><i class="fa-solid fa-file-invoice me-2"></i> LAPORAN</a>
                <a href="/logout" class="nav-link-custom text-danger mt-4"><i class="fa-solid fa-power-off me-2"></i> LOGOUT</a>
            </div>
        </div>

        <nav class="navbar navbar-expand fixed-top navbar-top shadow-sm px-3 no-print">
            <div class="container-fluid">
                <span class="navbar-text fw-semibold text-dark">Sistem Informasi Manajemen</span>
                <div class="ms-auto d-flex align-items-center gap-3">
                    <span class="badge bg-success px-2 py-1">{role_badge}</span>
                    <span class="text-muted small"><i class="fa-solid fa-user-lock me-1"></i> {session.get('username', 'Admin')}</span>
                </div>
            </div>
        </nav>

        <div class="main-content">
            {content}
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


# ================= ROUTE: LOGIN =================

@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            db.ping(reconnect=True)
        except:
            pass

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")

        return """
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <div class="container mt-5 text-center"><div class="alert alert-danger d-inline-block">Login Gagal! Username/Password salah.</div><br><a href="/" class="btn btn-primary">Kembali</a></div>
        """

    return """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <title>Login - InventarisApp</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #e9ecef; height: 100vh; display: flex; align-items: center; justify-content: center; }
            .login-card { width: 400px; border-top: 4px solid #007bff; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="card shadow login-card">
            <div class="card-body p-4">
                <h3 class="text-center fw-bold mb-2">Inventaris<span class="text-primary">App</span></h3>
                <p class="text-center text-muted small mb-4">Silakan login untuk mengelola sistem</p>
                <form method="post">
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input name="username" class="form-control" placeholder="Username" required autofocus>
                    </div>
                    <div class="mb-4">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" placeholder="Password" required>
                    </div>
                    <button class="btn btn-primary w-100 fw-bold">LOG IN</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """


# ================= ROUTE: DASHBOARD =================

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    # Cek & sambung ulang otomatis ke TiDB Cloud jika terputus
    try:
        db.ping(reconnect=True)
    except:
        pass

    cursor = db.cursor()
    cursor.execute("SELECT * FROM barang")
    barang = cursor.fetchall()

    # Perhitungan data agregat statistika untuk widget atas
    total_model = len(barang)
    total_stok = sum(b[4] for b in barang)
    stok_kritis = len([b for b in barang if b[4] <= 5])
    
    cursor.execute("SELECT COUNT(*) FROM transaksi WHERE jenis_transaksi='Masuk'")
    t_masuk = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM transaksi WHERE jenis_transaksi='Keluar'")
    t_keluar = cursor.fetchone()[0]
    cursor.close()

    # HTML dashboard murni
    dashboard_html = """
    <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
            <h2 class="fw-normal m-0 d-inline-block">Dashboard</h2>
            <small class="text-muted ms-2">Control panel</small>
        </div>
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb m-0 small">
                <li class="breadcrumb-item"><a href="/dashboard" class="text-decoration-none"><i class="fa-solid fa-home"></i> Home</a></li>
                <li class="breadcrumb-item active">Dashboard</li>
            </ol>
        </nav>
    </div>

    <div class="row g-3 mb-4 no-print">
        <div class="col-lg-3 col-6">
            <div class="card bg-success text-white border-0 shadow-sm">
                <div class="card-body p-3 d-flex justify-content-between align-items-center" style="min-height: 110px;">
                    <div>
                        <h1 class="fw-bold mb-1">{{ total_model }}</h1>
                        <p class="m-0 small text-white-50">Model Barang</p>
                    </div>
                    <i class="fa-solid fa-chart-bar fa-3x opacity-25"></i>
                </div>
                <div class="card-footer bg-dark bg-opacity-10 text-center py-1"><small class="text-white-50">More info <i class="fa-solid fa-circle-arrow-right"></i></small></div>
            </div>
        </div>
        <div class="col-lg-3 col-6">
            <div class="card bg-warning text-dark border-0 shadow-sm">
                <div class="card-body p-3 d-flex justify-content-between align-items-center" style="min-height: 110px;">
                    <div>
                        <h1 class="fw-bold mb-1">{{ total_stok }}</h1>
                        <p class="m-0 small text-black-50">Total Volume Stok</p>
                    </div>
                    <i class="fa-solid fa-boxes-stacked fa-3x opacity-25"></i>
                </div>
                <div class="card-footer bg-dark bg-opacity-10 text-center py-1"><small class="text-black-50">More info <i class="fa-solid fa-circle-arrow-right"></i></small></div>
            </div>
        </div>
        <div class="col-lg-3 col-6">
            <div class="card bg-danger text-white border-0 shadow-sm">
                <div class="card-body p-3 d-flex justify-content-between align-items-center" style="min-height: 110px;">
                    <div>
                        <h1 class="fw-bold mb-1">{{ stok_kritis }}</h1>
                        <p class="m-0 small text-white-50">Stok Kritis (<=5)</p>
                    </div>
                    <i class="fa-solid fa-triangle-exclamation fa-3x opacity-25"></i>
                </div>
                <div class="card-footer bg-dark bg-opacity-10 text-center py-1"><small class="text-white-50">More info <i class="fa-solid fa-circle-arrow-right"></i></small></div>
            </div>
        </div>
        <div class="col-lg-3 col-6">
            <div class="card bg-info text-white border-0 shadow-sm">
                <div class="card-body p-3 d-flex justify-content-between align-items-center" style="min-height: 110px;">
                    <div>
                        <h1 class="fw-bold mb-1">{{ t_masuk + t_keluar }}</h1>
                        <p class="m-0 small text-white-50">Total Transaksi</p>
                    </div>
                    <i class="fa-solid fa-clock-rotate-left fa-3x opacity-25"></i>
                </div>
                <div class="card-footer bg-dark bg-opacity-10 text-center py-1"><small class="text-white-50">More info <i class="fa-solid fa-circle-arrow-right"></i></small></div>
            </div>
        </div>
    </div>

    <div class="card border-0 shadow-sm mb-4">
        <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
            <h5 class="m-0 fw-bold text-dark"><i class="fa-solid fa-table me-2 text-secondary"></i>Data Master Barang</h5>
            {% if role == "admin" %}
            <a href="/tambah" class="btn btn-sm btn-success fw-bold"><i class="fa-solid fa-plus me-1"></i> Tambah Barang</a>
            {% endif %}
        </div>
        <div class="card-body">
            <div class="mb-3">
                <input type="text" id="inputCari" class="form-control" placeholder="🔍 Ketik nama, kode, atau kategori untuk mencari barang...">
            </div>
            <div class="table-responsive">
                <table class="table table-bordered table-hover align-middle m-0">
                    <thead class="table-light">
                        <tr>
                            <th width="60">ID</th>
                            <th>Kode</th>
                            <th>Nama Barang</th>
                            <th>Kategori</th>
                            <th>Stok Tersedia</th>
                            <th>Harga Satuan</th>
                            {% if role == "admin" %}
                            <th class="text-center" width="130">Aksi</th>
                            {% endif %}
                        </tr>
                    </thead>
                    <tbody>
                        {% for b in barang %}
                        <tr>
                            <td>{{ b[0] }}</td>
                            <td><span class="badge bg-light text-dark border font-monospace">{{ b[1] }}</span></td>
                            <td><strong>{{ b[2] }}</strong></td>
                            <td>{{ b[3] }}</td>
                            <td>
                                {% if b[4] <= 5 %}
                                <span class="badge bg-danger p-2 d-block text-center text-white">Kritis: {{ b[4] }} Pcs</span>
                                {% else %}
                                <span class="badge bg-primary p-2 d-block text-center text-white">{{ b[4] }} Pcs</span>
                                {% endif %}
                            </td>
                            <td>Rp {{ "{:,.0f}".format(b[5]) }}</td>
                            {% if role == "admin" %}
                            <td class="text-center">
                                <div class="btn-group btn-group-sm">
                                    <a href="/edit/{{ b[0] }}" class="btn btn-warning text-white"><i class="fa-solid fa-pen-to-square"></i></a>
                                    <a href="/hapus/{{ b[0] }}" class="btn btn-danger" onclick="return confirm('Hapus barang ini?')"><i class="fa-solid fa-trash"></i></a>
                                </div>
                            </td>
                            {% endif %}
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="7" class="text-center py-4 text-muted">Belum ada barang di dalam sistem.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="card border-0 shadow-sm" style="max-width: 500px;">
        <div class="card-header bg-white border-bottom fw-bold text-dark">Detail Login</div>
        <div class="card-body p-0">
            <table class="table table-sm m-0 align-middle">
                <tbody>
                    <tr><td class="p-3 text-muted" width="180">Nama</td><td class="p-3 fw-semibold">{{ user }}</td></tr>
                    <tr><td class="p-3 text-muted">Username</td><td class="p-3 font-monospace">{{ user }}</td></tr>
                    <tr><td class="p-3 text-muted">Level Hak Akses</td><td class="p-3"><span class="badge bg-success">{% if role == 'admin' %}MANAJEMEN{% else %}PETUGAS{% endif %}</span></td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <script>
    document.getElementById('inputCari').addEventListener('keyup', function() {
        let keyword = this.value.toLowerCase();
        let rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            if(row.closest('table').parentElement.classList.contains('table-responsive')) {
                row.style.display = row.textContent.toLowerCase().includes(keyword) ? '' : 'none';
            }
        });
    });
    </script>
    """
    
    rendered_content = render_template_string(
        dashboard_html, 
        barang=barang, 
        user=session.get("username", "Admin"), 
        role=session.get("role", "admin"), 
        total_model=total_model, 
        total_stok=total_stok, 
        stok_kritis=stok_kritis, 
        t_masuk=t_masuk, 
        t_keluar=t_keluar
    )
    
    return admin_lte_wrapper("Dashboard", rendered_content, active_menu="dashboard")


# ================= ROUTE: TAMBAH BARANG =================

@app.route("/tambah", methods=["GET", "POST"])
def tambah():
    if session.get("role") != "admin":
        return redirect("/dashboard")

    if request.method == "POST":
        try:
            db.ping(reconnect=True)
        except:
            pass
        cursor = db.cursor()
        cursor.execute("INSERT INTO barang (kode_barang, nama_barang, kategori, stok, harga) VALUES (%s,%s,%s,%s,%s)",
            (request.form["kode"], request.form["nama"], request.form["kategori"], request.form["stok"], request.form["harga"]))
        db.commit()
        cursor.close()
        return redirect("/dashboard")

    html_content = """
    <div class="card border-0 shadow-sm mx-auto" style="max-width: 700px;">
        <div class="card-header bg-white py-3 fw-bold text-dark"><i class="fa-solid fa-plus text-success me-2"></i>Tambah Barang Baru</div>
        <div class="card-body">
            <form method="post" class="row g-3">
                <div class="col-md-6"><label class="form-label fw-semibold">Kode Barang</label><input name="kode" class="form-control" placeholder="BRG00x" required></div>
                <div class="col-md-6"><label class="form-label fw-semibold">Nama Barang</label><input name="nama" class="form-control" required></div>
                <div class="col-md-6"><label class="form-label fw-semibold">Kategori</label><input name="kategori" class="form-control" required></div>
                <div class="col-md-3"><label class="form-label fw-semibold">Stok Awal</label><input type="number" name="stok" class="form-control" required></div>
                <div class="col-md-3"><label class="form-label fw-semibold">Harga Satuan</label><input type="number" name="harga" class="form-control" required></div>
                <div class="col-12 border-top pt-3 mt-4">
                    <button class="btn btn-success fw-bold px-4">Simpan</button>
                    <a href="/dashboard" class="btn btn-secondary px-4">Batal</a>
                </div>
            </form>
        </div>
    </div>
    """
    return admin_lte_wrapper("Tambah Barang", html_content, active_menu="dashboard")


# ================= ROUTE: EDIT BARANG =================

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    if session.get("role") != "admin":
        return redirect("/dashboard")

    try:
        db.ping(reconnect=True)
    except:
        pass

    cursor = db.cursor()
    if request.method == "POST":
        cursor.execute("UPDATE barang SET nama_barang=%s, kategori=%s, stok=%s, harga=%s WHERE id_barang=%s",
            (request.form["nama"], request.form["kategori"], request.form["stok"], request.form["harga"], id))
        db.commit()
        cursor.close()
        return redirect("/dashboard")

    cursor.execute("SELECT * FROM barang WHERE id_barang=%s", (id,))
    b = cursor.fetchone()
    cursor.close()

    html_content = f"""
    <div class="card border-0 shadow-sm mx-auto" style="max-width: 700px;">
        <div class="card-header bg-white py-3 fw-bold text-warning"><i class="fa-solid fa-edit me-2"></i>Edit Data Barang</div>
        <div class="card-body">
            <form method="post" class="row g-3">
                <div class="col-md-6"><label class="form-label fw-semibold">Nama Barang</label><input name="nama" value="{b[2]}" class="form-control" required></div>
                <div class="col-md-6"><label class="form-label fw-semibold">Kategori</label><input name="kategori" value="{b[3]}" class="form-control" required></div>
                <div class="col-md-6"><label class="form-label fw-semibold">Stok</label><input type="number" name="stok" value="{b[4]}" class="form-control" required></div>
                <div class="col-md-6"><label class="form-label fw-semibold">Harga (Rp)</label><input type="number" name="harga" value="{b[5]}" class="form-control" required></div>
                <div class="col-12 border-top pt-3 mt-4">
                    <button class="btn btn-warning text-white fw-bold px-4">Simpan Perubahan</button>
                    <a href="/dashboard" class="btn btn-secondary px-4">Batal</a>
                </div>
            </form>
        </div>
    </div>
    """
    return admin_lte_wrapper("Edit Barang", html_content, active_menu="dashboard")


# ================= ROUTE: HAPUS BARANG =================

@app.route("/hapus/<id>")
def hapus(id):
    if session.get("role") != "admin":
        return redirect("/dashboard")
    
    try:
        db.ping(reconnect=True)
    except:
        pass
    cursor = db.cursor()
    cursor.execute("DELETE FROM barang WHERE id_barang=%s", (id,))
    db.commit()
    cursor.close()
    return redirect("/dashboard")


# ================= ROUTE: BARANG MASUK =================

@app.route("/masuk", methods=["GET", "POST"])
def masuk():
    if "username" not in session:
        return redirect("/")

    try:
        db.ping(reconnect=True)
    except:
        pass

    cursor = db.cursor()
    if request.method == "POST":
        id_barang = request.form["id_barang"]
        jumlah = int(request.form["jumlah"])
        cursor.execute("UPDATE barang SET stok = stok + %s WHERE id_barang=%s", (jumlah, id_barang))
        cursor.execute("INSERT INTO transaksi (id_barang, jenis_transaksi, jumlah) VALUES (%s,'Masuk',%s)", (id_barang, jumlah))
        db.commit()
        cursor.close()
        return redirect("/dashboard")

    cursor.execute("SELECT * FROM barang")
    data = cursor.fetchall()
    cursor.close()

    form_html = """
    <div class="card border-0 shadow-sm mx-auto" style="max-width: 600px;">
        <div class="card-header bg-info text-white py-3 fw-bold"><i class="fa-solid fa-arrow-right-to-bracket me-2"></i>Input Transaksi Barang Masuk</div>
        <div class="card-body">
            <form method="post">
                <div class="mb-3">
                    <label class="form-label fw-semibold">Pilih Barang</label>
                    <select name="id_barang" class="form-select">
                        {% for b in barang %}
                        <option value="{{b[0]}}">{{b[2]}} (Stok Saat Ini: {{b[4]}})</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-semibold">Jumlah Kuantitas Masuk</label>
                    <input type="number" name="jumlah" class="form-control" min="1" required>
                </div>
                <button class="btn btn-info text-white fw-bold px-4">Proses Masuk</button>
                <a href="/dashboard" class="btn btn-secondary px-4">Batal</a>
            </form>
        </div>
    </div>
    """
    return admin_lte_wrapper("Barang Masuk", render_template_string(form_html, barang=data), active_menu="masuk")


# ================= ROUTE: BARANG KELUAR =================

@app.route("/keluar", methods=["GET", "POST"])
def keluar():
    if "username" not in session:
        return redirect("/")

    try:
        db.ping(reconnect=True)
    except:
        pass

    cursor = db.cursor()
    if request.method == "POST":
        id_barang = request.form["id_barang"]
        jumlah = int(request.form["jumlah"])
        
        cursor.execute("SELECT stok FROM barang WHERE id_barang=%s", (id_barang,))
        stok_ada = cursor.fetchone()[0]
        
        if jumlah > stok_ada:
            cursor.close()
            return "<script>alert('Gagal! Stok gudang tidak mencukupi permintaan.'); window.location='/keluar';</script>"

        cursor.execute("UPDATE barang SET stok = stok - %s WHERE id_barang=%s", (jumlah, id_barang))
        cursor.execute("INSERT INTO transaksi (id_barang, jenis_transaksi, jumlah) VALUES (%s,'Keluar',%s)", (id_barang, jumlah))
        db.commit()
        cursor.close()
        return redirect("/dashboard")

    cursor.execute("SELECT * FROM barang")
    data = cursor.fetchall()
    cursor.close()

    form_html = """
    <div class="card border-0 shadow-sm mx-auto" style="max-width: 600px;">
        <div class="card-header bg-warning text-dark py-3 fw-bold"><i class="fa-solid fa-arrow-right-from-bracket me-2"></i>Input Transaksi Barang Keluar</div>
        <div class="card-body">
            <form method="post">
                <div class="mb-3">
                    <label class="form-label fw-semibold">Pilih Barang</label>
                    <select name="id_barang" class="form-select">
                        {% for b in barang %}
                        <option value="{{b[0]}}">{{b[2]}} (Stok Saat Ini: {{b[4]}})</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="mb-4">
                    <label class="form-label fw-semibold">Jumlah Kuantitas Keluar</label>
                    <input type="number" name="jumlah" class="form-control" min="1" required>
                </div>
                <button class="btn btn-warning fw-bold px-4">Proses Keluar</button>
                <a href="/dashboard" class="btn btn-secondary px-4">Batal</a>
            </form>
        </div>
    </div>
    """
    return admin_lte_wrapper("Barang Keluar", render_template_string(form_html, barang=data), active_menu="keluar")


# ================= ROUTE: RIWAYAT / LAPORAN (Koneksi Stabil Anti-Timeout) =================

@app.route("/riwayat")
def riwayat():
    if "username" not in session:
        return redirect("/")

    # MEMASTIKAN RE-CONNECT KE SERVER TiDB JIKA SEWAKTU-WAKTU PUTUS/TIMEOUT
    try:
        db.ping(reconnect=True, attempts=3, delay=1)
    except Exception:
        pass

    cursor = db.cursor()
    
    try:
        cursor.execute("""
            SELECT transaksi.id_transaksi, barang.nama_barang, transaksi.jenis_transaksi, transaksi.jumlah, transaksi.tanggal
            FROM transaksi JOIN barang ON transaksi.id_barang = barang.id_barang
            ORDER BY transaksi.id_transaksi DESC
        """)
        data = cursor.fetchall()
    except Exception as e:
        return f"""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <div class="container mt-5 text-center">
            <div class="alert alert-warning d-inline-block shadow-sm">
                <h5><i class="fa-solid fa-triangle-exclamation me-2"></i>Koneksi Server Cloud Terputus</h5>
                <p class="m-0 small text-muted">Silakan tekan tombol muat ulang di bawah untuk menyambung kembali.</p>
                <code class="d-block mt-2 small text-danger">{str(e)}</code>
            </div>
            <br><a href="/riwayat" class="btn btn-primary btn-sm mt-2">Muat Ulang Halaman</a>
        </div>
        """
    finally:
        try:
            cursor.close()
        except:
            pass

    table_html = """
    <div class="card border-0 shadow-sm">
        <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
            <h5 class="m-0 fw-bold text-dark"><i class="fa-solid fa-file-invoice me-2 text-secondary"></i>Laporan Mutasi Transaksi Logistik</h5>
            <button onclick="window.print()" class="btn btn-sm btn-outline-primary no-print"><i class="fa-solid fa-print"></i> Cetak Dokumen / PDF</button>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered table-striped m-0 align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th>ID Transaksi</th>
                            <th>Nama Komoditas Barang</th>
                            <th>Status Mutasi</th>
                            <th>Volume Kuantitas</th>
                            <th>Tanggal Update</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for t in transaksi %}
                        <tr>
                            <td>#{{ t[0] }}</td>
                            <td><strong>{{ t[1] }}</strong></td>
                            <td>
                                {% if t[2] == 'Masuk' %}
                                <span class="badge bg-info text-white px-3 py-1">MASUK</span>
                                {% else %}
                                <span class="badge bg-warning text-dark px-3 py-1">KELUAR</span>
                                {% endif %}
                            </td>
                            <td>{{ t[3] }} Unit</td>
                            <td><small class="text-muted font-monospace">{{ t[4] }}</small></td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" class="text-center py-3 text-muted">Belum ada mutasi logistik terekam.</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """
    return admin_lte_wrapper("Laporan Mutasi", render_template_string(table_html, transaksi=data), active_menu="riwayat")


# ================= ROUTE: LOGOUT =================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)