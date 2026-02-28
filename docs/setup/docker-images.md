# Docker images

To deploy this lab, you will need these two Docker images:

- `ceos:image`: This image is required for the Arista cEOS node (`ceos-01`).
- `ghcr.io/nokia/srlinux`: This image is required for both Nokia SR Linux nodes (`srl-01` and `srl-02`).

## Getting Arista cEOS image

To obtain Arista cEOS images:

- Register/Login: Create an account on the [Arista website](https://www.arista.com/en/login).
- Locate Image: Go to the Software Downloads section, select "cEOS-lab", and choose the desired release (this tutorial uses: cEOS-lab-4.35.1F.tar.xz).
- Download: Download the cEOS-lab-xxx.tar.xz file to your local machine.
- Transfer: Move the file to your lab environment (e.g., Ubuntu VM or Docker host) using sftp or scp.
- Import: Import the image into Docker:

```bash
docker import  cEOS-lab-4.35.1F.tar.xz ceos:image
```

## Getting SR Linux image

Nokia SR Linux follows a free and open distribution model. You can pull SR Linux container from a public registry:

```
docker pull ghcr.io/nokia/srlinux
```
