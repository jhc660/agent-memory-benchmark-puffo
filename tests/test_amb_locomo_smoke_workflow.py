from pathlib import Path
import unittest


WORKFLOW = Path(__file__).parents[1] / ".github" / "workflows" / "amb-locomo-smoke.yml"


class AmbLocomoSmokeWorkflowTests(unittest.TestCase):
    def test_enables_only_bm25_and_puffo_q1_arms(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertEqual(workflow.count("--memory bm25 --query-limit 1"), 1)
        self.assertEqual(workflow.count("--memory puffo --query-limit 1"), 1)
        self.assertNotIn("--memory puffo-bm25", workflow)
        self.assertNotIn("--query-limit 50", workflow)


if __name__ == "__main__":
    unittest.main()
