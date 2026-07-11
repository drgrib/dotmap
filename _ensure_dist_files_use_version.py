import email
import pathlib
import sys
import tarfile
import zipfile


def _wheel_version(path: str) -> str:
    with zipfile.ZipFile(path) as zf:
        metadata_name = next(
            name for name in zf.namelist() if name.endswith(".dist-info/METADATA")
        )
        return email.message_from_bytes(zf.read(metadata_name))["Version"]


def _sdist_version(path: str) -> str:
    with tarfile.open(path, "r:gz") as tf:
        pkg_info = next(
            member
            for member in tf.getmembers()
            if pathlib.Path(member.name).name == "PKG-INFO"
        )
        return email.message_from_bytes(tf.extractfile(pkg_info).read())["Version"]


def main() -> int:
    if len(sys.argv) < 3:
        raise SystemExit(
            "usage: python _ensure_dist_files_use_version.py <expected-version> <dist-file>..."
        )

    expected = sys.argv[1]
    files = sys.argv[2:]
    validated = []

    for path in files:
        if path.endswith(".whl"):
            actual = _wheel_version(path)
        elif path.endswith(".tar.gz"):
            actual = _sdist_version(path)
        else:
            raise AssertionError(f"unsupported distribution file: {path}")

        assert actual == expected, f"{path} has version {actual!r} != expected {expected!r}"
        validated.append(f"{path}={actual}")

    print("validated dist versions:", ", ".join(validated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
