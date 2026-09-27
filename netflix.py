from pathlib import Path
import runpy


dashboard_path = Path(__file__).with_name("app.py")
runpy.run_path(str(dashboard_path), run_name="__main__")
