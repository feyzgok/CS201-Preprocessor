import os
import shutil
from config import ASSESSMENT_PATH, ZERO_POINTS_PATH

assessment_path = ASSESSMENT_PATH
zeropointassessment_path = ZERO_POINTS_PATH
copied_count = 0

# Hedef klasör yoksa oluştur
os.makedirs(zeropointassessment_path, exist_ok=True)

# Sadece assessment klasörünün içinde dönüyoruz
for root, dirs, files in os.walk(assessment_path):
    for file in files:
        if file.endswith(".txt"):
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Metindeki geçiş sayılarını buluyoruz
                assessment_count = content.count("ASSESSMENT")
                zero_pts_count = content.count("grade 0 pts")
                
                # Hem ASSESSMENT hem de grade 0 pts sayıları birbirine eşitse
                # (Assessment klasöründe olduğu için assessment_count > 0 olmalıdır)
                if assessment_count == zero_pts_count and assessment_count > 0:
                    # Dosyayı kopyalıyoruz
                    target_path = os.path.join(zeropointassessment_path, file)
                    shutil.copy(file_path, target_path)
                    print(f"[KOPYALANDI] {file} -> ASSESSMENT: {assessment_count}, grade 0 pts: {zero_pts_count}")
                    copied_count += 1
            except Exception as e:
                print(f"[HATA] Dosya okunurken sorun oluştu ({file}): {e}")

print("\n" + "="*50)
print(f"İşlem Tamamlandı! Toplam {copied_count} adet 0 puanlık dosya {zeropointassessment_path} konumuna kopyalandı.")
print("="*50 + "\n")