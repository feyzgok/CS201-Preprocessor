import os
from config import EXAM_REPO_PATH, ASSESSMENT_PATH, NONASSESSMENT_PATH

path = EXAM_REPO_PATH
assessment_path = ASSESSMENT_PATH
nonassessment_path = NONASSESSMENT_PATH

def count_txt_files(directory):
    count = 0
    # Eğer klasör varsa içindeki tüm txt dosyalarını say
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".txt"):
                    count += 1
    return count

def count_other_txt_files(base_dir):
    count = 0
    if os.path.exists(base_dir):
        for root, dirs, files in os.walk(base_dir):
            # .idea ve hedef klasörleri taramanın dışında tutuyoruz
            if ".idea" in dirs:
                dirs.remove(".idea")
            if "assessment" in dirs:
                dirs.remove("assessment")
            if "nonassessment" in dirs:
                dirs.remove("nonassessment")

            for file in files:
                if file.endswith(".txt"):
                    count += 1
    return count

assessment_count = count_txt_files(assessment_path)
nonassessment_count = count_txt_files(nonassessment_path)
other_count = count_other_txt_files(path)

print(f"Assessment klasöründeki .txt dosyası sayısı: {assessment_count}")
print(f"Nonassessment klasöründeki .txt dosyası sayısı: {nonassessment_count}")
print(f"Ana dizindeki (assessment, nonassessment ve .idea hariç) toplam .txt dosyası sayısı: {other_count}")
