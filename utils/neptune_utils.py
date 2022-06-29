import os
try: import neptune.new as neptune
except:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "neptune-client"])
    import neptune.new as neptune


def plugin_neptune(NEPTUNE_API_KEY, NEPTUNE_PROJECT):
    os.environ["NEPTUNE_API_TOKEN"] = NEPTUNE_API_KEY

    run = neptune.init(project=NEPTUNE_PROJECT,
                       api_token=NEPTUNE_API_KEY,
                       mode="sync",
                       )

    run["sys/name"] = "bus_stop_analysis"

    return run
