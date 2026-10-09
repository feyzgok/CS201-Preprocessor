import os
import glob
from collections import defaultdict

repo_test_path = '/Users/feyzagok/IdeaProjects/ExamRepositoryTest'
repo_path = '/Users/feyzagok/Documents/GitHub/ExamRepository'

mismatched_folders = [
    "divideQueue",
    "dequeue-array",
    "dequeue-list",
    "queue",
    "ascendants-maxHeap",
    "cutPaste"
]


def get_original_name(repo_filename):
    """
    Example:
        1539_S028401.txt -> S028401.txt
        42_S123456.txt   -> S123456.txt
    """

    filename = os.path.basename(repo_filename)

    if "_" not in filename:
        return None

    return filename.split("_", 1)[1]


for folder in mismatched_folders:

    print("\n" + "=" * 100)
    print(f"FOLDER: {folder}")
    print("=" * 100)

    # ============================================================
    # ExamRepositoryTest
    # Orijinal dosyalar: S*.txt
    # ============================================================

    original_folder = os.path.join(repo_test_path, folder)

    original_files = glob.glob(
        os.path.join(original_folder, 'S*.txt')
    )

    original_names = {
        os.path.basename(path)
        for path in original_files
    }


    # ============================================================
    # ExamRepository
    # train + test içerisindeki tüm txt dosyaları
    # ============================================================

    repo_folder = os.path.join(repo_path, folder)

    train_files = glob.glob(
        os.path.join(repo_folder, 'train', '*.txt')
    )

    test_files = glob.glob(
        os.path.join(repo_folder, 'test', '*.txt')
    )

    repo_files = train_files + test_files


    # ============================================================
    # original name -> ExamRepository paths
    #
    # Örnek:
    #
    # S028401.txt ->
    #   queue/train/1539_S028401.txt
    #   queue/test/991_S028401.txt
    # ============================================================

    repo_by_original_name = defaultdict(list)

    invalid_repo_files = []

    for repo_file in repo_files:

        original_name = get_original_name(repo_file)

        if original_name is None:
            invalid_repo_files.append(repo_file)
            continue

        repo_by_original_name[original_name].append(repo_file)


    # ============================================================
    # COUNTS
    # ============================================================

    print(f"ExamRepositoryTest originals : {len(original_names)}")
    print(f"ExamRepository train         : {len(train_files)}")
    print(f"ExamRepository test          : {len(test_files)}")
    print(f"ExamRepository total         : {len(repo_files)}")


    # ============================================================
    # DUPLICATES
    # Aynı Sxxxxx.txt birden fazla ExamRepository dosyasına dönüşmüş
    # ============================================================

    print("\nDUPLICATES")
    print("-" * 100)

    duplicate_count = 0
    extra_copy_count = 0

    for original_name, locations in sorted(repo_by_original_name.items()):

        if len(locations) > 1:

            duplicate_count += 1
            extra_copy_count += len(locations) - 1

            print(f"\n{original_name}")
            print(f"Found {len(locations)} times:")

            for path in locations:
                print(
                    "  ->",
                    os.path.relpath(path, repo_path)
                )

            print(f"Extra copies: {len(locations) - 1}")

    if duplicate_count == 0:
        print("None.")


    # ============================================================
    # MISSING
    # ExamRepositoryTest'te var ama ExamRepository'de yok
    # ============================================================

    print("\nMISSING FROM EXAMREPOSITORY")
    print("-" * 100)

    repo_original_names = set(repo_by_original_name.keys())

    missing_names = sorted(
        original_names - repo_original_names
    )

    if not missing_names:
        print("None.")
    else:
        for name in missing_names:
            print(name)


    # ============================================================
    # EXTRA / UNKNOWN
    # ExamRepository'de var ama ExamRepositoryTest'te karşılığı yok
    # ============================================================

    print("\nNO MATCH IN EXAMREPOSITORYTEST")
    print("-" * 100)

    extra_names = sorted(
        repo_original_names - original_names
    )

    if not extra_names:
        print("None.")
    else:

        for name in extra_names:

            print(f"\n{name}")

            for path in repo_by_original_name[name]:
                print(
                    "  ->",
                    os.path.relpath(path, repo_path)
                )


    # ============================================================
    # INVALID FILENAMES
    # "_" formatına uymayanlar
    # ============================================================

    print("\nINVALID EXAMREPOSITORY FILENAMES")
    print("-" * 100)

    if not invalid_repo_files:
        print("None.")
    else:
        for path in invalid_repo_files:
            print(
                os.path.relpath(path, repo_path)
            )


    # ============================================================
    # FOLDER SUMMARY
    # ============================================================

    print("\nSUMMARY")
    print("-" * 100)

    print(f"Original unique names : {len(original_names)}")
    print(f"Repo unique S names   : {len(repo_original_names)}")
    print(f"Duplicate S names     : {duplicate_count}")
    print(f"Total extra copies    : {extra_copy_count}")
    print(f"Missing originals     : {len(missing_names)}")
    print(f"Unknown repo names    : {len(extra_names)}")