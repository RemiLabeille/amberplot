#################################################################################################
# MD simulation trajectory to PDB per frame of interest
# 1_12_2026 
# Remi Labeille
# this script makes PDB files for a defined frame range within the trajectory
#################################################################################################

import argparse
from pathlib import Path
import mdtraj as md
import netCDF4

def main():
    parser = argparse.ArgumentParser(
        description="Convert AMBER MD trajectory frames to individual PDB files"
    )
    
    parser.add_argument(
        "traj_nc",
        type=Path,
        help="Path to trajectory NetCDF file (e.g., prod.nc)"
    )
    
    parser.add_argument(
        "topology_pdb",
        type=Path,
        help="Path to topology PDB file (e.g., LIG_solvated_tleap.pdb)"
    )
    
    # Create mutually exclusive group for frame selection
    frame_group = parser.add_mutually_exclusive_group()
    
    frame_group.add_argument(
        "--all",
        action="store_true",
        help="Extract all frames in the trajectory (overrides --start and --end)"
    )
    
    frame_group.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start frame (human numbering, default: 1)"
    )
    
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="End frame inclusive (default: last frame)"
    )
    
    parser.add_argument(
        "--outdir",
        type=Path,
        default=None,
        help="Output directory for PDB files (default: <topology_parent>/<pdbname>_trajectoryPDB)"
    )
    
    parser.add_argument(
        "--pdbname",
        type=str,
        default=None,
        help="Naming tag for output files (default: topology filename without .pdb)"
    )
    
    args = parser.parse_args()
    
    # ---- SETUP ----
    print(f"Loading trajectory: {args.traj_nc}")
    print(f"Topology: {args.topology_pdb}")
    
    # Set default pdbname if not provided
    pdbname = args.pdbname if args.pdbname else args.topology_pdb.stem
    
    # Set default outdir if not provided
    outdir = args.outdir if args.outdir else args.topology_pdb.parent / f"{pdbname}_trajectoryPDB"
    outdir.mkdir(parents=True, exist_ok=True)
    
    # ---- LOAD TRAJECTORY ----
    t = md.load(str(args.traj_nc), top=str(args.topology_pdb))
    total_frames = t.n_frames
    
    # Determine frame range
    if args.all:
        start_frame = 1
        end_frame = total_frames
        print(f"Trajectory has {total_frames} frames")
        print(f"Extracting ALL frames ({start_frame} to {end_frame}, inclusive)")
    else:
        start_frame = args.start
        end_frame = args.end if args.end is not None else total_frames
        print(f"Trajectory has {total_frames} frames")
        print(f"Extracting frames {start_frame} to {end_frame} (inclusive)")
    
    # ---- EXTRACT FRAMES ----
    sub = t[start_frame-1:end_frame]  # 0-based slice
    
    print(f"Saving {sub.n_frames} PDB files to {outdir}")
    
    for i in range(sub.n_frames):
        frame_num = start_frame + i
        filename = f"frame{frame_num:04d}_{pdbname}.pdb"
        filepath = outdir / filename
        sub[i].save_pdb(str(filepath))
        if (i + 1) % 10 == 0 or (i + 1) == sub.n_frames:  # Progress every 10 frames
            print(f"  ✓ {filename} ({i + 1}/{sub.n_frames})")
    
    print("✓ Done!")

if __name__ == "__main__":
    main()