frontend pg_write
  bind *:${PG_WRITE_PORT}
  default_backend pg_primary
backend pg_primary
  server pg1 ${PG_NODE_1}:5432 check
