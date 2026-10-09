import os

def find_unmatched_files():
    base_dir = "."  # Scriptin çalıştığı dizin
    exclude_dirs = {".idea", "assessment", "nonassessment", "ZeroPointAssessment", "UselessCode"}
    
    assessment_dir = os.path.join(base_dir, "assessment")
    nonassessment_dir = os.path.join(base_dir, "nonassessment")
    
    unmatched_count = 0
    
    for root, dirs, files in os.walk(base_dir):
        # exclude_dirs içindeki klasörleri taramadan çıkar
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Sadece 's' ile başlayan '.txt' dosyalarını kontrol et
            if file.startswith("s") and file.endswith(".txt"):
                file_path = os.path.join(root, file)
                
                # assessment veya nonassessment klasörlerinde aynı isimde dosya var mı kontrol et
                match_in_assessment = os.path.exists(os.path.join(assessment_dir, file))
                match_in_nonassessment = os.path.exists(os.path.join(nonassessment_dir, file))
                
                if not (match_in_assessment or match_in_nonassessment):
                    print(f"Eşleşme bulunamadı: {file_path}")
                    unmatched_count += 1
                    
    print(f"\nToplam eşleşmeyen dosya sayısı: {unmatched_count}")

if __name__ == "__main__":
    find_unmatched_files()
