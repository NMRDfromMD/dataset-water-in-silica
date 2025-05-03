#!/usr/bin/env python
# coding: utf-8

import os
import MDAnalysis as mda
from nmrdfrommd import NMRD

from utilities import save_result, get_git_repo_path


def main(nb_iterations):
    """Process one temperature point"""

    git_path = get_git_repo_path()
    data_dir = os.path.join(git_path, "data")
    topology_file = os.path.join(data_dir, "prod.tpr")
    trajectory_file = os.path.join(data_dir, "prod.xtc")

    if not os.path.exists(topology_file) or not os.path.exists(trajectory_file):
        print(f"Missing MD data")
        return

    try:
        u = mda.Universe(topology_file, trajectory_file)
        water = u.select_atoms("resname SOL and type HW")
        surface_groups = u.select_atoms("resname SiOH and type HOY")
        all_H = water+surface_groups

        nmr_water_intra = NMRD(
            u=u,
            atom_group=water,
            isotropic = False,
            type_analysis="intra_molecular",
            number_i=5) # to compensate for poorer statistics
        nmr_water_intra.run_analysis()

        save_result(nmr_water_intra, name=f"nmr_water_intra")
        print(f"nmr water intra Success")

        nmr_water_inter = NMRD(
            u=u,
            atom_group=water,
            isotropic = False,
            type_analysis="inter_molecular",
            number_i=1)
        nmr_water_inter.run_analysis()

        save_result(nmr_water_inter, name=f"nmr_water_inter")
        print(f"nmr water inter Success")

        nmr_full= NMRD(
            u=u,
            atom_group=all_H,
            isotropic = False,
            type_analysis="full",
            number_i=1)
        nmr_full.run_analysis()

        save_result(nmr_full, name=f"nmr_full")
        print(f"nmr full Success")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main(nb_iterations=500)