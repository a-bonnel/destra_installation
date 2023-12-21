import os
import subprocess
from pprint import pprint

# Configuration flags
ENABLE_CLONING = False
ENABLE_PULLING = False
ENABLE_BRANCHING = False
ENABLE_INSTALL_PRE_COMMIT = False
ENABLE_DIFF = False
ENABLE_DIFF_CREATION = False
COMPARE_RELEASE_DIFF = False
COMPARE_RENOVATE_DIFF = False
ENABLE_OVERRIDING_COPY = False
ENABLE_GIT_STATUS = False
ENABLE_GIT_COMMIT_PUSH = False
ENABLE_GIT_HARD_RESET = False

DESTRA_FOLDER = "/Users/abonnel/Documents/Destra/"

# List of GitHub repositories to clone
repositories = [
    "destra-chart",
    "destra-docker-images",
    "destra-adapter-filestorage",
    "destra-adapter-internal",
    "destra-imageserver-philips",
    "destra-imageserver-bioformats",
    # "destra-imageserver-openslide",
    # "destra-integration-tests",
    "destra-common",
    "destra-imageserver-openslide-py",
    "destra-adapter-sectra",
    "destra-dispatcher",
    "destra-worker",
    "destra-adapter-roche",
    "destra-adapter-calopix",
]

print("==========================================================")
print("This script is meant to perform actions on all Destra repositories")
print(f"Repos will be cloned in {DESTRA_FOLDER} folder")
print("List of repositories :")
for repo in repositories:
    print(repo)
print("==========================================================")

# Create folder if it does not exist
if os.path.isdir(DESTRA_FOLDER):
    print(f"The path '{DESTRA_FOLDER}' already exists.")
else:
    print(f"The path '{DESTRA_FOLDER}' does not exist and will be created.")
    os.makedirs(DESTRA_FOLDER, exist_ok=True)

if ENABLE_CLONING:
    # # Clone each repository into DESTRA_FOLDER
    print(f"\n*****\n***TASK : Cloning in {os.getcwd()} and install pre-commit.\n*****")
    for repo in repositories:
        os.chdir(DESTRA_FOLDER)
        if os.path.isdir(repo):
            print(f"The repo '{repo}' has already been cloned.")
        else:
            print(f"\nThe path '{repo}' does not exist and will be created.=======")
            subprocess.run(["git", "clone", f"git@github.com:owkin/{repo}.git"])
            if ENABLE_INSTALL_PRE_COMMIT:
                # Install pre-commit
                os.chdir(os.path.join(DESTRA_FOLDER, repo))
                # subprocess.run(["pre-commit", "autoupdate"])
                subprocess.run(["pre-commit", "install"])
    print("Cloning completed.")

if ENABLE_PULLING:
    # # Git pull on all repos
    print(f"\n*****\n***Git pull on destra repos in {os.getcwd()}.\n*****")
    for repo in repositories:
        print(
            f"\nPulling in repo {repo} at {os.path.join(DESTRA_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_FOLDER, repo))
        subprocess.run(["git", "pull"])

if ENABLE_BRANCHING:
    # # Git pull on all repos
    print(f"\n*****\n***Git branch on destra repos in {os.getcwd()}.\n*****")
    branch_name = "abo/pre-commit"
    for repo in repositories:
        print(
            f"\nCreating branch {branch_name} in repo {repo} at {os.path.join(DESTRA_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_FOLDER, repo))
        subprocess.run(["git", "switch", "-c", branch_name])

if ENABLE_DIFF:
    # Git diff
    os.chdir(DESTRA_FOLDER)

    # Make temp folders
    temp_renovate = os.path.join(DESTRA_FOLDER, "temp_renovate")
    temp_release = os.path.join(DESTRA_FOLDER, "temp_release")
    os.makedirs(temp_renovate, exist_ok=True)
    os.makedirs(temp_release, exist_ok=True)

    files = [".releaserc", "renovate.json"]
    base_repo = "destra-imageserver-openslide"
    print(f"\n*****\n***Git diff from {base_repo}.\n*****")
    base_release = os.path.join(DESTRA_FOLDER, base_repo, files[0])
    base_renovate = os.path.join(DESTRA_FOLDER, base_repo, files[1])

    if ENABLE_DIFF_CREATION:
        # Produce diff for release and renovate
        for repo in repositories:
            # print(f"\nDiff between repo {base_repo} and {repo} =============================")
            # print("\nRELEASE")
            compare_release = os.path.join(DESTRA_FOLDER, repo, files[0])
            result = subprocess.run(
                ["diff", base_release, compare_release], stdout=subprocess.PIPE, text=True
            )
            # Save the diff result to a file in temp_folder
            output_file_path = os.path.join(temp_release, repo)
            with open(output_file_path, "w") as output_file:
                output_file.write(result.stdout)

            # print("\nRENOVATE")
            compare_renovate = os.path.join(DESTRA_FOLDER, repo, files[1])
            result = subprocess.run(
                ["diff", base_renovate, compare_renovate], stdout=subprocess.PIPE, text=True
            )
            # Save the diff result to a file in temp_folder
            output_file_path = os.path.join(temp_renovate, repo)
            with open(output_file_path, "w") as output_file:
                output_file.write(result.stdout)

    if COMPARE_RENOVATE_DIFF:
        print("\nCompare release files")
        renovate_diff_file = os.path.join(DESTRA_FOLDER, temp_renovate, "renovate_example")
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
                        DESTRA_FOLDER, compare_path.replace("temp_renovate/", "")
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
                        DESTRA_FOLDER, compare_path.replace("temp_renovate/", "")
                    )
                    manual_copy.append(os.path.join(destination_folder, "renovate.json"))

        pprint(f"I SHOULD HAVE UPDATED IN\n{direct_copy}\n\n")
        #  "'/Users/abonnel/Documents/Destra/destra-adapter-calopix', "
        #  "'/Users/abonnel/Documents/Destra/destra-adapter-roche', "
        #  "'/Users/abonnel/Documents/Destra/destra-dispatcher', "
        #  "'/Users/abonnel/Documents/Destra/destra-adapter-sectra']\n"
        #  "'/Users/abonnel/Documents/Destra/destra-adapter-internal', "
        #  "'/Users/abonnel/Documents/Destra/destra-adapter-filestorage', "

        pprint(f"I SHOULD DO MANUEL COPY IN\n{manual_copy}\n\n")
    #  "'/Users/abonnel/Documents/Destra/destra-docker-images/renovate.json', "
    #  "'/Users/abonnel/Documents/Destra/destra-imageserver-philips/renovate.json', "
    #  "'/Users/abonnel/Documents/Destra/destra-imageserver-bioformats/renovate.json', "
    #  "'/Users/abonnel/Documents/Destra/destra-common/renovate.json', "
    #  "['/Users/abonnel/Documents/Destra/destra-imageserver-openslide-py/renovate.json', "
    #  "'/Users/abonnel/Documents/Destra/destra-worker/renovate.json', "

    #  "'/Users/abonnel/Documents/Destra/destra-chart/renovate.json']\n"

    if COMPARE_RELEASE_DIFF:
        print("\nCompare release files")
        release_diff_file = os.path.join(DESTRA_FOLDER, temp_release, "release_example")
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
                        DESTRA_FOLDER, compare_path.replace("temp_release/", "")
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
                        DESTRA_FOLDER, compare_path.replace("temp_release/", "")
                    )
                    manual_copy.append(os.path.join(destination_folder, ".releaserc"))
        # for folder in direct_copy:
        pprint(f"I SHOULD HAVE UPDATED IN\n{direct_copy}\n\n")
        # destra-adapter-internal
        # destra-adapter-calopix
        # destra-dispatcher
        # destra-imageserver-philips
        # destra-adapter-roche
        # destra-adapter-filestoragec
        # destra-adapter-sectra

        pprint(f"I SHOULD DO MANUEL COPY IN\n{manual_copy}\n\n")
        #  "['/Users/abonnel/Documents/Destra/destra-imageserver-openslide-py/.releaserc', "
        #  "'/Users/abonnel/Documents/Destra/destra-docker-images/.releaserc', "
        #  "'/Users/abonnel/Documents/Destra/destra-imageserver-bioformats/.releaserc', "
        #  "'/Users/abonnel/Documents/Destra/destra-worker/.releaserc', "
        #  "'/Users/abonnel/Documents/Destra/destra-common/.releaserc', "
        #  "'/Users/abonnel/Documents/Destra/destra-chart/.releaserc']\n"

if ENABLE_GIT_STATUS:
    # # Git pull on all repos
    print(f"\n*****\n***Git status on destra repos in {os.getcwd()}.\n*****")
    for repo in repositories:
        print(
            f"\nGit status in repo {repo} at {os.path.join(DESTRA_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_FOLDER, repo))
        subprocess.run(["git", "status"])

if ENABLE_GIT_COMMIT_PUSH:
    for repo in repositories:
        print(
            f"\nGit status in repo {repo} at {os.path.join(DESTRA_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_FOLDER, repo))
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "status"])
        subprocess.run(["git", "commit", "-m", "Renovate file update"])
        subprocess.run(["git", "push", "--set-upstream", "origin", "abo/pre-commit"])


if ENABLE_GIT_HARD_RESET:
    # # Git pull on all repos
    print(f"\n*****\n***Git pull on destra repos in {os.getcwd()}.\n*****")
    for repo in repositories:
        print(
            f"\nGit status in repo {repo} at {os.path.join(DESTRA_FOLDER, repo)} ==================="
        )
        os.chdir(os.path.join(DESTRA_FOLDER, repo))
        subprocess.run(["git", "reset", "--hard", "HEAD"])
