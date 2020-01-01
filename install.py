import sys
import shutil
import ply, ply.lex, ply.yacc
from pathlib import Path

TARGET = "ply"

def main(argv):
    user = False
    if len(argv) > 1:
        if argv[1] != '--user':
            raise SystemExit('usage: python install.py [--user]')
        else:
            user = True
    site_packages = [p for p in sys.path if p.endswith('site-packages')]
    path = Path(site_packages[0] if user else site_packages[-1]) / TARGET
    if path.exists():
        shutil.rmtree(path)
    shutil.copytree(TARGET, path)
    print(f'{TARGET} installed at {path}')

if __name__ == '__main__':
    main(sys.argv)


    
    
    
