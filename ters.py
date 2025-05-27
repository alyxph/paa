from datetime import datetime

tugas_list = []

class Tugas:
    def __init__(self, nama, matkul, deadline, prioritas, jenis, tipe):
        self.nama = nama
        self.matkul = matkul
        self.deadline = deadline
        self.prioritas = int(prioritas)
        self.jenis = jenis
        self.tipe = tipe
    
    def hitung_skor(self):
        """
        Fungsi greedy untuk menghitung skor prioritas tugas
        Semakin tinggi skor = semakin penting
        """
        skor = self.prioritas * 10  # Prioritas dasar
        
 
        hari_tersisa = (self.deadline - datetime.now()).days
        
        # Greedy: tugas dengan deadline dekat dapat skor lebih tinggi
        if hari_tersisa <= 1:
            skor += 50  # Deadline hari ini/besok
        elif hari_tersisa <= 3:
            skor += 30  # Deadline 2-3 hari
        elif hari_tersisa <= 7:
            skor += 15  # Deadline seminggu
        
        # Bonus skor berdasarkan tipe
        if self.tipe == 'besar':
            skor += 10
        if self.jenis == 'mandiri':
            skor += 5
            
        return skor
    
    def __str__(self):
        return (f"{self.nama} ({self.matkul}) | "
                f"Deadline: {self.deadline.strftime('%d/%m/%Y')} | "
                f"Prioritas: {self.prioritas} | {self.jenis.title()} | "
                f"Tipe: {self.tipe.title()} | Skor: {self.hitung_skor()}")

def tampilkan_menu():
    """Menampilkan menu utama"""
    print("\n" + "="*50)
    print("    PENJADWAL TUGAS KULIAH - GREEDY ALGORITHM")
    print("="*50)
    print("1. Tambah Tugas Baru")
    print("2. Lihat Semua Tugas") 
    print("3. Lihat Jadwal Prioritas (Greedy)")
    print("4. Cek Deadline Mendesak")
    print("5. Hapus Tugas")
    print("6. Keluar")
    print("="*50)

def input_tanggal():
    """Input tanggal dengan validasi sederhana"""
    while True:
        try:
            print("Format tanggal: DD/MM/YYYY (contoh: 31/12/2025)")
            tanggal_str = input("Masukkan deadline: ")
            tanggal = datetime.strptime(tanggal_str, "%d/%m/%Y")
            
            if tanggal < datetime.now():
                print("❌ Tanggal tidak boleh di masa lalu!")
                continue
                
            return tanggal
        except ValueError:
            print("❌ Format tanggal salah! Gunakan DD/MM/YYYY")

def tambah_tugas():
    """Menambah tugas baru ke dalam list"""
    print("\n📝 TAMBAH TUGAS BARU")
    print("-" * 25)
    
    # Input data tugas
    nama = input("Nama tugas: ").strip()
    if not nama:
        print("❌ Nama tugas tidak boleh kosong!")
        return
    
    matkul = input("Mata kuliah: ").strip()
    if not matkul:
        print("❌ Nama mata kuliah tidak boleh kosong!")
        return
    
    deadline = input_tanggal()
    
    # Input prioritas
    while True:
        try:
            prioritas = int(input("Prioritas (1-5, 5=sangat penting): "))
            if 1 <= prioritas <= 5:
                break
            else:
                print("❌ Prioritas harus antara 1-5!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")
    
    # Input jenis tugas
    while True:
        jenis = input("Jenis tugas (mandiri/kelompok): ").lower().strip()
        if jenis in ['mandiri', 'kelompok']:
            break
        print("❌ Pilih 'mandiri' atau 'kelompok'!")
    
    # Input tipe tugas
    while True:
        tipe = input("Tipe tugas (biasa/besar): ").lower().strip()
        if tipe in ['biasa', 'besar']:
            break
        print("❌ Pilih 'biasa' atau 'besar'!")
    
    # Buat objek tugas dan tambahkan ke list
    tugas_baru = Tugas(nama, matkul, deadline, prioritas, jenis, tipe)
    tugas_list.append(tugas_baru)
    
    print(f"✅ Tugas '{nama}' berhasil ditambahkan!")

def lihat_semua_tugas():
    """Menampilkan semua tugas yang ada"""
    if not tugas_list:
        print("\n📋 Belum ada tugas yang ditambahkan.")
        return
    
    print(f"\n📋 SEMUA TUGAS ({len(tugas_list)} tugas)")
    print("-" * 80)
    
    for i, tugas in enumerate(tugas_list, 1):
        print(f"{i}. {tugas}")

def jadwal_prioritas():
    """
    Implementasi Greedy Algorithm untuk mengurutkan tugas berdasarkan prioritas
    Mirip dengan konsep Huffman tree - yang paling penting/mendesak di atas
    """
    if not tugas_list:
        print("\n📋 Belum ada tugas untuk dijadwalkan.")
        return
    
    # Greedy: urutkan berdasarkan skor tertinggi (paling penting dulu)
    tugas_terurut = sorted(tugas_list, key=lambda x: x.hitung_skor(), reverse=True)
    
    print(f"\n🎯 JADWAL PRIORITAS - GREEDY ALGORITHM")
    print("📊 Tugas diurutkan berdasarkan: prioritas + deadline + tipe")
    print("-" * 80)
    
    for i, tugas in enumerate(tugas_terurut, 1):
        # Tambahkan indikator visual
        if tugas.hitung_skor() >= 60:
            status = "🔴 SANGAT URGENT"
        elif tugas.hitung_skor() >= 40:
            status = "🟡 PENTING"
        else:
            status = "🟢 NORMAL"
            
        print(f"{i}. {status}")
        print(f"   {tugas}")
        print()

def cek_deadline_mendesak():
    """Cek tugas dengan deadline mendesak (dalam 3 hari)"""
    if not tugas_list:
        print("\n📋 Belum ada tugas untuk dicek.")
        return
    
    sekarang = datetime.now()
    tugas_mendesak = []
    
    for tugas in tugas_list:
        hari_tersisa = (tugas.deadline - sekarang).days
        if 0 <= hari_tersisa <= 3:
            tugas_mendesak.append((tugas, hari_tersisa))
    
    if not tugas_mendesak:
        print("\n✅ Tidak ada tugas dengan deadline mendesak!")
        return
    
    print(f"\n⚠️  DEADLINE MENDESAK ({len(tugas_mendesak)} tugas)")
    print("-" * 60)
    
    # Urutkan berdasarkan hari tersisa (greedy: paling dekat dulu)
    tugas_mendesak.sort(key=lambda x: x[1])
    
    for tugas, hari in tugas_mendesak:
        if hari == 0:
            status = "🔴 HARI INI!"
        elif hari == 1:
            status = "🟠 BESOK"
        else:
            status = f"🟡 {hari} hari lagi"
            
        print(f"{status}")
        print(f"   {tugas}")
        print()

def hapus_tugas():
    """Menghapus tugas dari list"""
    if not tugas_list:
        print("\n📋 Tidak ada tugas untuk dihapus.")
        return
    
    lihat_semua_tugas()
    
    try:
        nomor = int(input(f"\nPilih nomor tugas yang akan dihapus (1-{len(tugas_list)}): "))
        if 1 <= nomor <= len(tugas_list):
            tugas_dihapus = tugas_list.pop(nomor - 1)
            print(f"✅ Tugas '{tugas_dihapus.nama}' berhasil dihapus!")
        else:
            print("❌ Nomor tidak valid!")
    except ValueError:
        print("❌ Masukkan nomor yang valid!")

def main():
    """Fungsi utama program"""
    print("🎓 Selamat datang di Penjadwal Tugas Kuliah!")
    print("📚 Menggunakan Greedy Algorithm untuk prioritas optimal")
    
    while True:
        tampilkan_menu()
        
        try:
            pilihan = input("Pilih menu (1-6): ").strip()
            
            if pilihan == '1':
                tambah_tugas()
            elif pilihan == '2':
                lihat_semua_tugas()
            elif pilihan == '3':
                jadwal_prioritas()
            elif pilihan == '4':
                cek_deadline_mendesak()
            elif pilihan == '5':
                hapus_tugas()
            elif pilihan == '6':
                print("\n👋 Terima kasih! Semangat mengerjakan tugas!")
                break
            else:
                print("❌ Pilihan tidak valid! Pilih 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program dihentikan. Sampai jumpa!")
            break
        except Exception as e:
            print(f"❌ Terjadi error: {e}")
        
        input("\nTekan Enter untuk melanjutkan...")

# Jalankan program
if __name__ == "__main__":
    main()