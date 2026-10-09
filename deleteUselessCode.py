import os
import re
import shutil
from config import NONASSESSMENT_PATH, USELESS_CODE_PATH

path = NONASSESSMENT_PATH
target_path = USELESS_CODE_PATH
deleted_count = 0

# Hedef klasörün var olduğundan emin olalım
os.makedirs(target_path, exist_ok=True)

# 1. Sadece if, for, while kelimelerini arayan regex
keyword_pattern = re.compile(r'\b(if|for|while)\b')

# 2. İçi boş if/for/while bloklarını ve ardından gelen anlamsız return ifadelerini yakalayan regex
# Örnek: for (...) { \n } \n return 0;
dummy_pattern = re.compile(r'\b(if|for|while)\s*\([^)]*\)\s*\{\s*\}\s*return\s+(0|1|false|true|null)\s*;')

if not os.path.exists(path):
    print(f"[HATA] Klasör bulunamadı: {path}")
else:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):  # Önceki dosyalarda olduğu gibi .txt varsayıyoruz
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 1. Şart: Dosyada if, for veya while var mı?
                    has_keywords = bool(keyword_pattern.search(content))
                    
                    should_delete = False
                    
                    if not has_keywords:
                        # İçinde hiç if, for veya while yoksa silinecek
                        should_delete = True
                        reason = "if/for/while kullanılmamış"
                    else:
                        # 2. Şart: if, for, while var ama anlamsız (dummy) mı?
                        # Dosyadaki tüm if/for/while'ları bulalım
                        total_keywords = len(keyword_pattern.findall(content))
                        
                        # İçi boş ve dummy return içeren blokları bulalım
                        dummy_blocks = len(dummy_pattern.findall(content))
                        
                        # Eğer dosyadaki tüm if/for/while blokları dummy ise (veya en az 1 dummy varsa ve dosya kısaysa)
                        # "Denklem mantığı": Eğer bulduğumuz dummy blok sayısı, toplam keyword sayısına eşit veya ondan büyükse
                        # (Yani dosyadaki tek döngü/koşul bu anlamsız bloklarsa) sil.
                        if dummy_blocks > 0 and dummy_blocks >= total_keywords:
                            should_delete = True
                            reason = "Sadece içi boş if/for/while ve dummy return var"

                    if should_delete:
                        # Dosyayı silmek yerine hedef klasöre taşıyoruz
                        target_file_path = os.path.join(target_path, file)
                        shutil.move(file_path, target_file_path)
                        print(f"[TAŞINDI] {file} - Sebep: {reason}")
                        deleted_count += 1
                        
                except Exception as e:
                    print(f"[HATA] Dosya işlenirken sorun oluştu ({file}): {e}")

    print("\n" + "="*50)
    print(f"İşlem Tamamlandı! Toplam {deleted_count} adet kullanışsız kod dosyası UselessCode klasörüne taşındı.")
    print("="*50 + "\n")
