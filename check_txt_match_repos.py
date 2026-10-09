import os
import hashlib


# ============================================================
# YAPILANDIRMA
# ============================================================

from config import EXAM_REPO_TEST_PATH, EXAM_REPO_PATH


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def normalize_content(content: str) -> str:
    """CRLF/CR → LF dönüşümü + baş/son boşluk temizliği."""
    return content.replace('\r\n', '\n').replace('\r', '\n').strip()


def get_content_hash(filepath: str):
    """Dosyayı okur, normalize eder ve SHA-256 hash döner. Hata varsa None."""
    for encoding in ('utf-8', 'latin-1'):
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            normalized = normalize_content(content)
            return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"[OKUMA HATASI] {filepath}: {e}")
            return None
    print(f"[ENCODING HATASI] {filepath}")
    return None


def collect_hashes_from_repo(repo_path: str) -> set:
    """
    ExamRepository'yi recursive gezer.
    Yalnızca adı 'train' veya 'test' olan klasörlerin içindeki .txt dosyalarını alır.
    Tüm hash'leri bir set içinde döner.
    """
    hashes = set()
    for root, dirs, files in os.walk(repo_path):
        parts = root.replace('\\', '/').split('/')
        # Bu dizin doğrudan 'train' veya 'test' adlı bir klasör mü?
        if parts[-1] in ('train', 'test'):
            for filename in files:
                if not filename.lower().endswith('.txt'):
                    continue
                filepath = os.path.join(root, filename)
                h = get_content_hash(filepath)
                if h is not None:
                    hashes.add(h)
    return hashes


def find_missing_in_repo(repo_test_path: str, repo_hashes: set):
    """
    ExamRepositoryTest'i recursive gezer, tüm .txt dosyalarını inceler.
    Hash'i repo_hashes içinde BULUNMAYANLARI döner (path listesi).
    """
    missing = []
    for root, dirs, files in os.walk(repo_test_path):
        # .git, .idea gibi gizli/meta klasörleri atla
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if not filename.lower().endswith('.txt'):
                continue
            filepath = os.path.join(root, filename)
            h = get_content_hash(filepath)
            if h is None:
                continue
            if h not in repo_hashes:
                missing.append(filepath)
    return missing


# ============================================================
# ANA PROGRAM
# ============================================================

def main():
    print("=" * 60)
    print("REPO KARŞILAŞTIRMA (İçerik tabanlı)")
    print("=" * 60)
    print(f"KAYNAK (orijinal)  : {EXAM_REPO_TEST_PATH}")
    print(f"HEDEF  (train/test): {EXAM_REPO_PATH}")
    print()

    if not os.path.exists(EXAM_REPO_TEST_PATH):
        print(f"[HATA] Kaynak repo bulunamadı: {EXAM_REPO_TEST_PATH}")
        return
    if not os.path.exists(EXAM_REPO_PATH):
        print(f"[HATA] Hedef repo bulunamadı: {EXAM_REPO_PATH}")
        return

    # 1) ExamRepository'deki train + test dosyalarının hash'lerini topla
    print("ExamRepository → train/ ve test/ klasörleri taranıyor...")
    repo_hashes = collect_hashes_from_repo(EXAM_REPO_PATH)
    print(f"  Bulunan benzersiz içerik sayısı: {len(repo_hashes)}")

    # 2) ExamRepositoryTest'te olup ExamRepository'de olmayan dosyaları bul
    print("\nExamRepositoryTest → tüm .txt dosyaları karşılaştırılıyor...")
    missing_files = find_missing_in_repo(EXAM_REPO_TEST_PATH, repo_hashes)

    # 3) Rapor
    print()
    print("=" * 60)
    print("SONUÇ")
    print("=" * 60)

    if not missing_files:
        print("OK  ExamRepositoryTest'teki tüm dosyaların içeriği")
        print("    ExamRepository train/test klasörlerinde mevcut.")
    else:
        print(f"EKSIK: {len(missing_files)} dosya ExamRepository'de (train/test) BULUNAMADI:\n")
        for fp in sorted(missing_files):
            print(f"  {fp}")

        # Raporu dışa aktar
        report_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'missing_in_repo_report.txt'
        )
        with open(report_path, 'w', encoding='utf-8') as rf:
            rf.write("ExamRepositoryTest'te bulunup ExamRepository'de (train/test) OLMAYAN dosyalar\n")
            rf.write(f"Kaynak : {EXAM_REPO_TEST_PATH}\n")
            rf.write(f"Hedef  : {EXAM_REPO_PATH}\n")
            rf.write(f"Toplam eksik: {len(missing_files)}\n")
            rf.write("=" * 60 + "\n")
            for fp in sorted(missing_files):
                rf.write(fp + "\n")
        print(f"\nRapor kaydedildi: {report_path}")


if __name__ == '__main__':
    main()