from dataclasses import dataclass
from typing import List


@dataclass
class MockTx:
    idx: int
    data: str

    def __str__(self) -> str:
        return f"Tx: {self.idx} with {self.data}"


def create_mock_txs(data_list: List[str]):
    return [MockTx(i, data) for i, data in enumerate(data_list)]
