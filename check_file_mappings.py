import os
import hashlib
from collections import defaultdict
from config import EXAM_REPO_PATH


SEARCH_PATH = EXAM_REPO_PATH


def normalize_content(content):
    """
    Normalizes file content before comparison.

    - Converts CRLF / CR to LF
    - Removes trailing/leading whitespace from the whole file
    """
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    return content.strip()


def get_content_hash(filepath):
    """
    Reads a text file, normalizes its content and returns a SHA-256 hash.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        normalized = normalize_content(content)

        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()

    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()

            normalized = normalize_content(content)

            return hashlib.sha256(
                normalized.encode("utf-8")
            ).hexdigest()

        except Exception as e:
            print(f"Could not read {filepath}: {e}")
            return None

    except Exception as e:
        print(f"Could not read {filepath}: {e}")
        return None


def collect_files_from_named_dirs(target_dir_name, search_path):
    """
    Recursively finds every .txt file located under a directory whose
    name is target_dir_name.

    Returns:
        {
            content_hash: [filepath1, filepath2, ...]
        }
    """
    content_map = defaultdict(list)

    for root, dirs, files in os.walk(search_path):
        path_parts = root.split(os.sep)

        if target_dir_name in path_parts:
            for filename in files:
                if not filename.lower().endswith(".txt"):
                    continue

                filepath = os.path.join(root, filename)
                content_hash = get_content_hash(filepath)

                if content_hash is not None:
                    content_map[content_hash].append(filepath)

    return content_map


def find_missing_by_content(source_dir_name, target_content_map, search_path):
    """
    Finds .txt files under source_dir_name whose CONTENT does not occur
    anywhere in target_content_map.

    Returns:
        [
            filepath1,
            filepath2,
            ...
        ]
    """
    missing = []

    for root, dirs, files in os.walk(search_path):
        path_parts = root.split(os.sep)

        if source_dir_name in path_parts:
            for filename in files:
                if not filename.lower().endswith(".txt"):
                    continue

                filepath = os.path.join(root, filename)
                content_hash = get_content_hash(filepath)

                if content_hash is None:
                    continue

                if content_hash not in target_content_map:
                    missing.append(filepath)

    return missing


def main():
    print("Repository:")
    print(SEARCH_PATH)

    print("\nCollecting TEST file contents...")
    test_content_map = collect_files_from_named_dirs(
        "test",
        SEARCH_PATH
    )

    print("Collecting TRAIN file contents...")
    train_content_map = collect_files_from_named_dirs(
        "train",
        SEARCH_PATH
    )

    print("Collecting NONASSESSMENT file contents...")
    nonassessment_content_map = collect_files_from_named_dirs(
        "nonassessment",
        SEARCH_PATH
    )

    print("Collecting ASSESSMENT file contents...")
    assessment_content_map = collect_files_from_named_dirs(
        "assessment",
        SEARCH_PATH
    )

    print("\nChecking NONASSESSMENT -> TEST...")
    missing_nonassessment = find_missing_by_content(
        "nonassessment",
        test_content_map,
        SEARCH_PATH
    )

    print("Checking ASSESSMENT -> TRAIN...")
    missing_assessment = find_missing_by_content(
        "assessment",
        train_content_map,
        SEARCH_PATH
    )

    print("Checking TEST -> NONASSESSMENT...")
    missing_test = find_missing_by_content(
        "test",
        nonassessment_content_map,
        SEARCH_PATH
    )

    print("Checking TRAIN -> ASSESSMENT...")
    missing_train = find_missing_by_content(
        "train",
        assessment_content_map,
        SEARCH_PATH
    )

    report_file = os.path.join(
        SEARCH_PATH,
        "content_matching_report.txt"
    )

    with open(report_file, "w", encoding="utf-8") as f:

        # -----------------------------
        # nonassessment -> test
        # -----------------------------

        header = "=== NONASSESSMENT files missing from TEST by content ==="
        print(f"\n{header}")
        f.write(header + "\n")

        if not missing_nonassessment:
            msg = (
                "Every nonassessment file has an identical-content "
                "counterpart somewhere under a test directory."
            )
            print(msg)
            f.write(msg + "\n")
        else:
            msg = (
                f"{len(missing_nonassessment)} nonassessment files "
                f"have no identical-content counterpart in test."
            )
            print(msg)
            f.write(msg + "\n\n")

            for filepath in missing_nonassessment:
                print(filepath)
                f.write(filepath + "\n")

        # -----------------------------
        # assessment -> train
        # -----------------------------

        header = "\n=== ASSESSMENT files missing from TRAIN by content ==="
        print(header)
        f.write(header + "\n")

        if not missing_assessment:
            msg = (
                "Every assessment file has an identical-content "
                "counterpart somewhere under a train directory."
            )
            print(msg)
            f.write(msg + "\n")
        else:
            msg = (
                f"{len(missing_assessment)} assessment files "
                f"have no identical-content counterpart in train."
            )
            print(msg)
            f.write(msg + "\n\n")

            for filepath in missing_assessment:
                print(filepath)
                f.write(filepath + "\n")

        # -----------------------------
        # test -> nonassessment
        # -----------------------------

        header = "\n=== TEST files missing from NONASSESSMENT by content ==="
        print(header)
        f.write(header + "\n")

        if not missing_test:
            msg = (
                "Every test file has an identical-content "
                "counterpart somewhere under a nonassessment directory."
            )
            print(msg)
            f.write(msg + "\n")
        else:
            msg = (
                f"{len(missing_test)} test files "
                f"have no identical-content counterpart in nonassessment."
            )
            print(msg)
            f.write(msg + "\n\n")

            for filepath in missing_test:
                print(filepath)
                f.write(filepath + "\n")

        # -----------------------------
        # train -> assessment
        # -----------------------------

        header = "\n=== TRAIN files missing from ASSESSMENT by content ==="
        print(header)
        f.write(header + "\n")

        if not missing_train:
            msg = (
                "Every train file has an identical-content "
                "counterpart somewhere under an assessment directory."
            )
            print(msg)
            f.write(msg + "\n")
        else:
            msg = (
                f"{len(missing_train)} train files "
                f"have no identical-content counterpart in assessment."
            )
            print(msg)
            f.write(msg + "\n\n")

            for filepath in missing_train:
                print(filepath)
                f.write(filepath + "\n")

    print(f"\nDetailed report saved to:\n{report_file}")


if __name__ == "__main__":
    main()