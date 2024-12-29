import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import time
import matplotlib.pyplot as plt
import sys
import random

# Tingkatkan batas kedalaman rekursi
sys.setrecursionlimit(20000)

# Database obat
obat_database = [
    {"nama": "Paracetamol", "harga": 5000, "struktur": "C8H9NO2"},
    {"nama": "Ibuprofen", "harga": 15000, "struktur": "C13H18O2"},
    {"nama": "Amoxicillin", "harga": 20000, "struktur": "C16H19N3O5S"},
]

# Menambahkan 2000 data obat untuk pengujian
for i in range(1, 2001):
    obat_database.append({
        "nama": f"Obat-{i}",
        "harga": random.randint(1000, 100000),
        "struktur": f"Struktur-{i}"
    })

# Fungsi iteratif untuk pencarian obat
def cari_obat_iteratif(keyword, data):
    """
    Pencarian obat secara iteratif.

    keyword: string yang dicari.
    data: list dictionary data obat.
    """
    hasil = []
    n = len(data)
    for i in range(n):
        if keyword.lower() in data[i]["nama"].lower():
            hasil.append(data[i])
    return hasil

# Fungsi rekursif untuk pencarian obat
def cari_obat_rekursif(keyword, data, index=0, hasil=None):
    """
    Pencarian obat secara rekursif.

    keyword: string yang dicari.
    data: list dictionary data obat.
    index: indeks saat ini dalam pencarian.
    hasil: list untuk menyimpan hasil pencarian.
    """
    if hasil is None:
        hasil = []

    # Kondisi basis: jika indeks melebihi panjang data
    if index >= len(data):
        return hasil

    # Cek apakah keyword ditemukan
    if keyword.lower() in data[index]["nama"].lower():
        hasil.append(data[index])

    # Rekursif dengan indeks berikutnya
    return cari_obat_rekursif(keyword, data, index + 1, hasil)

# Fungsi untuk benchmarking
def benchmark_cari_obat(keyword, sizes):
    waktu_iteratif = []
    waktu_rekursif = []

    for size in sizes:
        # Subset data untuk benchmark
        subset = obat_database[:size]

        # Uji fungsi iteratif
        start_iteratif = time.perf_counter()
        cari_obat_iteratif(keyword, subset)
        end_iteratif = time.perf_counter()
        waktu_iteratif.append(end_iteratif - start_iteratif)

        # Uji fungsi rekursif
        start_rekursif = time.perf_counter()
        cari_obat_rekursif(keyword, subset)
        end_rekursif = time.perf_counter()
        waktu_rekursif.append(end_rekursif - start_rekursif)

    return waktu_iteratif, waktu_rekursif

# Fungsi untuk visualisasi hasil benchmarking
def visualisasi_benchmark():
    keyword = entry_keyword.get()

    # Ukuran data untuk benchmark
    sizes = [100, 500, 1000, 1500, 2000]

    waktu_iteratif, waktu_rekursif = benchmark_cari_obat(keyword, sizes)

    # Visualisasi dengan diagram garis
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, waktu_iteratif, marker='o', label='Iteratif', color='blue')
    plt.plot(sizes, waktu_rekursif, marker='o', label='Rekursif', color='orange')
    plt.title("Perbandingan Waktu Eksekusi")
    plt.xlabel("Ukuran Data")
    plt.ylabel("Waktu (detik)")
    plt.legend()
    plt.grid(True)

    for i, size in enumerate(sizes):
        plt.text(size, waktu_iteratif[i], f"{waktu_iteratif[i]:.4f}", ha='right', color='blue')
        plt.text(size, waktu_rekursif[i], f"{waktu_rekursif[i]:.4f}", ha='right', color='orange')

    plt.tight_layout()
    plt.show()

# Fungsi untuk menampilkan hasil pencarian obat
def tampilkan_hasil_pencarian(hasil, judul):
    tabel_obat_window = tk.Toplevel(root)
    tabel_obat_window.title(judul)

    tree = ttk.Treeview(tabel_obat_window, columns=("Nama", "Harga", "Struktur"), show="headings")
    tree.heading("Nama", text="Nama Obat")
    tree.heading("Harga", text="Harga")
    tree.heading("Struktur", text="Struktur")

    for obat in hasil:
        tree.insert("", "end", values=(obat['nama'], obat['harga'], obat['struktur']))

    tree.pack(padx=10, pady=10)

# Fungsi untuk simulasi pencarian obat
def cari_obat_iteratif_gui():
    keyword = entry_keyword.get()
    hasil = cari_obat_iteratif(keyword, obat_database)
    if hasil:
        tampilkan_hasil_pencarian(hasil, "Hasil Pencarian Obat (Iteratif)")
    else:
        messagebox.showinfo("Hasil Pencarian", "Obat tidak ditemukan.")

def cari_obat_rekursif_gui():
    keyword = entry_keyword.get()
    hasil = cari_obat_rekursif(keyword, obat_database)
    if hasil:
        tampilkan_hasil_pencarian(hasil, "Hasil Pencarian Obat (Rekursif)")
    else:
        messagebox.showinfo("Hasil Pencarian", "Obat tidak ditemukan.")

# Fungsi untuk mencari nilai ASCII string dan melakukan pencarian berdasarkan ASCII
def konversi_string_ke_ascii(s):
    return [ord(c) for c in s]

def cari_ascii_iteratif(nilai_ascii):
    return [c for c in range(128) if c == nilai_ascii]

def cari_ascii_rekursif(nilai_ascii, index=0):
    if index >= 128:
        return []
    if index == nilai_ascii:
        return [index]
    return cari_ascii_rekursif(nilai_ascii, index + 1)

def cari_ascii_gui():
    string_input = entry_ascii.get()
    ascii_values = konversi_string_ke_ascii(string_input)

    hasil_iteratif = [cari_ascii_iteratif(val) for val in ascii_values]
    hasil_rekursif = [cari_ascii_rekursif(val) for val in ascii_values]

    tabel_ascii_window = tk.Toplevel(root)
    tabel_ascii_window.title("Hasil Pencarian ASCII")

    tree = ttk.Treeview(tabel_ascii_window, columns=("Karakter", "ASCII", "Iteratif", "Rekursif"), show="headings")
    tree.heading("Karakter", text="Karakter")
    tree.heading("ASCII", text="Nilai ASCII")
    tree.heading("Iteratif", text="Hasil Iteratif")
    tree.heading("Rekursif", text="Hasil Rekursif")

    for i, char in enumerate(string_input):
        tree.insert("", "end", values=(char, ascii_values[i], hasil_iteratif[i], hasil_rekursif[i]))

    tree.pack(padx=10, pady=10)

# GUI Utama
root = tk.Tk()
root.title("Sistem Database dan Analisis Obat")

frame_pencarian = tk.Frame(root)
frame_pencarian.pack(pady=10)

tk.Label(frame_pencarian, text="Masukkan Nama Obat:").grid(row=0, column=0, padx=10, pady=5)
entry_keyword = tk.Entry(frame_pencarian)
entry_keyword.grid(row=0, column=1, padx=10, pady=5)

tk.Button(frame_pencarian, text="Cari Obat (Iteratif)", command=cari_obat_iteratif_gui).grid(row=1, column=0, padx=10, pady=5)
tk.Button(frame_pencarian, text="Cari Obat (Rekursif)", command=cari_obat_rekursif_gui).grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_pencarian, text="Masukkan String:").grid(row=2, column=0, padx=10, pady=5)
entry_ascii = tk.Entry(frame_pencarian)
entry_ascii.grid(row=2, column=1, padx=10, pady=5)

tk.Button(frame_pencarian, text="Cari ASCII", command=cari_ascii_gui).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(frame_pencarian, text="Benchmark dan Visualisasi", command=visualisasi_benchmark).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()