# a file to call other functions after the download is complete (post download)


import glob

import geojson
from utils.utils import merge_dicts
from utils.normalization import compute_band_stats
from utils.splits import create_splits
import os
import argparse


def merge_tile_info(tile_dir, dst_path):
    if os.path.exists(dst_path):
        print("Merged tile info already exists")
        return
    paths = sorted(glob.glob(tile_dir + "/*.json"))

    # reading all the tile json files
    tile_info_dict = {}
    for path in paths:
        with open(path) as f:
            tmp = geojson.load(f)
        tile_info_dict = tmp | tile_info_dict

    # writing the merged dictionary to a file
    with open(dst_path, "w") as f:
        geojson.dump(tile_info_dict, f)

    # remove the individual tile_info files
    # for path in paths:
    #     os.remove(path)


def main(args):
    """
    A function to call other functions after the download is complete.
    merges all the tile_info files into a single file (these are temporary files created by the slurm jobs)
    converts the downloaded data to h5 format
    computes the band stats
    creates the splits (train and valid only)
    """

    print("Merging the tile_info files for all slurm jobs into a single file")
    out_path = (
        os.path.join(
            args.data_dir, args.data_dir.split("/")[-1] + "_tile_info.json"
        )
        if args.data_dir[-1] != "/"
        else os.path.join(
            args.data_dir, args.data_dir.split("/")[-2] + "_tile_info.json"
        )
    )
    merge_tile_info(os.path.join(args.data_dir, "tile_info"), out_path)

    # print('converting to h5')
    # ret = os.system(f'python -u utils/convert_to_h5.py --mode create --data_dir {args.data_dir}')
    # if ret != 0:
    #     exit()
    print("computing band stats")
    compute_band_stats(data_folder=args.data_dir)

    print("computing splits")
    create_splits(data_folder=args.data_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # provide the name of the output folder, by default the path of the output json is the name followed by _tile_info.json
    parser.add_argument(
        "--data_dir", type=str, help="path to the output folder", required=True
    )
    args = parser.parse_args()
    main(args)
