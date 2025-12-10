from pathlib import Path
def modify_conf(root: Path, changes: dict):
    # Very small demonstration: append a line to snort.conf.template
    tpl = root / "templates" / "snort.conf.tpl"
    if not tpl.exists():
        print("Template not found")
        return
    with open(tpl, "a") as f:
        for k, v in changes.items():
            f.write(f"# {k} -> {v}\n")
    print("Modified template (demo)")