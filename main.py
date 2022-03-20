from typing import List, Set
from merkle_tree import MerkleNode
from tools import MockTx, create_mock_txs


# Build a Merkle Tree from a set of mock transactions
def build_merkle_tree(txs: List[MockTx]) -> MerkleNode:
    return build_merkle_nodes([MerkleNode.from_transaction(tx) for tx in txs], depth=1)


def build_merkle_nodes(nodes: List[MerkleNode], depth: int) -> MerkleNode:
    if len(nodes) == 0:
        raise Exception("Invalid node amount")
    if len(nodes) == 1:
        return nodes[0]  # Merkle root

    # When there is an odd number of nodes, use the same hash from the last one
    if len(nodes) % 2 == 1:
        nodes.append(nodes[-1])

    new_nodes: List[MerkleNode] = list()
    for i in range(0, len(nodes), 2):
        new_nodes.append(MerkleNode.from_children(nodes[i], nodes[i + 1], depth))

    return build_merkle_nodes(new_nodes, depth + 1)


def search_for_differences(
    node_a: MerkleNode, node_b: MerkleNode, visited: Set[bytes] = set()
) -> List[str]:
    # Tree branch already visited
    if node_a.node_hash in visited and node_b.node_hash in visited:
        return []
    visited.update([node_a.node_hash, node_b.node_hash])

    # Equal children
    if node_a.node_hash == node_b.node_hash:
        return []

    if node_a.is_leaf and node_b.is_leaf:
        return [f"Difference found: {node_a.tx.data} vs. {node_b.tx.data}"]
    elif node_a.is_leaf or node_b.is_leaf:
        raise Exception("Trees have different heights")

    left_differences: List[str] = []
    if node_a.left_child.node_hash != node_b.left_child.node_hash:
        left_differences = search_for_differences(node_a.left_child, node_b.left_child)

    right_differences: List[str] = []
    if node_a.right_child.node_hash != node_b.right_child.node_hash:
        right_differences = search_for_differences(
            node_a.right_child, node_b.right_child
        )

    return left_differences + right_differences


def search_for_transaction(node: MerkleNode, target_tx: MockTx, carry: int = 0) -> bool:
    if node.is_leaf and node.tx.idx != target_tx.idx:
        raise Exception(f"Something went wrong! {node.tx} vs. {target_tx}")
    if node.is_leaf:
        return node.tx.data == target_tx.data

    if target_tx.idx < carry + (2 ** node.depth) / 2:
        return search_for_transaction(node.left_child, target_tx, carry)

    carry += (2 ** node.depth) / 2
    return search_for_transaction(node.right_child, target_tx, carry)


def test_differences():
    n1 = create_mock_txs(["a", "b", "c", "d", "e"])
    n2 = create_mock_txs(["a", "x", "c", "y", "z"])

    merkle_1 = build_merkle_tree(n1)
    merkle_2 = build_merkle_tree(n2)

    for diff in search_for_differences(merkle_1, merkle_2):
        print(diff)


def test_search_transaction():
    merkle_tree = build_merkle_tree(create_mock_txs(["a", "b", "c", "d", "e"]))
    target_tx = MockTx(3, "e")

    transaction_on_tree = search_for_transaction(merkle_tree, target_tx)
    status = "is" if transaction_on_tree else "is not"
    print(
        f"Transaction {target_tx.idx} with data: '{target_tx.data}'"
        f" {status} on Merkle Tree"
    )


# test_differences()
test_search_transaction()
