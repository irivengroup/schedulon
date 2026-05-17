from __future__ import annotations
def get_actor(x_schedulon_actor_id='system', x_schedulon_roles='admin'):
    return {'actor_id': x_schedulon_actor_id, 'roles': [r.strip() for r in x_schedulon_roles.split(',') if r.strip()], 'actor_type':'user'}
