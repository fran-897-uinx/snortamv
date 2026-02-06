from version import main as version_main
import sys

if "--version" in sys.argv:
    version_main()
    sys.exit(0)
