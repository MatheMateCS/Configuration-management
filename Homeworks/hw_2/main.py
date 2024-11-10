import argparse
import datetime
import os
import sys
import zlib


# Getting arguments transmitted to script
def get_args()->list: 
    parser = argparse.ArgumentParser()
    parser.add_argument("gvis_path", help="Path to graph visualizer")   # path to graph visualizer
    parser.add_argument("repo_path", help="Path to analysed repo")      # path to repository being analiysed
    parser.add_argument("res_path", help="Path to the result code")     # path to result in code form
    parser.add_argument("branch_name", help="Branch name")              # branch name
    args = parser.parse_args()
    return [args.gvis_path, args.repo_path, args.res_path, args.branch_name]

# Choosing branch and store information about commits
def get_commits_info(repo_path: str, branch_name: str)->dict: 
    if ".git" in os.listdir(repo_path):
        repo_path = os.path.join(repo_path, ".git")
    try:
        branches_path = os.path.join(repo_path, "refs", "heads")    # Path to branches references
        if not branch_name in os.listdir(branches_path):                    # Handling absence of that branch
            print(f"{'\033[91m'}There is no branch with name '{branch_name}' in this git tree!{'\033[0m'}")
            with open(os.path.join(repo_path, "HEAD"), "r") as href:
                content = href.read()
                if content.startswith("ref:"):
                    branch_name = content[5:].split('/')[-1].strip()        # Choosing current branch instead of non-existent
                else:
                    print(f"{'\033[91m'}Well, there is no git branches in this repo at all!{'\033[0m'}")
                    sys.exit(0)
            print(f"{'\033[91m'}So, the commits graph will be built for the current branch '{branch_name}'{'\033[0m'}")
        
        dict_info = {}                                                      # key - commit hash, value = list of [[parents], date, author]
        objects_path = os.path.join(repo_path, "objects")           # Path to git objects
        with open(os.path.join(branches_path, branch_name), "r") as bref:
            last_commit_hash = bref.read().strip()                          # Getting hash-reference to last commit in this branch
        commits_bypassing(objects_path, last_commit_hash, dict_info)
        return dict_info
    except FileNotFoundError:                                               # Handling wrong file pathes
        print(f"{'\033[91m'}It seems that you've entered wrong path to repo.\n\
              \rPlease restart program with correct arguments!{'\033[0m'}")
        sys.exit(-1)

# Recursive bypassing of commits
def commits_bypassing(objects_path: str, commit_hash: str, dict_info: dict)->None:
    with open(os.path.join(objects_path, commit_hash[:2], commit_hash[2:]), "rb") as info:
        data = zlib.decompress(info.read()).decode('utf-8').splitlines()        # Load commit info
    date, author, parents = None, "", []
    for line in data:
        if line.startswith("parent"):
            parents.append(line.split()[1])
        elif line.startswith("author"):
            author = line.split()[1]                                            # Parse author of commit
            date = datetime.datetime.fromtimestamp(int([i for i in line.split() 
                                    if len(i) == 10 and i.startswith("17")][0]))# Parse date of commit
    dict_info[commit_hash] = [parents, str(date), author]                       # Record commit info to the dictionary
    for parent in parents:
        commits_bypassing(objects_path, parent, dict_info)                      # Recursive calling

# Bulding a Mermaid graph
def build_tree(commits_info: dict)->str:
    graph = "flowchart TD\n"
    for commit_hash in commits_info:                                            # Bypassing dictionary
        if commit_hash != "leaf":
            commit_info = commits_info[commit_hash]
            graph += f"\t'{commit_hash}'[{commit_info[2]} {commit_info[1]}]\n"  # Calling the vertex
            for parent in commit_info[0]:                                       # Noting dependencies
                graph += f"\t'{commit_hash}' --> '{parent}'\n"
    return graph

# Writing Mermaid code to file
def write_to_file(res_path: str, data: str)->None:
    try:
        with open(res_path, "w+") as res:
            res.write(data)
        print(f"{'\033[92m'}Mermaid code of git commits graph was successfully saved into '{res_path}'{'\033[0m'}")
    except FileNotFoundError:
        print(f"{'\033[91m'}It seems that you've entered wrong path to result file.\n\
              \rPlease restart program with correct arguments!{'\033[0m'}")
        
def main()->None:
    args = get_args()                                                           # Receiving args
    write_to_file(args[2], build_tree(get_commits_info(args[1], args[3])))      # Writing Mermaid code
    os.system(f"python3 {args[0]} {args[2]}")                                   # Launch visualizer script

if __name__ == "__main__":
    main()
