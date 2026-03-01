from pathlib import Path
import shutil
from datetime import datetime
from rich.console import Console

console = Console()

ROOT = Path(__file__).resolve().parents[2]
RULES_DIR = ROOT / "rules"

SOURCES = RULES_DIR / "sources"
ENABLED = RULES_DIR / "enabled"
DISABLED = RULES_DIR / "disabled"
GENERATED = RULES_DIR / "generated"
BACKUPS = RULES_DIR / "backups"

for d in [SOURCES, ENABLED, DISABLED, GENERATED, BACKUPS]:
    d.mkdir(parents=True, exist_ok=True)


# ---------------- Core Ops ---------------- #

def list_rules():
    console.print("\n[bold green]Enabled rules:[/bold green]")
    for f in ENABLED.glob("*.rules"):
        console.print(f"  ✔ {f.name}")

    console.print("\n[bold yellow]Disabled rules:[/bold yellow]")
    for f in DISABLED.glob("*.rules"):
        console.print(f"  ✖ {f.name}")

    console.print("\n[bold cyan]Source rules:[/bold cyan]")
    for f in SOURCES.glob("*.rules"):
        console.print(f"  📄 {f.name}")


def enable_rule(name: str, dry_run=False):
    src = SOURCES / name
    dst = ENABLED / name

    if not src.exists():
        console.print(f"[red]Rule not found: {name}[/red]")
        return

    if dry_run:
        console.print(f"[yellow][DRY-RUN] enable {name}[/yellow]")
        return

    shutil.copy2(src, dst)
    console.print(f"[green]Enabled rule: {name}[/green]")


def disable_rule(name: str, dry_run=False):
    src = ENABLED / name
    dst = DISABLED / name

    if not src.exists():
        console.print(f"[red]Rule not enabled: {name}[/red]")
        return

    if dry_run:
        console.print(f"[yellow][DRY-RUN] disable {name}[/yellow]")
        return

    shutil.move(src, dst)
    console.print(f"[yellow]Disabled rule: {name}[/yellow]")


def build_ruleset(dry_run=False):
    target = GENERATED / "snort.rules"
    rules = []

    for rule_file in ENABLED.glob("*.rules"):
        rules.append(rule_file.read_text())

    if dry_run:
        console.print(
            f"[yellow][DRY-RUN] build ruleset with {len(rules)} files[/yellow]"
        )
        return

    target.write_text("\n".join(rules))
    console.print(f"[green]Generated ruleset → {target}[/green]")


def backup_rules():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = BACKUPS / f"rules_{ts}"

    shutil.make_archive(str(archive), "gztar", RULES_DIR)
    console.print(f"[blue]Rules backed up → {archive}.tar.gz[/blue]")