import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import threading
import os
import shutil
import webbrowser


def indirme_islemi():
    video_url = url_input.get().strip()

    if not video_url:
        messagebox.showwarning("Uyarı", "Lütfen geçerli bir YouTube linki girin!")
        return

    # ffmpeg/ffprobe yoksa kullanıcıyı bilgilendir
    if not ensure_ffmpeg_available():
        open_dl = messagebox.askyesno("FFmpeg Bulunamadı", "FFmpeg veya ffprobe bulunamadı. Devam etmek için kurmanız gerekir. İndirme sayfasını açmak ister misiniz?")
        if open_dl:
            webbrowser.open('https://ffmpeg.org/download.html')
        return

    indir_button.config(state=tk.DISABLED, text="İndiriliyor...", bg="#999999")
    durum_label.config(text="Şarkı indiriliyor, lütfen bekleyin...", fg="#e67e22")
    root.update_idletasks()

    output_dir = output_dir_var.get() or os.getcwd()
    # ffmpeg yolunu belirle (kullanıcı ayarlamışsa, yoksa sistem PATH)
    ffmpeg_path = ffmpeg_path_var.get().strip()
    if not ffmpeg_path:
        ffmpeg_path = shutil.which('ffmpeg') or ''

    def progress_hook(d):
        status = d.get('status')
        if status == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes') or 0
            if total:
                percent = downloaded / total * 100
                durum_label.config(text=f"İndiriliyor... {percent:.1f}%")
        elif status == 'finished':
            durum_label.config(text="Ses indirildi, işleniyor...", fg="#f1c40f")

    def download_thread():
        use_playlist = True
        try:
            use_playlist = bool(playlist_var.get())
        except Exception:
            use_playlist = True

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook],
            'quiet': True,
            'no_warnings': True,
        }

        if use_playlist:
            ydl_opts['outtmpl'] = os.path.join(output_dir, '%(playlist_index)s - %(title)s.%(ext)s')
            ydl_opts['ignoreerrors'] = True
        else:
            ydl_opts['outtmpl'] = os.path.join(output_dir, '%(title)s.%(ext)s')
            ydl_opts['noplaylist'] = True

        # Eğer ffmpeg yolu varsa, yt-dlp'ye ilet (klasör olarak)
        if ffmpeg_path:
            if os.path.isfile(ffmpeg_path):
                ffmpeg_loc = os.path.dirname(ffmpeg_path)
            else:
                ffmpeg_loc = ffmpeg_path
            ydl_opts['ffmpeg_location'] = ffmpeg_loc

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            durum_label.config(text="✓ İndirme Başarıyla Tamamlandı!", fg="#2ecc71")
            messagebox.showinfo("Başarılı", f"Şarkı başarıyla indirildi:\n{output_dir}")
            url_input.delete(0, tk.END)
        except Exception as e:
            durum_label.config(text="X İndirme başarısız oldu!", fg="#e74c3c")
            messagebox.showerror("Hata", f"Bir hata oldu, linki kontrol et:\n{e}")
        finally:
            indir_button.config(state=tk.NORMAL, text="Şarkıyı İndir", bg="#e74c3c")

    threading.Thread(target=download_thread, daemon=True).start()


def ensure_ffmpeg_available():
    # ffmpeg ya PATH'te olmalı ya da kullanıcı tarafından belirtilmiş olmalı
    if ffmpeg_path_var.get().strip():
        candidate = ffmpeg_path_var.get().strip()
        if os.path.isfile(candidate) or os.path.isdir(candidate):
            return True
    if shutil.which('ffmpeg'):
        return True
    return False


# --- Arayüz Tasarımı ---
root = tk.Tk()
root.title("YouTube MP3 Şarkı İndirici")
root.geometry("560x320")
root.configure(bg="#2c3e50")
root.resizable(False, False)

# Başlık
baslik_label = tk.Label(root, text="YouTube Ses İndirici", font=("Arial", 18, "bold"), bg="#2c3e50", fg="#ecf0f1")
baslik_label.pack(pady=16)

# Link Giriş Alanı Etiketi
link_label = tk.Label(root, text="YouTube Video Linkini Yapıştırın:", font=("Arial", 11), bg="#2c3e50", fg="#bdc3c7")
link_label.pack(pady=2)

# Link Giriş Kutusu
url_input = tk.Entry(root, width=60, font=("Arial", 11), bd=3, relief=tk.FLAT)
url_input.pack(pady=6, ipady=6)
url_input.focus()

# Çıktı Klasörü Seçimi
output_dir_var = tk.StringVar(value=os.getcwd())
output_frame = tk.Frame(root, bg="#2c3e50")
output_frame.pack(pady=6)
output_label_text = tk.Label(output_frame, text="Çıktı Klasörü:", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7")
output_label_text.pack(side=tk.LEFT, padx=(0, 6))
output_dir_label = tk.Label(output_frame, text=output_dir_var.get(), font=("Arial", 9), bg="#2c3e50", fg="#ecf0f1")
output_dir_label.pack(side=tk.LEFT)
choose_button = tk.Button(output_frame, text="Değiştir", font=("Arial", 9), bg="#3498db", fg="white", bd=0,
                          activebackground="#2980b9", command=lambda: choose_folder())
choose_button.pack(side=tk.LEFT, padx=8)


# FFmpeg yolu seçimi
ffmpeg_path_var = tk.StringVar(value=shutil.which('ffmpeg') or "")
ff_frame = tk.Frame(root, bg="#2c3e50")
ff_frame.pack(pady=6)
ff_label_text = tk.Label(ff_frame, text="FFmpeg Yolu:", font=("Arial", 10), bg="#2c3e50", fg="#bdc3c7")
ff_label_text.pack(side=tk.LEFT, padx=(0, 6))
ff_label = tk.Label(ff_frame, text=ffmpeg_path_var.get() or "(PATH'te yok)", font=("Arial", 9), bg="#2c3e50", fg="#ecf0f1")
ff_label.pack(side=tk.LEFT)


def choose_ffmpeg():
    filetypes = [("FFmpeg Executable", "*.exe"), ("All files", "*")]
    path = filedialog.askopenfilename(title="FFmpeg yürütülebilir dosyasını seçin", initialdir=os.path.expanduser("~"), filetypes=filetypes)
    if path:
        ffmpeg_path_var.set(path)
        ff_label.config(text=path)

ff_choose_btn = tk.Button(ff_frame, text="FFmpeg Seç", font=("Arial", 9), bg="#9b59b6", fg="white", bd=0, activebackground="#8e44ad", command=choose_ffmpeg)
ff_choose_btn.pack(side=tk.LEFT, padx=8)


# Çalma listesi indir seçeneği
playlist_var = tk.BooleanVar(value=True)
playlist_check = tk.Checkbutton(root, text="Çalma listesini indir (varsa)", variable=playlist_var, bg="#2c3e50", fg="#ecf0f1", selectcolor="#2c3e50", activebackground="#2c3e50", font=("Arial", 10))
playlist_check.pack(pady=4)


def choose_folder():
    folder = filedialog.askdirectory(initialdir=output_dir_var.get() or os.getcwd())
    if folder:
        output_dir_var.set(folder)
        output_dir_label.config(text=folder)

# İndirme Butonu
indir_button = tk.Button(root, text="Şarkıyı İndir", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white",
                         activebackground="#c0392b", activeforeground="white", bd=0, width=20, command=indirme_islemi)
indir_button.pack(pady=12, ipady=6)

# Durum Bildirim Etiketi
durum_label = tk.Label(root, text="Hazır", font=("Arial", 10, "italic"), bg="#2c3e50", fg="#95a5a6")
durum_label.pack(pady=8)

# Uygulamayı Başlat
root.mainloop()