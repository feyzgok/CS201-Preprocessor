import os
import shutil

def delete_train_test_dirs(root_dir):
    """
    Belirtilen dizin içerisinde, exclude_dirs hariç tutularak,
    'train' ve 'test' adındaki KLASÖRLERİ (ve içlerindeki her şeyi) siler.
    """
    exclude_dirs = {".idea", "assessment", "nonassessment", "ZeroPointAssessment", "UselessCode"}
    
    if not os.path.exists(root_dir):
        print(f"Hata: {root_dir} bulunamadı.")
        return

    deleted_count = 0
    print(f"'{root_dir}' dizini taranıyor...\n")

    # os.walk ile dizin ağacında gezinme (topdown=True olmalı ki dirs listesini değiştirebilelim)
    for current_dir, dirs, files in os.walk(root_dir, topdown=True):
        # Hariç tutulacak klasörleri listeden çıkar (içlerine girilmesini engeller)
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # 'train' ve 'test' klasörlerini bul ve sil
        for target in ['train', 'test']:
            if target in dirs:
                target_path = os.path.join(current_dir, target)
                try:
                    # shutil.rmtree ile klasörü ve içindeki her şeyi sil
                    shutil.rmtree(target_path)
                    print(f"Silindi: {target_path}")
                    deleted_count += 1
                    
                    # Klasörü sildiğimiz için os.walk'un bu klasörün içine girmeye çalışmasını engelliyoruz
                    dirs.remove(target)
                except Exception as e:
                    print(f"Hata oluştu ({target_path}): {e}")

    print(f"\nİşlem tamamlandı. Toplam {deleted_count} adet 'train' veya 'test' klasörü silindi.")

if __name__ == "__main__":
    from config import EXAM_REPO_PATH
    root_directory = EXAM_REPO_PATH
    
    # Kullanıcıdan onay alma (Güvenlik için)
    print(f"DİKKAT: '{root_directory}' dizinindeki 'train' ve 'test' KLASÖRLERİ (ve içerikler) silinecek!")
    onay = input("Emin misiniz? (evet/hayır): ")
    
    if onay.lower() == 'evet':
        delete_train_test_dirs(root_directory)
    else:
        print("İşlem iptal edildi.")
