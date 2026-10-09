# =============================================================================
#  config.py  —  Merkezi Path Yapılandırması
#  Bu dosyayı kendi sisteminize göre düzenleyin.
#  Diğer tüm scriptler path'leri buradan okur.
# =============================================================================

import os

# ---------------------------------------------------------------------------
# Ana Repo Path'leri
# ---------------------------------------------------------------------------

# Orijinal sınav dosyalarının bulunduğu kaynak repo
EXAM_REPO_TEST_PATH = '/Users/feyzagok/IdeaProjects/ExamRepositoryTest'

# Train/test verilerinin oluşturulduğu hedef repo
EXAM_REPO_PATH = '/Users/feyzagok/Documents/GitHub/ExamRepository'

# ---------------------------------------------------------------------------
# ExamRepository Alt Klasörleri  (EXAM_REPO_PATH üzerinden türetilir)
# ---------------------------------------------------------------------------

ASSESSMENT_PATH     = os.path.join(EXAM_REPO_PATH, 'assessment')
NONASSESSMENT_PATH  = os.path.join(EXAM_REPO_PATH, 'nonassessment')
TRAIN_PATH          = os.path.join(EXAM_REPO_PATH, 'train')
TEST_PATH           = os.path.join(EXAM_REPO_PATH, 'test')
USELESS_CODE_PATH   = os.path.join(EXAM_REPO_PATH, 'UselessCode')
ZERO_POINTS_PATH    = os.path.join(EXAM_REPO_PATH, 'ZeroPointsAssessmentt')

# ---------------------------------------------------------------------------
# Dogrulama  —  Script basinda calisir, hatali path'leri hemen bildirir
# ---------------------------------------------------------------------------

def validate_paths(paths: dict, exit_on_error: bool = False) -> None:
    """
    Verilen path sozlugundeki yollari kontrol eder.
    exit_on_error=True ise eksik path bulununca program sonlanir.
    """
    all_ok = True
    for name, p in paths.items():
        if not os.path.exists(p):
            print(f"[UYARI] Path bulunamadi -> {name}: {p}")
            all_ok = False
    if not all_ok and exit_on_error:
        raise SystemExit("[HATA] Gerekli path'ler eksik, config.py dosyasini kontrol edin.")


# Scriptten dogrudan calistirilirsa tum path'leri listeler
if __name__ == '__main__':
    all_paths = {
        'EXAM_REPO_TEST_PATH': EXAM_REPO_TEST_PATH,
        'EXAM_REPO_PATH'     : EXAM_REPO_PATH,
        'ASSESSMENT_PATH'    : ASSESSMENT_PATH,
        'NONASSESSMENT_PATH' : NONASSESSMENT_PATH,
        'TRAIN_PATH'         : TRAIN_PATH,
        'TEST_PATH'          : TEST_PATH,
        'USELESS_CODE_PATH'  : USELESS_CODE_PATH,
        'ZERO_POINTS_PATH'   : ZERO_POINTS_PATH,
    }
    print("=" * 60)
    print("  config.py  -  Mevcut Path Yapilandirmasi")
    print("=" * 60)
    for name, p in all_paths.items():
        status = "OK" if os.path.exists(p) else "!!"
        print(f"  [{status}]  {name:<22} = {p}")
    print("=" * 60)
