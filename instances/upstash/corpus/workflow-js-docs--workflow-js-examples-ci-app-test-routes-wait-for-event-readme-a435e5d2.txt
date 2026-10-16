# README
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/ci/app/test-routes/wait-for-event/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14, workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0, workflow-0.1.5, workflow-0.1.4, workflow-0.1.3

Under the `wait-for-event` directory, there are three routes:
- `/workflow`: the workflow we run in the tests to do the following in order:
  1. wait for a random event which should timeout
  2. sequentially, call `/notifier` and wait to get notified. `/notifier` uses `waitUntil` to sleep for 2 secs and call notify
  3. in parallel, call `/notifier-workflow` and wait to get notified with text data
  4. wait to get notified with object data by `/notifier-workflow`
- `/notifier`: an endpoint which notifies the workflow using the SDK
- `/notifier-workflow`: a workflow which notifies the original workflow two times:
  1. with a text event data
  2. with an object event data

`/notifier` workflow will keep retrying until it has successfully notified the original worklfow two times (one with text one with object).

once the `/notifier-workflow` finishes execution, it will save it's state to Redis. `/workflow` will check if `/notifier-workflow` has finished in its last step.
