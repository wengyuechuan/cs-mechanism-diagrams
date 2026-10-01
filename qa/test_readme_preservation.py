"""A gallery rebuild must preserve the hand-written project README."""
import json,subprocess,sys,tempfile,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class ReadmePreservation(unittest.TestCase):
    def test_existing_readme_survives_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'tools').mkdir();(root/'metadata').mkdir()
            shutil.copy2(ROOT/'tools/build_gallery.py',root/'tools/build_gallery.py')
            for name in ['figures','papers','templates']:
                (root/'metadata'/f'{name}.json').write_text('[]',encoding='utf8')
            text='# Custom public README\n\nHand-maintained instructions.\n'
            (root/'README.md').write_text(text,encoding='utf8')
            result=subprocess.run([sys.executable,str(root/'tools/build_gallery.py')],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual((root/'README.md').read_text(encoding='utf8'),text)

if __name__=='__main__':unittest.main()
