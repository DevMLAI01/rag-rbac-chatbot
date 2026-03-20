"""Unit tests for RBAC filter — no Chroma connection needed."""
import pytest
from config.roles import Role
from src.retrieval.rbac_filter import build_rbac_filter


def test_employee_sees_only_general():
    f = build_rbac_filter(Role.EMPLOYEE)
    assert f == {"dept_general": {"$eq": True}}


def test_finance_sees_finance_and_general():
    f = build_rbac_filter(Role.FINANCE)
    assert f == {"$or": [
        {"dept_finance": {"$eq": True}},
        {"dept_general": {"$eq": True}},
    ]}


def test_clevel_sees_all_departments():
    f = build_rbac_filter(Role.CLEVEL)
    keys = {clause.keys().__iter__().__next__() for clause in f["$or"]}
    # clevel should have access to all 6 departments
    assert "dept_clevel" in keys
    assert "dept_finance" in keys
    assert "dept_hr" in keys
    assert "dept_engineering" in keys
    assert "dept_marketing" in keys
    assert "dept_general" in keys


def test_finance_filter_excludes_hr():
    f = build_rbac_filter(Role.FINANCE)
    # HR dept flag must not appear anywhere in the filter
    filter_str = str(f)
    assert "dept_hr" not in filter_str


def test_marketing_filter_excludes_finance():
    f = build_rbac_filter(Role.MARKETING)
    filter_str = str(f)
    assert "dept_finance" not in filter_str


def test_hr_filter_excludes_engineering():
    f = build_rbac_filter(Role.HR)
    filter_str = str(f)
    assert "dept_engineering" not in filter_str
