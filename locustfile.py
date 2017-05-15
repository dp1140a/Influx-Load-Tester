from locust import HttpLocust, TaskSet, task

import resource
import os
from DataGenerator import *

resource.setrlimit(resource.RLIMIT_NOFILE, (3000, 3000))
configFile = "conf/config.json"
# Get config file and setup
if os.environ.get("DG_CONFIG"):
    DG = DataGenerator(os.environ.get("DG_CONFIG"))
else:
    print("No path to custom config file specified in ENV Variable: DG_CONFIG.  Looking for conf/config.json")
    if os.path.isfile(configFile):
        DG = DataGenerator(configFile)
    else:
        print("Cannot find conf/config.json. Need a config. Exiting")
        sys.exit(-1)

DG.setupMeasurements()
DG.setupTagKeys()
DG.setupFieldKeys()

class UserBehavior(TaskSet):
    def on_start(self):
        self.readQuery = {"q": "select last(*) from /.*/ where time > NOW() - 1m group by *",
                          "db": DG.config.get("database")}

    # READ TASKS
    @task(DG.config.get("readWeight"))
    def get_latest_data_for_all_devices(self):
        self.client.get("/query", params=self.readQuery,
                        name="Select last value from all measurements for all devices")

    # WRITE TASKS
    @task(DG.config.get("writeWeight"))
    def write_batch(self):
        batch = "\n".join(DG.getBatch())
        self.client.post("/write", data=batch,
                         params="db=" + DG.config.get("database"),
                         headers={'Content-Type': 'application/octet-stream'},
                         name="Write batch metrics")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = DG.config.get("min_wait")
    max_wait = DG.config.get("max_wait")
