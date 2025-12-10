"""Very small error handler utility."""
def handle_error(e: Exception, context: str = ""):
    print(f"ERROR in {context}: {e}")