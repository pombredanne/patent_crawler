""" Redis and MongoDB settings
"""
# MongoDB settings
# MONGODB_JOBS = "mongodb://192.168.170.60:8051/mrq" # MongoDB URI for the jobs, scheduled_jobs & workers database.Defaults to mongodb://127.0.0.1:27017/mrq
# MONGODB_LOGS = 1 #MongoDB URI for the logs database."0" will disable remote logs, "1" will use main MongoDB.Defaults to 1
# If provided, sets the log collection to capped to that amount of bytes.
MONGODB_LOGS_SIZE = None
# If provided, skip the creation of MongoDB indexes at worker startup.
NO_MONGODB_ENSURE_INDEXES = None

# Redis settings
# REDIS = "redis://oio:oio@192.168.251.4:5201/2" #Redis URI.Defaults to redis://127.0.0.1:6379
REDIS_PREFIX = "mrq"  # Redis key prefix.Default to "mrq".
# Redis max connection pool size.Defaults to 1000.
REDIS_MAX_CONNECTIONS = 1000
# Redis connection pool timeout to wait for an available connection.Defaults to 30.
REDIS_TIMEOUT = 30

"""General MrQ settings
"""
TRACE_GREENLETS = False  # Collect stats about each greenlet execution time and switches.Defaults to False.
# Collect stats about memory for each task. Incompatible with `GREENLETS` > 1. Defaults to False.
TRACE_MEMORY = False
TRACE_IO = True  # Collect stats about all I/O operations.Defaults to True.
PRINT_MONGODB = False  # Print all MongoDB requests.Defaults to False.
# Create a .png object graph in trace_memory_output_dir with a random object of this type.
TRACE_MEMORY_TYPE = ""
# Directory where to output .pngs with object graphs.Defaults to folder memory_traces.
TRACE_MEMORY_OUTPUT_DIR = "memory_traces"
PROFILE = False  # Run profiling on the whole worker.Defaults to False.
NAME = None  # Specify a different name.
QUIET = False  # Don\'t output task logs.Defaults to False.
CONFIG = None  # Path of a config file.
# Path to a custom worker class.Defaults to "mrq.worker.Worker".
WORKER_CLASS = "mrq.worker.Worker"
VERSION = False  # Prints current MRQ version.Defaults to  False.
# Skips patching __import__ to fix gevent bug #108.Defaults to False.
NO_IMPORT_PATCH = False
# Adds random latency to the network calls, zero to N seconds. Can be a range (1-2)').Defaults to 0.
ADD_NETWORK_LATENCY = 0
# Seconds the results are kept in MongoDB when status is success.Defaults to 604800 seconds which is 7 days.
DEFAULT_JOB_RESULT_TTL = 604800
# Seconds the tasks are kept in MongoDB when status is abort.Defaults to 86400 seconds which is 1 day.
DEFAULT_JOB_ABORT_TTL = 86400
# Seconds the tasks are kept in MongoDB when status is cancelDefaults to 86400 seconds which is 1 day.
DEFAULT_JOB_CANCEL_TTL = 86400
# In seconds, delay before interrupting the job.Defaults to 3600 seconds which is 1 hour.
DEFAULT_JOB_TIMEOUT = 3600
# Set the status to "maxretries" after retrying that many times.Defaults to 3 seconds.
DEFAULT_JOB_MAX_RETRIES = 3
# Seconds before a job in retry status is requeued again.Defaults to 3 seconds.
DEFAULT_JOB_RETRY_DELAY = 3
# Do not use compacted job IDs in Redis. For compatibility with 0.1.x only. Defaults to
USE_LARGE_JOB_IDS = False

""" mrq-worker settings
"""
# QUEUES = ("default",) # The queues to listen on.Defaults to default , which will listen on all queues.
# MAX_JOBS = 0 #Gevent:max number of jobs to do before quitting. Workaround for memory leaks in your tasks. Defaults to 0
# MAX_MEMORY = 1 #Max memory (in Mb) after which the process will be shut down. Use with PROCESS = [1-N] to have supervisord automatically respawn the worker when this happens.Defaults to 1
# GRENLETS = 1 #Max number of greenlets to use.Defaults to 1.
# PROCESSES = 0 #Number of processes to launch with supervisord.Defaults to 0.
# SUPERVISORD_TEMPLATE = "supervisord_templates/default.conf" #Path of supervisord template to use. Defaults to supervisord_templates/default.conf.
# SCHEDULER = False #Run the scheduler.Defaults to False.
# SCHEDULER_INTERVAL = 60 #Seconds between scheduler checks.Defaults to 60 seconds, only ints are acceptable.
# REPORT_INTERVAL = 10.5 #Seconds between worker reports to MongoDB.Defaults to 10 seconds, floats are acceptable too.
# REPORT_FILE = "" #Filepath of a json dump of the worker status. Disabled if none.
# ADMIN_PORT = 0 #Start an admin server on this port, if provided. Incompatible with --processes.Defaults to 0
# ADMIN_IP = "127.0.0.1" #IP for the admin server to listen on. Use "0.0.0.0" to allow access from outside.Defaults to 127.0.0.1.
# LOCAL_IP = "" #Overwrite the local IP, to be displayed in the dashboard.
# MAX_LATENCY = 3  #Max seconds while worker may sleep waiting for a new job.Can be < 1 and a float value.

""" mrq-dashboard settings
"""
# DASHBOARD_HTTPAUTH = "" #HTTP Auth for the Dashboard. Format is user
# DASHBOARD_QUEUE = "default" #Default queue for dashboard actions.
# DASHBOARD_PORT = 5555 #Use this port for mrq-dashboard.Defaults to port 5555.
# DASHBOARD_IP = "0.0.0.0" #Bind the dashboard to this IP. Default is 0.0.0.0, use 127.0.0.1 to restrict access

SCHEDULER_TASKS = [

    # This will requeue jobs in the 'retry' status, until they reach their max_retries.
    {
        "path": "mrq.basetasks.cleaning.RequeueRetryJobs",
        "params": {},
        "interval": 60
    },

    # This will requeue jobs marked as interrupted, for instance when a worker received SIGTERM
    {
        "path": "mrq.basetasks.cleaning.RequeueInterruptedJobs",
        "params": {},
        "interval": 5 * 60
    },

    # This will requeue jobs marked as started for a long time (more than their own timeout)
    # They can exist if a worker was killed with SIGKILL and not given any time to mark
    # its current jobs as interrupted.
    {
        "path": "mrq.basetasks.cleaning.RequeueStartedJobs",
        "params": {},
        "interval": 3600
    },

    # This will requeue jobs 'lost' between redis.blpop() and mongo.update(status=started).
    # This can happen only when the worker is killed brutally in the middle of dequeue_jobs()
    {
        "path": "mrq.basetasks.cleaning.RequeueLostJobs",
        "params": {},
        "interval": 24 * 3600
    },

    # This will clean the list of known queues in Redis. It will mostly remove empty queues
    # so that they are not displayed in the dashboard anymore.
    {
        "path": "mrq.basetasks.cleaning.CleanKnownQueues",
        "params": {},
        "interval": 24 * 3600
    }
]
