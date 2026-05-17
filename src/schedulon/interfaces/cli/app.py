import subprocess, json
import typer, uvicorn, httpx
from rich.console import Console
from schedulon.infrastructure.db.session import SessionLocal
from schedulon.application.services import seed_demo
console=Console()
app=typer.Typer(no_args_is_help=True)
db_app=typer.Typer(); admin_app=typer.Typer(); jobs_app=typer.Typer(); reports_app=typer.Typer(); audit_app=typer.Typer()
app.add_typer(db_app,name='db'); app.add_typer(admin_app,name='admin'); app.add_typer(jobs_app,name='jobs'); app.add_typer(reports_app,name='reports'); app.add_typer(audit_app,name='audit')
def out(d): console.print_json(json.dumps(d, default=str))
@app.command()
def api(host:str='0.0.0.0', port:int=8000): uvicorn.run('schedulon.interfaces.api.app:app', host=host, port=port)
@app.command()
def worker(worker_id:str='worker-local'): console.print(f'Worker {worker_id} ready')
@app.command()
def scheduler(): console.print('Scheduler ready')
@app.command()
def version(): console.print('schedulon 1.0.0')
@db_app.command('upgrade')
def db_upgrade(): subprocess.run(['alembic','upgrade','head'], check=True); console.print('PROD_READY')
@db_app.command('rollback')
def db_rollback(revision:str='-1'): subprocess.run(['alembic','downgrade',revision], check=True); console.print('ROLLBACK_DONE')
@admin_app.command('seed-demo')
def seed_demo_cmd():
    with SessionLocal() as db: out(seed_demo(db))
@jobs_app.command('create-command')
def create_command(name:str, command:str, environment:str='development'): out(httpx.post('http://127.0.0.1:8000/api/v1/jobs', json={'name':name,'execution_backend':'command','backend_config':{'command':command},'environment':environment}).json())
@jobs_app.command('trigger')
def trigger(job_id:str, ticket:str|None=None): out(httpx.post(f'http://127.0.0.1:8000/api/v1/jobs/{job_id}/trigger', json={'ticket_number':ticket}).json())
@reports_app.command('get')
def get_report(run_id:str): out(httpx.get(f'http://127.0.0.1:8000/api/v1/reports/{run_id}').json())
@audit_app.command('list')
def audit_list(): out(httpx.get('http://127.0.0.1:8000/api/v1/audit-events').json())
