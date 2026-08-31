import sys
import types
import unittest
from pathlib import Path


try:
    import rich.console  # noqa: F401
    import rich.table  # noqa: F401
    import tiktoken  # noqa: F401
except ModuleNotFoundError:
    # Keep this adapter unit test runnable when optional AMB runtime extras are absent.
    sys.modules.setdefault("tiktoken", types.ModuleType("tiktoken"))
    rich_module = types.ModuleType("rich")
    console_module = types.ModuleType("rich.console")
    table_module = types.ModuleType("rich.table")
    console_module.Console = object
    table_module.Table = object
    sys.modules.setdefault("rich", rich_module)
    sys.modules.setdefault("rich.console", console_module)
    sys.modules.setdefault("rich.table", table_module)

# Import the LoCoMo adapter without importing every optional dataset adapter.
dataset_package = types.ModuleType("memory_bench.dataset")
dataset_package.__path__ = [str(Path(__file__).parents[1] / "src" / "memory_bench" / "dataset")]
sys.modules["memory_bench.dataset"] = dataset_package

from memory_bench.dataset.locomo import LoComoDataset


class LoComoDatasetTests(unittest.TestCase):
    def test_load_documents_filters_to_requested_conversation_ids(self) -> None:
        dataset = LoComoDataset()
        dataset._load_raw = lambda: [
            {
                "sample_id": "alpha",
                "conversation": {
                    "speaker_a": "Ada",
                    "speaker_b": "Ben",
                    "session_1": [{"speaker": "Ada", "text": "alpha"}],
                },
            },
            {
                "sample_id": "beta",
                "conversation": {
                    "speaker_a": "Bea",
                    "speaker_b": "Cam",
                    "session_1": [{"speaker": "Bea", "text": "beta"}],
                },
            },
        ]

        documents = dataset.load_documents("locomo10", user_ids={"alpha"})

        self.assertEqual([document.user_id for document in documents], ["alpha"])


if __name__ == "__main__":
    unittest.main()
