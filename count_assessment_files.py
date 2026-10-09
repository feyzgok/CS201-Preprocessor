import os

def count_assessment_files_in_repo(repo_path):
    """
    Belirtilen repo içindeki tüm dizinleri recursive (iç içe) olarak gezer.
    Eğer yolun içinde 'assessment' veya 'nonassessment' adlı bir klasör bulunuyorsa, 
    o klasörlerin (ve alt klasörlerinin) içindeki dosya sayılarını hesaplar.
    """
    total_assessment_files = 0
    total_nonassessment_files = 0
    
    for root, dirs, files in os.walk(repo_path):
        # Yolun tüm klasör isimlerini bir listeye ayırıyoruz
        path_parts = root.split(os.sep)
        
        # Önce 'nonassessment' kontrol ediliyor
        if 'nonassessment' in path_parts:
            total_nonassessment_files += len(files)
        # Ardından 'assessment' kontrol ediliyor
        elif 'assessment' in path_parts:
            total_assessment_files += len(files)
            
    return total_assessment_files, total_nonassessment_files

if __name__ == "__main__":
    from config import EXAM_REPO_PATH
    repo_path = EXAM_REPO_PATH
    
    if not os.path.exists(repo_path):
        print(f"Hata: '{repo_path}' dizini bulunamadı.")
    else:
        print(f"'{repo_path}' dizini taranıyor, 'assessment' ve 'nonassessment' klasörlerindeki dosyalar sayılıyor...")
        
        assessment_count, nonassessment_count = count_assessment_files_in_repo(repo_path)
        
        print("-" * 65)
        print(f"Tüm 'assessment' klasörlerinin içindeki toplam dosya sayısı: {assessment_count}")
        print(f"Tüm 'nonassessment' klasörlerinin içindeki toplam dosya sayısı: {nonassessment_count}")
        print("-" * 65)
