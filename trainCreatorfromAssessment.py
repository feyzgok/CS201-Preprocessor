import os
import shutil

def get_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def find_assessment_files(assessment_dir):
    # assessment klasöründeki tüm dosyaların içeriklerini ve yollarını bir listede tutalım
    assessment_files = []
    for root, dirs, files in os.walk(assessment_dir):
        for file in files:
            filepath = os.path.join(root, file)
            content = get_file_content(filepath)
            if content is not None:
                assessment_files.append({
                    'path': filepath,
                    'name': file,
                    'content': content
                })
    return assessment_files

def process_tests(root_dir, assessment_dir):
    assessment_files = find_assessment_files(assessment_dir)
    if not assessment_files:
        print(f"{assessment_dir} içerisinde dosya bulunamadı veya okunamadı.")
        return

    exclude_dirs = {".idea", "assessment", "nonassessment", "ZeroPointAssessment", "UselessCode"}
    
    # Tüm klasörleri gez
    for root, dirs, files in os.walk(root_dir):
        # İstenmeyen klasörleri (exclude_dirs) arama dışı bırak
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # 1. Eğer bu klasörün içinde 'train' adında bir alt klasör varsa işlem yap
        has_train_folder = any(d.lower() == 'train' for d in dirs)
        
        if has_train_folder:
            # Train klasörünün tam yolunu belirle
            train_folder_path = None
            for d in dirs:
                if d.lower() == 'train':
                    train_folder_path = os.path.join(root, d)
                    break
                    
            # 2. Bu klasördeki (root) S ile başlayan txt dosyalarını bul
            s_files = [f for f in files if (f.startswith('S') or f.startswith('s')) and f.endswith('.txt')]
            
            for s_file in s_files:
                file_path = os.path.join(root, s_file)
                content = get_file_content(file_path)
                
                if content is not None:
                    # 3. S ile başlayan dosyaların içeriği assessment'taki dosyalar ile kıyaslanacak
                    for ass_file in assessment_files:
                        if content == ass_file['content']:
                            print(f"Eşleşme bulundu: {file_path} içeriği ile {ass_file['path']} aynı.")
                            
                            dest_path = os.path.join(train_folder_path, ass_file['name'])
                            
                            # 4. İçeriği aynı olan dosyalar kendi adlarıyla train klasörü içerisine kopyalanacak ve S dosyası silinecek
                            try:
                                if os.path.exists(ass_file['path']):
                                    shutil.copy(ass_file['path'], dest_path)
                                    print(f"-> Dosya kopyalandı: {ass_file['path']} -> {dest_path}")
                                else:
                                    with open(dest_path, 'w', encoding='utf-8') as f:
                                        f.write(ass_file['content'])
                                    print(f"-> Dosya kopyası oluşturuldu: {dest_path}")
                                
                                # Eşleşen S ile başlayan dosyayı bulunduğu dizinden kaldır
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                    print(f"-> S ile başlayan dosya silindi: {file_path}")
                                    
                            except Exception as e:
                                print(f"İşlem hatası: {e}")

if __name__ == "__main__":
    from config import EXAM_REPO_PATH, ASSESSMENT_PATH
    ROOT_DIR = EXAM_REPO_PATH
    ASSESSMENT_DIR = ASSESSMENT_PATH
    
    if os.path.exists(ASSESSMENT_DIR):
        process_tests(ROOT_DIR, ASSESSMENT_DIR)
    else:
        print(f"assessment klasörü bulunamadı: {ASSESSMENT_DIR}. Lütfen yolun doğru olduğundan emin olun.")
