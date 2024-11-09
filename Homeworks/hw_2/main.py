import argparse
import datetime
import os
import sys
import zlib

test_repo = "YP-Frontend"

# Getting arguments transmitted to script
def get_args()->list: 
    parser = argparse.ArgumentParser()
    parser.add_argument("gvis_path", help="Path to graph visualizer")   # path to graph visualizer
    parser.add_argument("repo_path", help="Path to analysed repo")      # path to repository being analiysed
    parser.add_argument("res_path", help="Path to the result code")     # path to result in code form
    parser.add_argument("branch_name", help="Branch name")              # branch name
    args = parser.parse_args()
    return [args.gvis_path, args.repo_path, args.res_path, args.branch_name]

# Bypassing commits and store information about them
def get_commits_hierarchy(repo_path: str, branch_name: str): 
    try:
        branches_path = os.path.join(repo_path, ".git", "refs", "heads")    # Path to branches references
        objects_path = os.path.join(repo_path, ".git", "objects")           # Path to git objects
        if not branch_name in os.listdir(branches_path):                    # Handling absence of that branch
            print(f"{'\033[91m'}There is no branch with name '{branch_name}' in this git tree!{'\033[0m'}")
            with open(os.path.join(repo_path, ".git", "HEAD")) as href:
                content = href.read()
                if content.startswith("ref:"):
                    branch_name = content[5:].split('/')[-1].strip()        # Choosing current branch instead of non-existent
                else:
                    print(f"{'\033[91m'}Well, there is no git branches in this repo at all!{'\033[0m'}")
                    sys.exit(0)
            print(f"{'\033[91m'}So, the commits graph will be built for the current branch '{branch_name}'{'\033[0m'}")
        
    except FileNotFoundError:                                               # Handling wrong file pathes
        print(f"{'\033[91m'}It seems that you've entered wrong pathes.\n\
              \rPlease restart program with correct arguments!{'\033[0m'}")
        sys.exit(-1)

def main():
    # args = get_args()
    # print(args)
    # print(os.listdir(os.path.join(test_repo, branches_path)))
    # print(f"{'\033[91m'}WARNING!")
    get_commits_hierarchy(test_repo, "master")
    
    
if __name__ == "__main__":
    main()
