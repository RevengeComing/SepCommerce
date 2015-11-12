from ..decorators import permission_required
from .models import Permission

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
