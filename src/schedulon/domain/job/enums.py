from enum import StrEnum
class ExecutionBackend(StrEnum):
    COMMAND='command'
    SCRIPT_INLINE='script_inline'
    SCRIPT_FILE='script_file'
    ANSIBLE_PLAYBOOK='ansible_playbook'
    AWX_JOB='awx_job'
