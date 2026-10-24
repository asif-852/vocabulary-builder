import importlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append('scripts')

def validate_set(module_name, set_dict_name):
    mod = importlib.import_module(module_name)
    data = getattr(mod, set_dict_name)
    print(f"Validating {module_name}.{set_dict_name} ({len(data)} items)...")
    assert len(data) == 20, f"Expected 20 items, got {len(data)}"
    
    for k, v in data.items():
        opts = v['options']
        assert len(opts) == 6, f"Item {k} options len != 6"
        true_syns = [o for o in opts if o['isSynonym']]
        dists = [o for o in opts if not o['isSynonym']]
        assert len(true_syns) == 3, f"Item {k} true synonyms != 3 (got {len(true_syns)})"
        assert len(dists) == 3, f"Item {k} distractors != 3 (got {len(dists)})"
        
        for o in opts:
            assert o['word'][0].isupper(), f"Item {k} option not title-cased: {o['word']}"
            assert len(o['meaningBn']) >= 2, f"Item {k} meaning too short: {o['meaningBn']}"
            assert not re.search(r'[a-zA-Z]', o['meaningBn']), f"Item {k} English in meaning: {o['meaningBn']}"
            
    print(f"SUCCESS: {module_name} validated perfectly!")

if __name__ == '__main__':
    module = sys.argv[1]
    dict_name = sys.argv[2]
    validate_set(module, dict_name)
