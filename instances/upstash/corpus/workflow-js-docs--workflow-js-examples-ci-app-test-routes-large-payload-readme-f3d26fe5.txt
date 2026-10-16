# README
# джерело: https://github.com/upstash/workflow-js/blob/v1.4.0/examples/ci/app/test-routes/large-payload/README.md
# отримано: 2026-10-16
# версія: workflow-1.4.0, workflow-1.3.3, workflow-1.3.2, workflow-1.3.1, workflow-1.3.0, workflow-1.2.1, workflow-1.2.0, workflow-1.1.1, workflow-1.1.0, workflow-1.0.0, workflow-0.2.23, workflow-0.2.22, workflow-0.2.21, workflow-0.2.20, workflow-0.2.19, workflow-0.2.18, workflow-0.2.17, workflow-0.2.16, workflow-0.2.15, workflow-0.2.14, workflow-0.2.13, workflow-0.2.12, workflow-0.2.11, workflow-0.2.10, workflow-0.2.9, workflow-0.2.8, workflow-0.2.7, workflow-0.2.6, workflow-0.2.5, workflow-0.2.4, workflow-0.2.3, workflow-0.2.2, workflow-0.2.1, workflow-0.2.0

This directory has a endpoints testing the lazy fetch functionality:
- `call-result`: endpoint called with context.call returns a large payload
- `error`: a large error is thrown. failureFunction is called with the initial body.
- `initial`: workflow is started with a large object
- `step-result`: a step returns a large result
- `step-result-parallel`: a parallel step returns a large result

In `utils.ts`, you can find the large object used.
