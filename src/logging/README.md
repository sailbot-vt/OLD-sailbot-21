# `logging`

Sets up system and event logging.

Logging is started by the `main.py` module, so that testing and debugging during normal development does not clutter the log files. The `logging` module provides `start()` and `stop()` hooks to manage logging sessions.

Log files end in `.log.yml` and are not tracked by version control. Each session generates a new log file with a header that includes the timestamp and GPS location, if available.

Log files are stored on the SailBOT server for two weeks. At the conclusion of every logging session, a background task will attempt to upload all the log files currently stored on the local machine to the server. Logs will be stored in the `%/logs/` directory (where `%` is the application root).

## Log Types

#### Error logs

Errors include failed calls to hardware interfaces, and numerical methods failing. Warnings include unexpected sensor readings.

###### Log levels:
`WARNING`, `ERROR`, `CRITICAL`


#### Data logs

All queries to hardware interfaces should be logged. All modules actively querying hardware interfaces should provide pre-query hooks to set the return value of the hardware query.

Logging sessions are fully replayable. The top-level `sim.replay` module provides an interface to replay sessions. Options for real-time, fast-forward, and continuous replay are provided.

Replay sessions will mock the components in the `hardware` module and record the outputs to each for analysis.

###### Log levels:
`INFO`
