import os
import shutil
from config import EXAM_REPO_PATH, ASSESSMENT_PATH, NONASSESSMENT_PATH

path = EXAM_REPO_PATH
assessment_path = ASSESSMENT_PATH
nonassessment_path = NONASSESSMENT_PATH

os.makedirs(assessment_path, exist_ok=True)
os.makedirs(nonassessment_path, exist_ok=True)

counter = 1

total_assessment = 0
total_nonassessment = 0
total_error = 0

for root, dirs, files in os.walk(path):
    # İstenmeyen klasörleri taramamak için dizin listesinden çıkartıyoruz
    for d in list(dirs):
        if d in [".idea", ".git", "assessment", "nonassessment", "UselessCode", "ZeroPointAssessment"]:
            dirs.remove(d)
    
    print(f"\n[KLASÖR] İçine girildi: {root}")
    
    for file in files:
        # S ile veya s ile başlayan ve .txt ile biten dosyaları tarıyoruz
        if (file.startswith("S") or file.startswith("s")) and file.endswith(".txt"):
            print(f"  ├── [DOSYA] Okunuyor: {file}")
            
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Yeni ismin başına sayaç koyarak (sıra numarası_orijinalad) oluşturuyoruz
                new_file_name = f"{counter}_{file}"

                # İçeriğinde assessment kelimesi geçiyorsa assessment klasörüne, yoksa nonassessment klasörüne
                if "assessment" in content.lower():
                    shutil.copy(file_path, os.path.join(assessment_path, new_file_name))
                    total_assessment += 1
                else:
                    shutil.copy(file_path, os.path.join(nonassessment_path, new_file_name))
                    total_nonassessment += 1
                    
                counter += 1
            except Exception as e:
                print(f"  └── [ERROR] Kopyalanamadı! Bu dosya işlenemedi. ({file_path}) Hata: {e}")
                total_error += 1

print("\n" + "="*50)
print("İşlem Tamamlandı! İşte Sonuçlar:")
print(f" -> Toplam 'Assessment' klasörüne giden dosya: {total_assessment}")
print(f" -> Toplam 'Nonassessment' klasörüne giden dosya: {total_nonassessment}")
print(f" -> Toplam okunamayıp dışarıda kalan (Hatalı) dosya: {total_error}")
print("="*50 + "\n")