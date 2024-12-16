from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

# Inisialisasi Flask dan Flask-Login
app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Inisialisasi database
def init_db():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()

    # Membuat tabel untuk produk
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # Membuat tabel untuk pengguna
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Membuat tabel untuk transaksi
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Menambahkan admin jika belum ada
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    conn.commit()
    conn.close()

# Model pengguna
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
    user_data = c.fetchone()
    conn.close()
    if user_data:
        return User(*user_data)
    return None

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user_data = c.fetchone()
        conn.close()

        if user_data and user_data[2] == password:
            user = User(*user_data)
            login_user(user)
            return redirect(url_for('dashboard'))
        return "Pergi Penyusup 🤬", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect('store.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists", 400
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE stock > 0")  # Produk dengan stok tersedia
    products = c.fetchall()
    conn.close()

    print("Products:", products)  # Debug log

    return render_template('dashboard.html', products=products)

@app.route('/products')
@login_required
def products():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']

        try:
            conn = sqlite3.connect('store.db')
            c = conn.cursor()
            c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            conn.commit()
            conn.close()
            return redirect(url_for('products'))
        except sqlite3.Error as e:
            return f"Database error: {e}", 500
    return render_template('add_product.html')

@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    conn = sqlite3.connect('store.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']

        c.execute("UPDATE products SET name = ?, price = ?, stock = ? WHERE id = ?", (name, price, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('products'))

    c.execute("SELECT * FROM products WHERE id = ?", (id,))
    product = c.fetchone()
    conn.close()
    return render_template('update_product.html', product=product)

@app.route('/delete_product/<int:id>', methods=['GET'])
@login_required
def delete_product(id):
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('products'))

# Fungsi tambahan dan main
def add_sample_products():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    # c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", ('Produk A', 10000, 50))
    # c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", ('Produk B', 20000, 30))
    # c.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", ('Produk C', 15000, 20))
    conn.commit()
    conn.close()

# Route untuk mencari produk
@app.route('/search_product', methods=['GET, POST'])
def search_product():
    if request.method == 'POST':
        search_query = request.form['search_query']
        
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        print("Masuk")
        c.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + search_query + '%',))
        products = c.fetchall()
        conn.close()
        
        return render_template('start_transactions.html', products=products)

@app.route('/transactions')
def transactions():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    
    # Ambil semua data transaksi dengan informasi produk
    c.execute("""
        SELECT t.id, p.name, t.quantity, t.total
        FROM transactions t
        JOIN products p ON t.product_id = p.id
        ORDER BY t.id DESC
    """)
    transactions = c.fetchall()
    conn.close()

    return render_template('transactions.html', transactions=transactions)

# Route untuk menambahkan produk ke keranjang
@app.route('/add_to_cart/<int:product_id>', methods=['GET'])
def add_to_cart(product_id):
    # Ambil detail produk dari database
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('SELECT id, name, price FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    conn.close()

    if product:
        # Ambil keranjang dari session atau buat keranjang baru jika kosong
        cart = session.get('cart', [])

        # Cek apakah produk sudah ada di keranjang
        for item in cart:
            if item['id'] == product[0]:
                item['quantity'] += 1  # Tambah jumlah produk jika sudah ada
                break
        else:
            # Tambahkan produk baru ke keranjang
            cart.append({
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'quantity': 1
            })

        # Simpan kembali keranjang ke session
        session['cart'] = cart

    return redirect(url_for('start_transaction'))

@app.route('/remove_from_cart/<int:product_id>', methods=['GET'])
@login_required
def remove_from_cart(product_id):
    # Mengambil keranjang dari session
    carts = session.get('carts', [])

    # Menghapus produk dari keranjang
    carts = [item for item in carts if item['id'] != product_id]

    # Simpan kembali ke session
    session['carts'] = carts

    return redirect(url_for('start_transaction'))

# Route untuk memulai transaksi
# Route untuk memulai transaksi
@app.route('/start_transaction', methods=['GET', 'POST'])
def start_transaction():
    # Logika pencarian produk
    products = []
    if request.method == 'POST':
        search_query = request.form['search_query']
        conn = sqlite3.connect('store.db')
        c = conn.cursor()
        c.execute("SELECT id, name, price, stock FROM products WHERE name LIKE ?", 
                  ('%' + search_query + '%',))
        products = c.fetchall()
        conn.close()

    # Ambil keranjang dari session
    cart = session.get('cart', [])

    return render_template('start_transaction.html', products=products, carts=cart)

# Route untuk checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', [])  # Ambil keranjang dari session
    total_price = sum(item['price'] * item['quantity'] for item in cart)  # Hitung total harga

    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'cash')  # Ambil metode pembayaran

        # Simpan transaksi ke database
        conn = sqlite3.connect('store.db')
        c = conn.cursor()

        for item in cart:
            c.execute("""
                INSERT INTO transactions (product_id, quantity, total)
                VALUES (?, ?, ?)
            """, (item['id'], item['quantity'], item['price'] * item['quantity']))

            # Update stok produk
            c.execute("""
                UPDATE products
                SET stock = stock - ?
                WHERE id = ?
            """, (item['quantity'], item['id']))

        conn.commit()
        conn.close()

        session.pop('cart', None)  # Kosongkan keranjang setelah transaksi selesai
        return redirect(url_for('transactions'))  # Redirect ke halaman riwayat transaksi

    return render_template('checkout.html', carts=cart, total_price=total_price)


# Route untuk menampilkan halaman sukses
@app.route('/checkout_success')
def checkout_success():
    return redirect(url_for('transactions'))

# @app.route('/complete_transaction', methods=['GET', 'POST'])
# @login_required
# def complete_transaction():
#     cart = session.get('cart', [])
#     if not cart:
#         return "Keranjang kosong, tidak bisa menyelesaikan transaksi.", 400

#     total_price = sum(item['subtotal'] for item in cart)

#     if request.method == 'GET':
#         return render_template('input_cash.html', total_price=total_price)

#     if request.method == 'POST':
#         # Pastikan data form memiliki key "cash"
#         if 'cash' not in request.form:
#             return "Jumlah uang tunai tidak ditemukan.", 400

#         try:
#             cash = float(request.form['cash'])  # Ambil jumlah uang dari form
#             if cash < total_price:
#                 return f"Uang yang diberikan kurang. Total: {total_price}, Diberikan: {cash}", 400

#             change = cash - total_price

#             # Simpan transaksi
#             conn = sqlite3.connect('store.db')
#             c = conn.cursor()
#             for item in cart:
#                 c.execute(
#                     "INSERT INTO transactions (product_id, quantity, total) VALUES (?, ?, ?)",
#                     (item['id'], item['quantity'], item['subtotal']),
#                 )
#                 c.execute(
#                     "UPDATE products SET stock = stock - ? WHERE id = ?",
#                     (item['quantity'], item['id']),
#                 )
#             conn.commit()
#             conn.close()

#             # Bersihkan keranjang
#             session.pop('cart', None)

#             return f"Transaksi selesai. Total: {total_price}, Diberikan: {cash}, Kembalian: {change}"

#         except ValueError:
#             return "Jumlah uang tunai harus berupa angka.", 400
#         except sqlite3.Error as e:
#             return f"Database error: {e}", 500

# @app.route('/delete_all_products', methods=['POST'])
# @login_required
# def delete_all_products():
#     try:
#         conn = sqlite3.connect('store.db')
#         c = conn.cursor()
#         c.execute("DELETE FROM products")  # Menghapus semua data dari tabel products
#         conn.commit()
#         conn.close()
#         return "Semua produk telah dihapus.", 200
#     except sqlite3.Error as e:
#         return f"Database error: {e}", 500

#@app.route('/print_receipt/<transaction_id>')
#def print_receipt(transaction_id):
#    transaction = get_transaction_by_id(transaction_id)  # Fungsi untuk mengambil data transaksi
#    return render_template('print_receipt.html', transaction=transaction)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)