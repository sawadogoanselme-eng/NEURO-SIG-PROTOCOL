import ezero_filter as ezero
import time

# Initialisation
filtre = ezero.EZeroFilter()

# Structure de Gouvernance complexe (DAO)
dao_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PeP_Governance {
    struct Proposal {
        uint256 id;
        address proposer;
        uint256 eta;
        uint256 startBlock;
        uint256 endBlock;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
    }

    uint256 public constant QUORUM_VOTES = 400000 * 10**18; 
    uint256 public constant VOTING_DELAY = 1; 
    uint256 public constant VOTING_PERIOD = 50400; 

    mapping(uint256 => Proposal) public proposals;

    function propose(address[] memory targets, uint256[] memory values, string memory description) public returns (uint256) {
        require(msg.sender != address(0), "Proposeur invalide");
        // Logique de création de proposition complexe
        return 12345;
    }

    function castVote(uint256 proposalId, uint8 support) public {
        Proposal storage proposal = proposals[proposalId];
        require(block.number <= proposal.endBlock, "Vote termine");
        if (support == 1) {
            proposal.forVotes += 100;
        } else {
            proposal.againstVotes += 100;
        }
    }
}
"""

print(f"\n--- TEST DAO : STRUCTURES DE VOTE COMPLEXES ---")
res = filtre.filter(dao_code)

print(f"✅ Statut         : Analyse complétée")
print(f"📊 Gain Énergétique: {res['gain_pct']}%")
print(f"⚡ Latence        : {res['ms']} ms")
print(f"🧠 Synapses       : {res['plasticity']['synapses']}")
print(f"\n--- SQUELETTE LOGIQUE EXTRAIT ---")
print(res['skeleton'])