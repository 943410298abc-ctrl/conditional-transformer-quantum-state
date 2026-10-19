import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def import_file(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

new_run=import_file('new_run','scripts/new_run.py')
validation=import_file('validate_workspace','scripts/validate_workspace.py')

class TestCollaborationScaffold(unittest.TestCase):
    def test_run_id(self):
        self.assertEqual(new_run.make_run_id('20261019T010000Z','tfim-baseline',3),'20261019T010000Z-tfim-baseline-s3')
        with self.assertRaises(ValueError):new_run.make_run_id('now','Spaces Are Bad',0)
        with self.assertRaises(ValueError):new_run.make_run_id('now','baseline',-1)

    def test_current_files(self):
        errors,_=validation.validate()
        self.assertEqual(errors,[])

    def test_reject_fake_completed_run(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'run-id'/'manifest.json'
            p.parent.mkdir()
            p.write_text('{"run_id":"run-id","status":"completed","seed":0,"issue":1}',encoding='utf-8')
            errors=validation.check_manifest(p)
            self.assertTrue(any('missing fields' in e for e in errors))
            self.assertTrue(any('missing command' in e for e in errors))

if __name__=='__main__':unittest.main()
