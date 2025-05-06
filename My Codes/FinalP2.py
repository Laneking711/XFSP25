import numpy as np
from typing import List, Tuple, NamedTuple
import sys
from polymerClasses import Position, molecule, macroMolecule


class PolymerStats(NamedTuple):
    """Container for polymer statistics results"""
    avg_com: Tuple[float, float, float]
    avg_ete: float
    std_ete: float
    avg_rg: float
    std_rg: float
    pdi: float
    actual_avg_N: float


def simulate_polymers(target_N: int, num_molecules: int) -> Tuple[List[macroMolecule], List[float]]:
    """
    Simulate polymer molecules with normally distributed degrees of polymerization
    Returns list of molecules and list of actual N values
    """
    molecules = []
    actual_Ns = []

    for _ in range(num_molecules):
        # Sample N from normal distribution with mean=target_N, std=0.1*target_N
        while True:
            N = int(np.random.normal(target_N, 0.1 * target_N))
            if N > 0:  # Ensure valid polymerization degree
                break
        actual_Ns.append(N)

        # Create macromolecule with random chain configuration
        polymer = macroMolecule(degreeOfPolymerization=N,
                                segmentLength=0.154e-9,  # 0.154 nm bond length
                                merWt=14.0)  # CH2 molecular weight
        polymer.freelyJointedChainModel()
        molecules.append(polymer)

    return molecules, actual_Ns


def calculate_statistics(molecules: List[macroMolecule], actual_Ns: List[int]) -> PolymerStats:
    """Calculate all required statistics for the polymer ensemble"""
    # Convert all measurements to proper units (nm for COM, µm for distances)
    nm_to_um = 1e-3  # Conversion from nm to µm

    # Center of mass (in nm)
    com_x = np.array([m.centerOfMass.x * 1e9 for m in molecules])  # m to nm
    com_y = np.array([m.centerOfMass.y * 1e9 for m in molecules])
    com_z = np.array([m.centerOfMass.z * 1e9 for m in molecules])
    avg_com = (
        np.mean(com_x),
        np.mean(com_y),
        np.mean(com_z)
    )

    # End-to-end distance (in µm)
    ete_distances = np.array([m.endToEndDistance * 1e6 for m in molecules])  # m to µm
    avg_ete = np.mean(ete_distances)
    std_ete = np.std(ete_distances, ddof=1)  # Sample standard deviation

    # Radius of gyration (in µm)
    rg_values = np.array([m.radiusOfGyration * 1e6 for m in molecules])  # m to µm
    avg_rg = np.mean(rg_values)
    std_rg = np.std(rg_values, ddof=1)

    # Polydispersity index (PDI)
    mws = np.array([m.MW for m in molecules])
    Mn = np.mean(mws)  # Number-average molecular weight
    Mw = np.mean(mws ** 2) / Mn  # Weight-average molecular weight
    pdi = Mw / Mn

    # Average actual degree of polymerization
    actual_avg_N = np.mean(actual_Ns)

    return PolymerStats(
        avg_com=avg_com,
        avg_ete=avg_ete,
        std_ete=std_ete,
        avg_rg=avg_rg,
        std_rg=std_rg,
        pdi=pdi,
        actual_avg_N=actual_avg_N
    )


def main() -> int:
    """Command line interface for polymer statistics"""
    print("Polymer Chain Statistics Calculator")
    print("----------------------------------")

    try:
        # Get user input with defaults
        target_N = int(input("degree of polymerization (1000)?: ") or 1000)
        if target_N <= 0:
            raise ValueError("Degree of polymerization must be positive")

        num_molecules = int(input("How many molecules (50)?: ") or 50)
        if num_molecules <= 0:
            raise ValueError("Number of molecules must be positive")

        # Run simulation
        print("\nSimulating polymer chains...", end='', flush=True)
        molecules, actual_Ns = simulate_polymers(target_N, num_molecules)
        print("done")

        # Calculate statistics
        print("Calculating statistics...", end='', flush=True)
        stats = calculate_statistics(molecules, actual_Ns)
        print("done\n")

        # Print results
        print(f"Metrics for {num_molecules} molecules of degree of polymerization ≈ {target_N}")
        print(f"Avg. Center of Mass (nm) = {stats.avg_com[0]:.3f}, {stats.avg_com[1]:.3f}, {stats.avg_com[2]:.3f}")

        print("\nEnd-to-end distance (µm):")
        print(f"    Average = {stats.avg_ete:.3f}")
        print(f"    Std. Dev. = {stats.std_ete:.3f}")

        print("\nRadius of gyration (µm):")
        print(f"    Average = {stats.avg_rg:.3f}")
        print(f"    Std. Dev. = {stats.std_rg:.3f}")

        print(f"\nPDI = {stats.pdi:.2f}")

        return 0  # Success

    except ValueError as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())