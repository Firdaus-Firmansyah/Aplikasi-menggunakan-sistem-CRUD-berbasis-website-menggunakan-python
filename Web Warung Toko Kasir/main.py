import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv

# Koneksi ke database SQLite
conn = sqlite3.connect('stok_toko.db')
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    stok INTEGER NOT NULL,
    harga REAL NOT NULL
)
""")
conn.commit()

# Fungsi Tambah Produk
def tambah_produk():
    nama = entry_nama.get()
    stok = entry_stok.get()
    harga = entry_harga.get()

    if not nama or not stok.isdigit() or not harga.replace('.', '', 1).isdigit():
        messagebox.showerror("Input Error", "Masukkan data yang valid!")
        return

    cursor.execute("INSERT INTO produk (nama, stok, harga) VALUES (?, ?, ?)", (nama, int(stok), float(harga)))
    conn.commit()
    messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")
    refresh_tabel()

# Fungsi Update Produk
def update_produk():
    selected_item = tabel.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin diperbarui!")
        return

    item_id = tabel.item(selected_item)['values'][0]
    stok = entry_stok.get()
    harga = entry_harga.get()

    if not stok.isdigit() or not harga.replace('.', '', 1).isdigit():
        messagebox.showerror("Input Error", "Masukkan data yang valid!")
        return

    cursor.execute("UPDATE produk SET stok = ?, harga = ? WHERE id = ?", (int(stok), float(harga), item_id))
    conn.commit()
    messagebox.showinfo("Sukses", "Produk berhasil diperbarui!")
    refresh_tabel()

# Fungsi Hapus Produk
def hapus_produk():
    selected_item = tabel.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin dihapus!")
        return

    item_id = tabel.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM produk WHERE id = ?", (item_id,))
    conn.commit()
    messagebox.showinfo("Sukses", "Produk berhasil dihapus!")
    refresh_tabel()

# Fungsi Refresh Tabel
def refresh_tabel():
    for row in tabel.get_children():
        tabel.delete(row)

    cursor.execute("SELECT * FROM produk")
    for row in cursor.fetchall():
        tabel.insert('', 'end', values=row)

# Fungsi Simpan ke CSV
def simpan_csv():
    with open('stok_toko.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nama Produk', 'Stok', 'Harga'])
        cursor.execute("SELECT * FROM produk")
        writer.writerows(cursor.fetchall())
    messagebox.showinfo("Sukses", "Data berhasil disimpan ke stok_toko.csv!")

# GUI Utama
root = tk.Tk()
root.title("Manajemen Stok Toko")
root.geometry("800x400")

# Form Input
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5)
entry_nama = tk.Entry(frame_form)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Stok:").grid(row=1, column=0, padx=5, pady=5)
entry_stok = tk.Entry(frame_form)
entry_stok.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Harga:").grid(row=2, column=0, padx=5, pady=5)
entry_harga = tk.Entry(frame_form)
entry_harga.grid(row=2, column=1, padx=5, pady=5)

# Tombol Aksi
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Tambah Produk", command=tambah_produk).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Update Produk", command=update_produk).grid(row=0, column=1, padx=10)
tk.Button(frame_buttons, text="Hapus Produk", command=hapus_produk).grid(row=0, column=2, padx=10)
tk.Button(frame_buttons, text="Simpan ke CSV", command=simpan_csv).grid(row=0, column=3, padx=10)

# Tabel Data
tabel = ttk.Treeview(root, columns=('ID', 'Nama', 'Stok', 'Harga'), show='headings')
tabel.pack(pady=10, fill=tk.BOTH, expand=True)

tabel.heading('ID', text='ID')
tabel.heading('Nama', text='Nama Produk')
tabel.heading('Stok', text='Stok')
tabel.heading('Harga', text='Harga')

tabel.column('ID', width=50)
tabel.column('Nama', width=200)
tabel.column('Stok', width=100)
tabel.column('Harga', width=100)

# Load Data Awal
refresh_tabel()

# Menjalankan Aplikasi
root.mainloop()