from routing import TestRouter


def test_change_routes_to_tests_for_dependent_module() -> None:
    router = TestRouter(
        {
            "all_tests": ["tests"],
            "modules": {
                "core": {"patterns": ["src/core.py"], "tests": ["tests/test_core.py"]},
                "app": {
                    "patterns": ["src/app.py"],
                    "tests": ["tests/test_app.py"],
                    "depends_on": ["core"],
                },
            },
        }
    )
    plan = router.plan(["src/core.py"])
    assert plan.test_paths == ("tests/test_app.py", "tests/test_core.py")
    assert not plan.full_suite


def test_unmapped_file_falls_back_to_full_suite() -> None:
    plan = TestRouter({"all_tests": ["tests"], "modules": {}}).plan(["new_module.py"])
    assert plan.full_suite
    assert plan.test_paths == ("tests",)
