JOB_ID="$1"
curl -X POST http://localhost:8000/api/v1/jobs/${JOB_ID}/trigger -H 'Content-Type: application/json' -d '{"ticket_number":"CHG001"}'
