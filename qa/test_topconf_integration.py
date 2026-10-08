"""Contracts for provenance-aware upstream import and portable JPEG references."""
import unittest,importlib.util,struct,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class UpstreamImportContracts(unittest.TestCase):
    def test_teaser_keeps_unknown_visual_and_pending_review(self):
        imp=module(ROOT/'tools/import_topconf.py','topconf_import')
        row={'id':'neurips2024-1022','title':'HippoRAG: Long-Term Memory','venue':'neurips','year':2024,'pattern':'teaser','authors':['A'], 'paper':'https://example.org/paper','pdf_source':'https://example.org/paper.pdf'}
        result=imp.normalize(row,'abc123')
        self.assertEqual(result['kind'],'upstream_reference')
        self.assertEqual(result['layout_style'],'L00');self.assertEqual(result['visual_style'],'V00')
        self.assertEqual(result['upstream_commit'],'abc123');self.assertEqual(result['authors'],['A'])
        self.assertEqual(result['style_review_status'],'pending')

    def test_source_path_cannot_escape_checkout(self):
        imp=module(ROOT/'tools/import_topconf.py','topconf_import_paths')
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):imp.source_image(Path(tmp),'../outside.jpg')

    def test_jpeg_dimensions_without_third_party_dependencies(self):
        lib=module(ROOT/'agent-skill/cs-mechanism-imagegen/scripts/library.py','jpeg_library')
        jpeg=b'\xff\xd8\xff\xc0'+struct.pack('>H',17)+b'\x08'+struct.pack('>HH',80,120)+b'\x03'+b'\x01\x11\x00\x02\x11\x00\x03\x11\x00'+b'\xff\xd9'
        self.assertEqual(lib.image_dimensions(jpeg),(120,80))
        with self.assertRaises(ValueError):lib.image_dimensions(b'\xff\xd8\xff\xc0\x00\x11')

    def test_search_filters_upstream_source_and_pattern(self):
        lib=module(ROOT/'agent-skill/cs-mechanism-imagegen/scripts/library.py','upstream_search')
        base={'id':'TCF_A','title':'HippoRAG','description':'','category':'05_检索','topic':'05','layout_style':'L00','visual_style':'V00','kind':'upstream_reference','year':2024,'source_collection':'topconf','upstream_pattern':'teaser','venue':'NeurIPS','authors':['Alice']}
        rows=[base,{**base,'id':'T17','kind':'original_blueprint','source_collection':'local','upstream_pattern':None}]
        got=lib.search(rows,source='topconf',pattern='teaser',venue='neurips',query='Alice',limit=10)
        self.assertEqual([x['id'] for x in got],['TCF_A'])

    def test_unreviewed_style_is_not_a_generation_preset(self):
        lib=module(ROOT/'agent-skill/cs-mechanism-imagegen/scripts/library.py','unreviewed_prompt')
        brief={'nodes':[{'id':'A','label':'Input'}],'edges':[]}
        with self.assertRaises(ValueError):lib.make_prompt(brief,[],'L00','V00')

if __name__=='__main__':unittest.main()
