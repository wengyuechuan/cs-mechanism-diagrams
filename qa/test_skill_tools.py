import unittest,importlib.util,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'agent-skill/cs-mechanism-imagegen'

class SkillContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=SKILL/'scripts/library.py'
        spec=importlib.util.spec_from_file_location('mechanism_library',path)
        cls.lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.lib)
        cls.brief=json.loads((SKILL/'assets/briefs/graph-rag.json').read_text(encoding='utf8'))

    def test_reject_unknown_endpoint(self):
        b=copy.deepcopy(self.brief);b['edges'][0]['target']='DOES_NOT_EXIST'
        with self.assertRaises(ValueError):self.lib.validate_brief(b)

    def test_reject_forbidden_writeback(self):
        b=copy.deepcopy(self.brief);b['edges'].append({'source':'A','target':'G','kind':'write'})
        with self.assertRaises(ValueError):self.lib.validate_brief(b)

    def test_reject_missing_group_member(self):
        b=copy.deepcopy(self.brief);b['groups'][0]['members'].append('UNKNOWN')
        with self.assertRaises(ValueError):self.lib.validate_brief(b)

    def test_reject_duplicate_node_and_edge(self):
        for field in ['nodes','edges']:
            b=copy.deepcopy(self.brief);b[field].append(copy.deepcopy(b[field][0]))
            with self.assertRaises(ValueError):self.lib.validate_brief(b)

    def test_valid_dag_keeps_exact_topology(self):
        b=self.lib.validate_brief(copy.deepcopy(self.brief))
        self.assertEqual(len(b['nodes']),9);self.assertEqual(len(b['edges']),8)
        self.assertEqual(b['non_edges'],self.brief['non_edges'])

    def test_strict_filter_does_not_fallback(self):
        cat=self.lib.read('catalog.json')
        results=self.lib.search(cat,'retrieval','L08','V01','',10,None)
        self.assertTrue(results)
        self.assertTrue(all(x['topic']=='05' and x['layout_style']=='L08' and x['visual_style']=='V01' for x in results))
        self.assertEqual(self.lib.search(cat,'retrieval','L08','V06','',10,None),[])

    def test_prompt_preserves_all_edges_and_reference_roles(self):
        cat=self.lib.read('catalog.json');refs=[x for x in cat if x['id'] in ['T17','T18']]
        prompt=self.lib.make_prompt(self.brief,refs,'L08','V01')
        for edge in self.brief['edges']:self.assertIn(edge['source']+' -> '+edge['target'],prompt)
        self.assertIn('EXACTLY 9 system nodes and 8 directed system arrows',prompt)
        self.assertIn('style/layout reference',prompt)
        self.assertIn('Forbidden system edges',prompt)

if __name__=='__main__':unittest.main()
