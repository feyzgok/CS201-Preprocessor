import os
from config import EXAM_REPO_PATH

base_path = EXAM_REPO_PATH

# Hariç tutulacak klasörlerin listesi
exclude_dirs = {".idea", "assessment", "nonassessment", "ZeroPointAssessment", "UselessCode"}

def create_train_test_folders():
    # Belirtilen dizindeki tüm dosya ve klasörleri listele
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        
        # Eğer bu bir klasörse ve hariç tutulanlardan biri değilse
        if os.path.isdir(item_path) and item not in exclude_dirs:
            # İçerisine eklenecek train ve test yollarını belirle
            train_path = os.path.join(item_path, "train")
            test_path = os.path.join(item_path, "test")
            
            # Klasörleri oluştur (eğer zaten varsa hata vermez)
            os.makedirs(train_path, exist_ok=True)
            os.makedirs(test_path, exist_ok=True)
            
            print(f"[BAŞARILI] '{item}' içerisine 'train' ve 'test' klasörleri oluşturuldu.")
            
            # Not: Eğer klasör değil de içi boş "train.txt" ve "test.txt" DOSYALARI oluşturmak 
            # istiyorsanız aşağıdaki satırları kullanabilirsiniz ve üstteki os.makedirs satırlarını silebilirsiniz:
            # open(os.path.join(item_path, "train.txt"), 'a').close()
            # open(os.path.join(item_path, "test.txt"), 'a').close()

if __name__ == "__main__":
    create_train_test_folders()
    print("\nİşlem tamamlandı!")
