class ProcessLifecycleTracker:

    def __init__(self):

        self.previous_processes = set()

    def update(self, observations):

        current_processes = {
            observation.entity_id
            for observation in observations
            if observation.entity_type == "process"
        }

        started = current_processes - self.previous_processes

        exited = self.previous_processes - current_processes

        running = current_processes & self.previous_processes

        self.previous_processes = current_processes

        return {
            "started": started,
            "running": running,
            "exited": exited,
        }



    
# Yes. This is the exact piece that answers your question. The important idea is:

#  > **The tracker does not mark an entity as "started" because the ID itself says so. It compares the set of process IDs from the previous scan with the set from the current scan.**

#  Let's go through it step by step.

#  ## 1\. Initial state

#  When you create the tracker:

# ```
# def __init__(self):
#     self.previous_processes = set()
# ```

#  You start with:

# ```
# self.previous_processes = set()
# ```

#  An empty set means:

#  > "I haven't seen any processes before."

# ---

#  ## 2\. `update()` receives observations

#  Your orchestrator does:

# ```
# lifecycle = self.lifecycle_tracker.update(
#     process_observations
# )
# ```

#  Suppose `process_observations` contains these observations:

# ```
# Observation 1
# entity_type = "process"
# entity_id   = "pid:100@abc"

# Observation 2
# entity_type = "process"
# entity_id   = "pid:200@def"

# Observation 3
# entity_type = "process"
# entity_id   = "pid:300@ghi"
# ```

# ---

#  ## 3\. It extracts the entity IDs

#  This code:

# ```
# current_processes = {
#     observation.entity_id
#     for observation in observations
#     if observation.entity_type == "process"
# }
# ```

#  is basically saying:

#  > "Give me the `entity_id` of every observation whose type is `process`."

#  So:

# ```
# observations
# ```

#  might be:

# ```
# [
#     Observation(
#         entity_type="process",
#         entity_id="pid:100@abc"
#     ),
#     Observation(
#         entity_type="process",
#         entity_id="pid:200@def"
#     ),
#     Observation(
#         entity_type="process",
#         entity_id="pid:300@ghi"
#     )
# ]
# ```

#  Then this:

# ```
# current_processes = {
#     observation.entity_id
#     for observation in observations
#     if observation.entity_type == "process"
# }
# ```

#  produces:

# ```
# current_processes = {
#     "pid:100@abc",
#     "pid:200@def",
#     "pid:300@ghi"
# }
# ```

#  So **this is where the `entity_id` enters the lifecycle calculation.**

# ---

#  # 4\. The first scan

#  Remember:

# ```
# self.previous_processes = set()
# ```

#  So initially:

# ```
# previous_processes
#     ↓
# {}

# current_processes
#     ↓
# {
#     100,
#     200,
#     300
# }
# ```

#  Now:

# ```
# started = current_processes - self.previous_processes
# ```

#  means:

#  > Give me things that are in `current_processes` but NOT in `previous_processes`.

#  Therefore:

# ```
# current:
# {100, 200, 300}

# previous:
# {}

# started:
# {100, 200, 300}
# ```

#  So all three are considered **started**.

#  Your result becomes:

# ```
# {
#     "started": {
#         "pid:100@abc",
#         "pid:200@def",
#         "pid:300@ghi"
#     },

#     "running": set(),

#     "exited": set()
# }
# ```

# ---

#  # 5\. Then this line is VERY important

#  At the end of `update()`:

# ```
# self.previous_processes = current_processes
# ```

#  Now the tracker remembers:

# ```
# previous_processes =
# {
#     100,
#     200,
#     300
# }
# ```

#  It's basically taking a snapshot:

#  > "These are the processes I saw this time. I'll compare the next scan against these."

# ---

#  # 6\. Second scan

#  Imagine the next time your collector runs, it sees:

# ```
# 100
# 200
# 300
# 400
# ```

#  So:

# ```
# current_processes = {
#     100,
#     200,
#     300,
#     400
# }
# ```

#  Previous was:

# ```
# previous_processes = {
#     100,
#     200,
#     300
# }
# ```

#  Now:

# ```
# started = current_processes - previous_processes
# ```

#  gives:

# ```
# {400}
# ```

#  Why?

#  Because `400` exists now but didn't exist before.

#  So:

# ```
# started = {
#     400
# }
# ```

# ---

#  # 7\. What about `running`?

#  You have:

# ```
# running = current_processes & self.previous_processes
# ```

#  The `&` means **intersection**.

#  In plain English:

#  > Give me processes that exist both now AND before.

#  Current:

# ```
# {100, 200, 300, 400}
# ```

#  Previous:

# ```
# {100, 200, 300}
# ```

#  Intersection:

# ```
# {100, 200, 300}
# ```

#  Therefore:

# ```
# running = {
#     100,
#     200,
#     300
# }
# ```

#  Those processes existed in both snapshots, so they're considered **running**.

# ---

#  # 8\. What about `exited`?

#  Now imagine the third scan.

#  Current processes are:

# ```
# {100, 200, 400}
# ```

#  Previous processes were:

# ```
# {100, 200, 300, 400}
# ```

#  Process `300` disappeared.

#  Your code:

# ```
# exited = self.previous_processes - current_processes
# ```

#  means:

#  > Give me processes that existed before but don't exist now.

#  Therefore:

# ```
# previous:
# {100, 200, 300, 400}

# current:
# {100, 200, 400}

# exited:
# {300}
# ```

#  So `300` becomes an exited process.

# ---

#  # 9\. The whole thing visually

#  Imagine your operating system has processes:

#  ### Scan #1

# ```
# Current:
# A B C

# Previous:
# (empty)

# Started:
# A B C

# Running:
# (empty)

# Exited:
# (empty)
# ```

#  Then tracker saves:

# ```
# Previous = A B C
# ```

#  ### Scan #2

# ```
# Current:
# A B C D

# Previous:
# A B C

# Started:
# D

# Running:
# A B C

# Exited:
# (empty)
# ```

#  Then tracker saves:

# ```
# Previous = A B C D
# ```

#  ### Scan #3

# ```
# Current:
# A B D

# Previous:
# A B C D

# Started:
# (empty)

# Running:
# A B D

# Exited:
# C
# ```

#  Then tracker saves:

# ```
# Previous = A B D
# ```

# ---

#  # 10\. Now connect this back to your orchestrator

#  This:

# ```
# lifecycle = self.lifecycle_tracker.update(
#     process_observations
# )
# ```

#  might return:

# ```
# {
#     "started": {
#         "pid:1724@1789035754.05"
#     },

#     "running": {
#         "pid:100@...",
#         "pid:200@..."
#     },

#     "exited": {
#         "pid:1500@..."
#     }
# }
# ```

#  Then your orchestrator does:

# ```
# for entity_id in lifecycle["started"]:
# ```

#  So:

# ```
# entity_id = "pid:1724@1789035754.05"
# ```

#  Then it creates:

# ```
# LifecycleEvent(
#     event_type="process_started",
#     entity_type="process",
#     entity_id=entity_id,
#     timestamp=...
# )
# ```

#  Notice the distinction:

# ```
# "started"
#    ↑
#    └── classification/key produced by LifecycleTracker

# "pid:1724@1789035754.05"
#    ↑
#    └── actual entity_id from the Observation

# "process_started"
#    ↑
#    └── event_type YOU create in the Orchestrator
# ```

#  That's the whole chain.

# ```
# Observation
#     │
#     │ entity_id = "pid:1724@..."
#     ↓
# LifecycleTracker
#     │
#     │ compares current vs previous IDs
#     ↓
# "started": {"pid:1724@..."}
#     │
#     ↓
# Orchestrator
#     │
#     │ event_type = "process_started"
#     ↓
# LifecycleEvent
#     │
#     ↓
# SQLite
# ```

#  ### One subtle but important point

#  Your tracker is **not actually observing a process "starting" in the operating-system sense**.

#  It only knows:

#  > "This process ID exists in the current snapshot, but it didn't exist in my previous snapshot."

#  Therefore it **infers** that the process started sometime between the two observations.

#  Likewise, `"exited"` means:

#  > "It existed in the previous snapshot, but it isn't present in the current snapshot."

#  That distinction will become important later if you're building a reliable lifecycle/history system.