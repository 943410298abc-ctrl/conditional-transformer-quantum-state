"""Inventory archive bytes without extracting or executing untrusted historical code."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = []
    for path in sorted((ROOT / 'experiments').glob('*.zip')):
        entries = []
        with zipfile.ZipFile(path) as archive:
            for item in archive.infolist():
                data = archive.read(item.filename)
                entries.append(dict(name=item.filename, bytes=len(data),
                                    sha256=hashlib.sha256(data).hexdigest()))
        output.append(dict(path=path.relative_to(ROOT).as_posix(),
                           sha256=hashlib.sha256(path.read_bytes()).hexdigest(), entries=entries))
    dest = ROOT / 'docs' / 'audit' / 'archive_inventory.json'
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Inventoried {len(output)} immutable archives')


if __name__ == '__main__':
    main()
