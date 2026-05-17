RUN_ID="$1"
curl http://localhost:8000/api/v1/reports/${RUN_ID}
