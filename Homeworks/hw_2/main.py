import argparse
import datetime
import os
import zlib


def get_args(): # Getting arguments transmitted to script
    parser = argparse.ArgumentParser()
    parser.add_argument("gvis_path", help="Path to graph visualizer") # path to graph visualizer
    parser.add_argument("repo_path", help="Path to analysed repo") # path to repository being analiysed
    parser.add_argument("res_path", help="Path to the result code") # path to result in code form
    parser.add_argument("branch_name", help="Branch name") # branch name
    args = parser.parse_args()
    return [args.gvis_path, args.repo_path, args.res_path, args.branch_name]

def main():
    args = get_args()
    print(args)

if __name__ == "__main__":
    main()
