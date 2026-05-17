from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from schedulon.interfaces.api.middleware.security_headers import security_headers_middleware
from schedulon.interfaces.api.routes import admin, approvals, audit, auth, governance, health, jobs, recovery, reports, runtime, runs, targets, templates

def create_app() -> FastAPI:
    app = FastAPI(title="Schedulon API", version="1.0.0", docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")
    app.middleware("http")(security_headers_middleware)
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
    app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
    app.include_router(targets.router, prefix="/api/v1/targets", tags=["targets"])
    app.include_router(runs.router, prefix="/api/v1/runs", tags=["runs"])
    app.include_router(approvals.router, prefix="/api/v1/approvals", tags=["approvals"])
    app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
    app.include_router(audit.router, prefix="/api/v1/audit-events", tags=["audit"])
    app.include_router(runtime.router, prefix="/api/v1/runtime", tags=["runtime"])
    app.include_router(recovery.router, prefix="/api/v1/recovery", tags=["recovery"])
    app.include_router(governance.router, prefix="/api/v1/governance", tags=["governance"])
    app.include_router(templates.router, prefix="/api/v1/templates", tags=["templates"])
    app.add_api_route("/metrics", health.metrics, methods=["GET"], include_in_schema=False)
    static_dir = Path(__file__).resolve().parents[1] / "web" / "static"
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    @app.get("/ui", include_in_schema=False)
    def ui(): return FileResponse(static_dir / "index.html")
    @app.get("/", include_in_schema=False)
    def root(): return FileResponse(static_dir / "index.html")
    return app
app = create_app()
