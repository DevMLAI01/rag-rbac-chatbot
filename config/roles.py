from enum import Enum


class Role(str, Enum):
    FINANCE = "finance"
    MARKETING = "marketing"
    HR = "hr"
    ENGINEERING = "engineering"
    CLEVEL = "clevel"
    EMPLOYEE = "employee"


# Single source of truth for role → accessible departments
ROLE_ACCESS_MAP: dict[Role, list[str]] = {
    Role.FINANCE:     ["finance", "general"],
    Role.MARKETING:   ["marketing", "general"],
    Role.HR:          ["hr", "general"],
    Role.ENGINEERING: ["engineering", "general"],
    Role.CLEVEL:      ["finance", "marketing", "hr", "engineering", "clevel", "general"],
    Role.EMPLOYEE:    ["general"],
}
