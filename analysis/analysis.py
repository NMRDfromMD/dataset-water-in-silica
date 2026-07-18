#!/usr/bin/env python
# coding: utf-8

import os
import MDAnalysis as mda
from nmrdfrommd import NMRD

from utilities import save_result, get_git_repo_path

git_path = get_git_repo_path()
data_dir = os.path.join(git_path, "data")
topology_file = os.path.join(data_dir, "prod.tpr")
trajectory_file = os.path.join(data_dir, "prod.xtc")

u = mda.Universe(topology_file, trajectory_file)
water = u.select_atoms("resname SOL and type HW")
surface_groups = u.select_atoms("resname SiOH and type HOY")
all_H = water+surface_groups

n = 500
repet = 1

for iteration in range(repet):

    nmr_water_intra = NMRD(
        u=u,
        atom_group=water,
        isotropic = False,
        type_analysis="intra_molecular",
        number_i=n)
    out = nmr_water_intra.run_analysis()

    save_result(out, n, iteration, "nmr_water_intra")
    print(f"nmr water intra Success")

    nmr_water_inter = NMRD(
        u=u,
        atom_group=water,
        isotropic = False,
        type_analysis="inter_molecular",
        number_i=n)
    out = nmr_water_inter.run_analysis()

    save_result(out, n, iteration, "nmr_water_inter")
    print(f"nmr water inter Success")

    nmr_full= NMRD(
        u=u,
        atom_group=all_H,
        isotropic = False,
        type_analysis="full",
        number_i=n)
    out = nmr_full.run_analysis()

    save_result(out, n, iteration ,"nmr_full")
    print(f"nmr full Success")

    nmr_water_silica = NMRD(
        u=u,
        atom_group=water,
        neighbor_group = surface_groups,
        isotropic = False,
        type_analysis="full",
        number_i=n)
    out = nmr_water_silica.run_analysis()

    save_result(out, n, iteration, "nmr_water_silica")
    print(f"nmr water-silica Success")

