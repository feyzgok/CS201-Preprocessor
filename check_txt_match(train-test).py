import os

def check_txt_files(root_dir):
    exclude_dirs = {".idea", "assessment", "nonassessment", "ZeroPointAssessment", "UselessCode"}
    
    # Tüm dizinlerde özyinelemeli (recursive) olarak dolaş
    for current_dir, dirs, files in os.walk(root_dir):
        # Hariç tutulacak klasörleri listeden çıkar (içlerine girilmesini engeller)
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Eğer bulunduğumuz klasörün içinde 'train' veya 'test' varsa işlemi yap
        if 'train' in dirs or 'test' in dirs:
            
            # Bulunduğumuz ana (parent) klasördeki txt dosyalarını bul
            parent_txts = set()
            for f in files:
                if f.endswith('.txt') and 'refCode' not in f:
                    parent_txts.add(f)
                    
            # train ve test klasörlerindeki txt dosyalarını bul
            train_test_txts = set()
            for sub_dir in ['train', 'test']:
                if sub_dir in dirs:
                    sub_dir_path = os.path.join(current_dir, sub_dir)
                    for f in os.listdir(sub_dir_path):
                        if f.endswith('.txt') and os.path.isfile(os.path.join(sub_dir_path, f)):
                            train_test_txts.add(f)
                            
            # Karşılaştırma yap
            missing_in_train_test = parent_txts - train_test_txts
            
            if missing_in_train_test:
                for f in missing_in_train_test:
                    # Kullanıcının istediği formatta path'i yazdır (Örn: accumulate/S...txt)
                    # current_dir içerisinden root_dir kısmını çıkararak daha temiz bir path elde edebiliriz
                    rel_path = os.path.relpath(current_dir, root_dir)
                    if rel_path == ".":
                        print(f"{f}")
                    else:
                        print(f"{os.path.join(rel_path, f)}")

if __name__ == '__main__':
    from config import EXAM_REPO_PATH
    root_directory = EXAM_REPO_PATH
    check_txt_files(root_directory)
