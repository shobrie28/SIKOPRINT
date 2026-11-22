from tampilan import judul, garis


def ringkas_spesifikasi(conn, pesanan):
    with conn.cursor() as cur:
        if pesanan["jenis_pesanan"] == "PRINT":
            cur.execute(
                "SELECT * FROM booking_print WHERE kode_booking = %s",
                (pesanan["kode_booking"],),
            )
            b = cur.fetchone()
            if not b:
                return "Detail print tidak ditemukan"
            lembar = b["jumlah_lembar"] * b["jumlah_eksemplar"]
            jilid = "Tanpa Jilid" if b["opsi_jilid"] == "Tanpa" else b["opsi_jilid"]
            teks = f"{b['ukuran_kertas']} {b['pilihan_warna']} {lembar} lbr + {jilid}"
        else:
            cur.execute(
                "SELECT nama_barang, jumlah FROM detail_atk WHERE kode_booking = %s",
                (pesanan["kode_booking"],),
            )
            rincian = cur.fetchall()
            if not rincian:
                return "ATK: Detail kosong"
            teks = "ATK: " + ", ".join(
                f"{(r['nama_barang'].split() or ['Barang'])[0]} x{r['jumlah']}"
                for r in rincian
            )
    return teks if len(teks) <= 28 else teks[:25] + "..."


def tampil_antrean(conn):
    judul("DAFTAR ANTREAN PESANAN MASUK")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM pesanan WHERE status_pesanan != 'Tuntas' "
            "ORDER BY urutan ASC"
        )
        antrean = cur.fetchall()
    print(f"{'NO':<4}{'KODE BOOKING':<14}{'COSTUMER':<15}"
          f"{'DETAIL SPESIFIKASI':<30}{'STATUS'}")
    garis("-")
    if not antrean:
        print("Belum ada pesanan dalam antrean.")
    for no, p in enumerate(antrean, start=1):
        print(f"{str(no) + '.':<4}{p['kode_booking']:<14}"
              f"{p['nama_pemesan'][:13]:<15}"
              f"{ringkas_spesifikasi(conn, p):<30}"
              f"{p['status_pesanan'].upper()}")
    garis("-")
    return antrean
