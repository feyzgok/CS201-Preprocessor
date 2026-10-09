import os
import shutil

def get_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

def find_nonassessment_files(nonassessment_dir):
    # nonassessment klasöründeki tüm dosyaların içeriklerini ve yollarını bir listede tutalım
    nonassessment_files = []
    for root, dirs, files in os.walk(nonassessment_dir):
        for file in files:
            filepath = os.path.join(root, file)
            content = get_file_content(filepath)
            if content is not None:
                nonassessment_files.append({
                    'path': filepath,
                    'name': file,
                    'content': content
                })
    return nonassessment_files

def process_tests(root_dir, nonassessment_dir):
    nonassessment_files = find_nonassessment_files(nonassessment_dir)
    if not nonassessment_files:
        print(f"{nonassessment_dir} içerisinde dosya bulunamadı veya okunamadı.")
        return

    exclude_dirs = {".idea", "assessment", "nonassessment", "ZeroPointAssessment", "UselessCode"}
    
    # Tüm klasörleri gez
    for root, dirs, files in os.walk(root_dir):
        # İstenmeyen klasörleri (exclude_dirs) arama dışı bırak
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # 1. Eğer bu klasörün içinde 'test' adında bir alt klasör varsa işlem yap
        has_test_folder = any(d.lower() == 'test' for d in dirs)
        
        if has_test_folder:
            # Test klasörünün tam yolunu belirle
            test_folder_path = None
            for d in dirs:
                if d.lower() == 'test':
                    test_folder_path = os.path.join(root, d)
                    break
                    
            # 2. Bu klasördeki (root) S ile başlayan txt dosyalarını bul
            s_files = [f for f in files if (f.startswith('S') or f.startswith('s')) and f.endswith('.txt')]
            
            for s_file in s_files:
                file_path = os.path.join(root, s_file)
                content = get_file_content(file_path)
                
                if content is not None:
                    # 3. S ile başlayan dosyaların içeriği nonassessment'taki dosyalar ile kıyaslanacak
                    for non_ass_file in nonassessment_files:
                        if content == non_ass_file['content']:
                            print(f"Eşleşme bulundu: {file_path} içeriği ile {non_ass_file['path']} aynı.")
                            
                            dest_path = os.path.join(test_folder_path, non_ass_file['name'])
                            
                            # 4. İçeriği aynı olan dosyalar kendi adlarıyla test klasörü içerisine kopyalanacak ve S dosyası silinecek
                            try:
                                if os.path.exists(non_ass_file['path']):
                                    shutil.copy(non_ass_file['path'], dest_path)
                                    print(f"-> Dosya kopyalandı: {non_ass_file['path']} -> {dest_path}")
                                else:
                                    with open(dest_path, 'w', encoding='utf-8') as f:
                                        f.write(non_ass_file['content'])
                                    print(f"-> Dosya kopyası oluşturuldu: {dest_path}")
                                
                                # Eşleşen S ile başlayan dosyayı bulunduğu dizinden kaldır
                                if os.path.exists(file_path):
                                    os.remove(file_path)
                                    print(f"-> S ile başlayan dosya silindi: {file_path}")
                                    
                            except Exception as e:
                                print(f"İşlem hatası: {e}")

if __name__ == "__main__":
    from config import EXAM_REPO_PATH, NONASSESSMENT_PATH
    ROOT_DIR = EXAM_REPO_PATH
    NONASSESSMENT_DIR = NONASSESSMENT_PATH
    
    if os.path.exists(NONASSESSMENT_DIR):
        process_tests(ROOT_DIR, NONASSESSMENT_DIR)
    else:
        print(f"nonassessment klasörü bulunamadı: {NONASSESSMENT_DIR}. Lütfen yolun doğru olduğundan emin olun.")
