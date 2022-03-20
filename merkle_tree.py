# Improve type annotations
from __future__ import annotations

# Hashing algorithm
from hashlib import md5

from tools import MockTx


class MerkleNode:
    def __init__(self, node_hash: bytes, depth: int) -> None:
        self.node_hash: bytes = node_hash
        self.depth = depth
        self.left: MerkleNode | None
        self.right: MerkleNode | None
        # For demonstration purposes
        # Transaction from which the node was built from
        self.transaction: MockTx | None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    @property
    def left_child(self) -> MerkleNode:
        if self.left is None:
            raise Exception("Node has no left child")
        return self.left

    @property
    def right_child(self) -> MerkleNode:
        if self.right is None:
            raise Exception("Node has no right child")
        return self.right

    @property
    def tx(self) -> MockTx:
        if self.transaction is None:
            raise Exception("Node has no transaction associated")
        return self.transaction

    @classmethod
    def from_transaction(cls, tx: MockTx) -> MerkleNode:
        merkle_hash = md5(tx.data.encode()).digest()

        merkle_node = cls(merkle_hash, 0)
        merkle_node.left = merkle_node.right = None
        merkle_node.transaction = tx

        return merkle_node

    @classmethod
    def from_children(
        cls, left_child: MerkleNode, right_child: MerkleNode, depth: int
    ) -> MerkleNode:
        merkle_hash = md5(left_child.node_hash + right_child.node_hash).digest()

        merkle_node = cls(merkle_hash, depth)
        merkle_node.left = left_child
        merkle_node.right = right_child
        merkle_node.transaction = None

        return merkle_node
