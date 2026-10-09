import os

def count_train_test_files_in_repo(repo_path):
    """
    Belirtilen repo içindeki tüm dizinleri recursive (iç içe) olarak gezer.
    Eğer yolun içinde 'train' veya 'test' adlı bir klasör bulunuyorsa, 
    o klasörlerin (ve alt klasörlerinin) içindeki dosya sayılarını hesaplar.
    """
    total_train_files = 0
    total_test_files = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Yolun tüm klasör isimlerini bir listeye ayırıyoruz
        path_parts = root.split(os.sep)
        
        # Yol 'train' klasörünü içeriyorsa
        if 'train' in path_parts:
            total_train_files += len(files)
        # Yol 'test' klasörünü içeriyorsa
        elif 'test' in path_parts:
            total_test_files += len(files)
            
    return total_train_files, total_test_files

if __name__ == "__main__":
    from config import EXAM_REPO_PATH
    repo_path = EXAM_REPO_PATH
    
    if not os.path.exists(repo_path):
        print(f"Hata: '{repo_path}' dizini bulunamadı.")
    else:
        print(f"'{repo_path}' dizini taranıyor, 'train' ve 'test' klasörlerindeki dosyalar sayılıyor...")
        
        train_count, test_count = count_train_test_files_in_repo(repo_path)
        
        print("-" * 50)
        print(f"Tüm 'train' klasörlerinin (ve alt dizinlerinin) içindeki toplam dosya sayısı: {train_count}")
        print(f"Tüm 'test' klasörlerinin (ve alt dizinlerinin) içindeki toplam dosya sayısı: {test_count}")
        print("-" * 50)
