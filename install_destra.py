import os

# List of GitHub repositories to clone
repositories = [
	"git@github.com:owkin/destra-chart.git",
	"git@github.com:owkin/destra-docker-images.git",
	"git@github.com:owkin/destra-adapter-filestorage.git",
	"git@github.com:owkin/destra-adapter-internal.git",
	"git@github.com:owkin/destra-imageserver-philips.git",
	"git@github.com:owkin/destra-imageserver-bioformats.git",
	"git@github.com:owkin/destra-imageserver-openslide.git",
	"git@github.com:owkin/destra-integration-tests.git",
	"git@github.com:owkin/destra-common.git",
	"git@github.com:owkin/destra-imageserver-openslide-py.git",
	"git@github.com:owkin/destra-adapter-sectra.git",
	"git@github.com:owkin/destra-dispatcher.git",
	"git@github.com:owkin/destra-worker.git",
	"git@github.com:owkin/destra-adapter-roche.git",
	"git@github.com:owkin/destra-adapter-calopix.git",
]

# Clone each repository
for repo in repositories:
	os.system(f"git clone {repo}")

print("Cloning completed.")

