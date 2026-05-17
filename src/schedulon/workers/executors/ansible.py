from schedulon.workers.executors.command import execute
def execute_playbook(path, extra_vars=None): return execute(f'ansible-playbook {path}')
