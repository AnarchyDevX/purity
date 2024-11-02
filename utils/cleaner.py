import os
import shutil

def delete_pycache_dirs(root_dir='..'):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname == '__pycache__':
                pycache_path = os.path.join(dirpath, dirname)
                try:
                    shutil.rmtree(pycache_path)
                    print(f"Supprimé: {pycache_path}")
                except Exception as e:
                    print(f"Erreur lors de la suppression de {pycache_path}: {e}")
                    
delete_pycache_dirs(root_dir='..')