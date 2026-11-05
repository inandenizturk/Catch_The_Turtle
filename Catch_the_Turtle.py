import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(master_secret):
    """Girilen şifreyi Fernet için geçerli 32-byte url-safe base64 anahtarına çevirir."""
    hasher = hashlib.sha256(master_secret.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(hasher)

def save_and_encrypt():
    title = title_entry.get().strip()
    message = secret_text.get("1.0", tk.END).strip()
    master_key = master_entry.get().strip()

    if not title or not message or not master_key:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurunuz!")
        return

    # Şifreleme
    key = generate_key(master_key)
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode('utf-8')).decode('utf-8')

    # Dosyaya yazma
    try:
        with open("secret_notes.txt", "a", encoding="utf-8") as file:
            file.write(f"{title}\n{encrypted_message}\n\n")

        # Giriş alanlarını temizleme
        title_entry.delete(0, tk.END)
        secret_text.delete("1.0", tk.END)
        master_entry.delete(0, tk.END)
        messagebox.showinfo("Başarılı", "Notunuz şifrelendi ve kaydedildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Dosyaya yazılamadı: {e}")

def decrypt():
    encrypted_message = secret_text.get("1.0", tk.END).strip()
    master_key = master_entry.get().strip()

    if not encrypted_message or not master_key:
        messagebox.showwarning("Eksik Bilgi", "Lütfen şifreli metni ve anahtarı giriniz!")
        return

    try:
        key = generate_key(master_key)
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_message.encode('utf-8')).decode('utf-8')

        secret_text.delete("1.0", tk.END)
        secret_text.insert("1.0", decrypted_message)
    except Exception:
        messagebox.showerror("Hata", "Şifre çözülemedi! Anahtarı veya şifreli metni kontrol ediniz.")

# --- UI Kurulumu ---
window = tk.Tk()
window.title("Secret Notes")
window.config(padx=30, pady=20)

# 1. Logo / Görsel (top_secret.png dosyan aynı klasörde olmalı)
try:
    img = Image.open("top_secret.png")
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(image=photo)
    logo_label.image = photo
    logo_label.pack(pady=10)
except Exception:
    # Görsel yoksa hata vermemesi için boş label
    logo_label = tk.Label(text="🔒 SECRET NOTES", font=("Verdana", 14, "bold"))
    logo_label.pack(pady=10)

# 2. Başlık Girişi
title_label = tk.Label(text="Enter your title", font=("Verdana", 10, "normal"))
title_label.pack(pady=5)
title_entry = tk.Entry(width=35)
title_entry.pack(pady=5)

# 3. Gizli Not Girişi
secret_label = tk.Label(text="Enter your secret", font=("Verdana", 10, "normal"))
secret_label.pack(pady=5)
secret_text = tk.Text(width=35, height=12)
secret_text.pack(pady=5)

# 4. Master Key Girişi
master_label = tk.Label(text="Enter master key", font=("Verdana", 10, "normal"))
master_label.pack(pady=5)
master_entry = tk.Entry(width=35, show="*")
master_entry.pack(pady=5)

# 5. Butonlar
save_btn = tk.Button(text="Save & Encrypt", command=save_and_encrypt)
save_btn.pack(pady=5)

decrypt_btn = tk.Button(text="Decrypt", command=decrypt)
decrypt_btn.pack(pady=5)

window.mainloop()
