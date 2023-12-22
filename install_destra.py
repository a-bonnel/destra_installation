import os
import subprocess
from pprint import pprint

from utils import colorize

# Define Destra root folder
given_path = os.environ.get("DESTRA_ROOT_FOLDER")
if given_path:
    DESTRA_ROOT_FOLDER = given_path
else:
    print(
        colorize(
            "Before anything you need to set the DESTRA_ROOT_FOLDER constant at the top of the script.\n"
            "Use the command DESTRA_ROOT_FOLDER=/path/to/destra/root/folder python3 install_destra.py",
            "red",
        )
    )
    exit()

# Configuration flags
# GENERAL TASKS
ENABLE_CLONING = False
ENABLE_PULLING = False
ENABLE_BRANCHING = False
ENABLE_INSTALL_PRE_COMMIT = False
ENABLE_GIT_STATUS = False

# # Git add, commit, push
ENABLE_GIT_COMMIT_PUSH = False
ENABLE_ADD = False
ENABLE_STATUS = False
ENABLE_COMMIT = False
ENABLE_PUSH = False

ENABLE_GIT_HARD_RESET = False

# CUSTOM TASKS
ENABLE_DIFF = False
ENABLE_DIFF_CREATION = False
COMPARE_RELEASE_DIFF = False
COMPARE_RENOVATE_DIFF = False
ENABLE_OVERRIDING_COPY = False


# List of GitHub repositories to clone
repositories = [
    "destra-chart",
    "destra-docker-images",
    "destra-adapter-filestorage",
    "destra-adapter-internal",
    "destra-imageserver-philips",
    "destra-imageserver-bioformats",
    "destra-imageserver-openslide",
    "destra-common",
    "destra-imageserver-openslide-py",
    "destra-adapter-sectra",
    "destra-dispatcher",
    "destra-worker",
    "destra-adapter-roche",
    "destra-adapter-calopix",
    # "destra-integration-tests", # Not yet implemented
]

print("==========================================================")
print("This script is meant to perform actions on all Destra repositories")
print(f"Repos will be cloned in {DESTRA_ROOT_FOLDER} folder")
print("List of repositories :")
for repo in repositories:
    print(repo)
print("==========================================================")

# Create folder if it does not exist
if os.path.isdir(DESTRA_ROOT_FOLDER):
    print(colorize(f"The path '{DESTRA_ROOT_FOLDER}' already exists.", "green"))
else:
    print(colorize(f"The path '{DESTRA_ROOT_FOLDER}' does not exist.", "magenta"))
    create_dir = input(colorize("Do you wish to create that folder ? y/N", "magenta"))
    if create_dir == "y":
        os.makedirs(DESTRA_ROOT_FOLDER, exist_ok=True)
        print(
            colorize(
                f"The path '{DESTRA_ROOT_FOLDER}' has been created, continuing script.", "yellow"
            )
        )
    else:
        print(colorize("Folder was not created, stopping now", "red"))

if ENABLE_CLONING:
    # # Clone each repository into DESTRA_ROOT_FOLDER
    print(f"\n*****\n***TASK : Cloning in {os.getcwd()} and install pre-commit.\n*****")
    for repo in repositories:
        os.chdir(DESTRA_ROOT_FOLDER)
        if os.path.isdir(repo):
            print(f"The repo '{repo}' has already been cloned.")
        else:
            print(f"\nThe path '{repo}' does not exist and will be created.=======")
            subprocess.run(["git", "clone", f"git@github.com:owkin/{repo}.git"])
            if ENABLE_INSTALL_PRE_COMMIT:
                # Install pre-commit
                os.chdir(os.path.join(DESTRA_ROOT_FOLDER, repo))
                # subprocess.run(["pre-commit", "autoupdate"])
                subprocess.run(["pre-commit", "install"])
    print("Cloning completed.")

if ENABLE_PULLING:
    # # Git pull on all repos
    print(f"\n*****\n***Git pull on destra repos in {os.getcwd()}.\n*****")
    for repo in repositories:
        print(
            f"\nPulling in repo {repo} at {os.path.join(DESTRA_ROOT_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_ROOT_FOLDER, repo))
        subprocess.run(["git", "pull"])

if ENABLE_BRANCHING:
    # # Git pull on all repos
    print(f"\n*****\n***Git branch on destra repos in {os.getcwd()}.\n*****")
    branch_name = "abo/pre-commit"
    for repo in repositories:
        print(
            f"\nCreating branch {branch_name} in repo {repo} at {os.path.join(DESTRA_ROOT_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_ROOT_FOLDER, repo))
        subprocess.run(["git", "switch", "-c", branch_name])

if ENABLE_GIT_STATUS:
    # # Git pull on all repos
    print(f"\n*****\n***Git status on destra repos in {os.getcwd()}.\n*****")
    for repo in repositories:
        print(
            f"\nGit status in repo {repo} at {os.path.join(DESTRA_ROOT_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_ROOT_FOLDER, repo))
        subprocess.run(["git", "status"])

if ENABLE_GIT_COMMIT_PUSH:
    for repo in repositories:
        print(
            f"\nGit actions in repo {repo} at {os.path.join(DESTRA_ROOT_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_ROOT_FOLDER, repo))
        if ENABLE_ADD:
            subprocess.run(["git", "add", "."])
        if ENABLE_STATUS:
            subprocess.run(["git", "status"])
        if ENABLE_COMMIT:
            subprocess.run(["git", "commit", "-m", "Renovate file update"])
        if ENABLE_PUSH:
            subprocess.run(["git", "push", "--set-upstream", "origin", "abo/pre-commit"])


if ENABLE_GIT_HARD_RESET:
    # # Git pull on all repos
    print(f"\n*****\n***Git pull on destra repos in {os.getcwd()}.\n*****")
    for repo in repositories:
        print(
            f"\nGit status in repo {repo} at {os.path.join(DESTRA_ROOT_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_ROOT_FOLDER, repo))
        subprocess.run(["git", "reset", "--hard", "HEAD"])


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CUSTOM DIFF TASK
if ENABLE_DIFF:
    # Git diff
    os.chdir(DESTRA_ROOT_FOLDER)

    # Make temp folders
    temp_renovate = os.path.join(DESTRA_ROOT_FOLDER, "temp_renovate")
    temp_release = os.path.join(DESTRA_ROOT_FOLDER, "temp_release")
    os.makedirs(temp_renovate, exist_ok=True)
    os.makedirs(temp_release, exist_ok=True)

    files = [".releaserc", "renovate.json"]
    base_repo = "destra-imageserver-openslide"
    print(f"\n*****\n***Git diff from {base_repo}.\n*****")
    base_release = os.path.join(DESTRA_ROOT_FOLDER, base_repo, files[0])
    base_renovate = os.path.join(DESTRA_ROOT_FOLDER, base_repo, files[1])

    if ENABLE_DIFF_CREATION:
        # Produce diff for release and renovate
        for repo in repositories:
            # print(f"\nDiff between repo {base_repo} and {repo} =============================")
            # print("\nRELEASE")
            compare_release = os.path.join(DESTRA_ROOT_FOLDER, repo, files[0])
            result = subprocess.run(
                ["diff", base_release, compare_release], stdout=subprocess.PIPE, text=True
            )
            # Save the diff result to a file in temp_folder
            output_file_path = os.path.join(temp_release, repo)
            with open(output_file_path, "w") as output_file:
                output_file.write(result.stdout)

            # print("\nRENOVATE")
            compare_renovate = os.path.join(DESTRA_ROOT_FOLDER, repo, files[1])
            result = subprocess.run(
                ["diff", base_renovate, compare_renovate], stdout=subprocess.PIPE, text=True
            )
            # Save the diff result to a file in temp_folder
            output_file_path = os.path.join(temp_renovate, repo)
            with open(output_file_path, "w") as output_file:
                output_file.write(result.stdout)

    if COMPARE_RENOVATE_DIFF:
        print("\nCompare release files")
        renovate_diff_file = os.path.join(DESTRA_ROOT_FOLDER, temp_renovate, "renovate_example")
        subprocess.run(
            ["cp", os.path.join(temp_renovate, "destra-adapter-calopix"), renovate_diff_file]
        )

        direct_copy = []
        manual_copy = []
        # Iterate over all files in the compare folder
        for compare_file in os.listdir(temp_renovate):
            print(f"Comparing {compare_file} to renovate_example")
            compare_path = os.path.join(temp_renovate, compare_file)

            # Skip directories, process only files
            if os.path.isfile(compare_path):
                # Run the diff command and capture the output
                result = subprocess.run(
                    ["diff", renovate_diff_file, compare_path], stdout=subprocess.PIPE, text=True
                )

                # Print the diff result to the console
                if result.stdout == "":
                    destination_folder = os.path.join(
                        DESTRA_ROOT_FOLDER, compare_path.replace("temp_renovate/", "")
                    )
                    print(
                        f"Copying renovate.rc from {base_renovate} folder directly into {destination_folder}\n"
                    )
                    if ENABLE_OVERRIDING_COPY:
                        subprocess.run(["cp", base_renovate, destination_folder])
                    direct_copy.append(destination_folder)
                else:
                    print(f"Diff result for {compare_file}:")
                    print(result.stdout)
                    destination_folder = os.path.join(
                        DESTRA_ROOT_FOLDER, compare_path.replace("temp_renovate/", "")
                    )
                    manual_copy.append(os.path.join(destination_folder, "renovate.json"))

        pprint(f"OK TO DO DIRECT COPY IN\n{direct_copy}\n\n")
        pprint(f"I SHOULD DO MANUEL COPY IN\n{manual_copy}\n\n")

    if COMPARE_RELEASE_DIFF:
        print("\nCompare release files")
        release_diff_file = os.path.join(DESTRA_ROOT_FOLDER, temp_release, "release_example")
        subprocess.run(
            ["cp", os.path.join(temp_release, "destra-imageserver-philips"), release_diff_file]
        )

        direct_copy = []
        manual_copy = []
        # Iterate over all files in the compare folder
        for compare_file in os.listdir(temp_release):
            print(f"Comparing {compare_file} to release_example")
            compare_path = os.path.join(temp_release, compare_file)

            # Skip directories, process only files
            if os.path.isfile(compare_path):
                # Run the diff command and capture the output
                result = subprocess.run(
                    ["diff", release_diff_file, compare_path], stdout=subprocess.PIPE, text=True
                )

                # Print the diff result to the console
                if result.stdout == "":
                    destination_folder = os.path.join(
                        DESTRA_ROOT_FOLDER, compare_path.replace("temp_release/", "")
                    )
                    print(
                        f"Copying release.rc from {base_release} folder directly into {destination_folder}\n"
                    )
                    if ENABLE_OVERRIDING_COPY:
                        subprocess.run(["cp", base_release, destination_folder])
                    direct_copy.append(destination_folder)
                else:
                    print(f"Diff result for {compare_file}:")
                    print(result.stdout)
                    destination_folder = os.path.join(
                        DESTRA_ROOT_FOLDER, compare_path.replace("temp_release/", "")
                    )
                    manual_copy.append(os.path.join(destination_folder, ".releaserc"))

        pprint(f"OK TO DO DIRECT COPY IN\n{direct_copy}\n\n")
        pprint(f"I SHOULD DO MANUEL COPY IN\n{manual_copy}\n\n")
