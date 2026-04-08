import ezero_filter as ezero
import time

# Initialisation avec ton cerveau de 556 Ko
filtre = ezero.EZeroFilter()

# ÉCHANTILLON A : Logiciel Python (Data Science)
python_code = """
import numpy as np
import pandas as pd

def calculate_recycling_efficiency(waste_input, metal_yield):
    # Calcul de performance pour PeP Recycling
    efficiency = (metal_yield / waste_input) * 100
    if efficiency > 85:
        return "Optimal"
    else:
        return "To Improve"

data = {"iron": 500, "copper": 200}
result = calculate_recycling_efficiency(1000, 700)
"""

# ÉCHANTILLON B : Blockchain (Le contrat DAO précédent)
solidity_code = """
pragma solidity ^0.8.20;
contract PeP_Governance {
    uint256 public constant QUORUM = 400000;
    function vote(uint256 id) public {
        require(id > 0, "Invalid ID");
    }
}
"""

print(f"--- TEST DE COLLISION SÉMANTIQUE ---")

print("\n[RUNNING PYTHON TEST]")
res_py = filtre.filter(python_code)
print(f"Gain Python   : {res_py['gain_pct']}%")
print(f"Squelette Py  : {res_py['skeleton']}")

print("\n[RUNNING SOLIDITY TEST]")
res_sol = filtre.filter(solidity_code)
print(f"Gain Solidity : {res_sol['gain_pct']}%")
print(f"Squelette Sol : {res_sol['skeleton']}")