import os
from config import ASSESSMENT_PATH

assessment_path = ASSESSMENT_PATH
deleted_count = 0

if not os.path.exists(assessment_path):
    print(f"[HATA] Klasör bulunamadı: {assessment_path}")
else:
    # Sadece assessment klasörünün içinde dönüyoruz
    for root, dirs, files in os.walk(assessment_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Dosya içeriğinde 'violation' kelimesi geçiyorsa
                    if "violation" in content.lower():
                        os.remove(file_path)
                        print(f"[SİLİNDİ] {file} (violation içeriyor)")
                        deleted_count += 1
                except Exception as e:
                    print(f"[HATA] Dosya okunurken/silinirken sorun oluştu ({file}): {e}")

    print("\n" + "="*50)
    print(f"İşlem Tamamlandı! Toplam {deleted_count} adet 'violation' içeren dosya silindi.")
    print("="*50 + "\n")
