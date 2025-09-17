# CI notes

- Web CI now uses actions/setup-node with built-in pnpm cache. No separate STORE_PATH or actions/cache step is needed.
- NEXT_TELEMETRY_DISABLED is set during build to silence telemetry.
- Docker build steps updated to docker/build-push-action@v6.
- API CI uses actions/setup-python@v5 and actions/cache@v4.

Manual re-run: push to a branch that touches relevant paths or use the Run workflow UI.
