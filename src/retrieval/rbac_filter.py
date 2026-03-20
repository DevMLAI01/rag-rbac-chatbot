from config.roles import Role, ROLE_ACCESS_MAP


def build_rbac_filter(role: str | Role) -> dict:
    """
    Build a Chroma metadata `where` filter for the given role.
    Uses per-department boolean flags (dept_finance, dept_hr, etc.)
    which are reliably supported by Chroma's $eq operator.
    """
    if isinstance(role, str):
        role = Role(role)

    accessible = ROLE_ACCESS_MAP[role]

    if len(accessible) == 1:
        return {f"dept_{accessible[0]}": {"$eq": True}}

    return {"$or": [{f"dept_{dept}": {"$eq": True}} for dept in accessible]}
