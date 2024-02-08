sudo dnf reinstall container-selinux

sudo chcon -Rt container_file_t $HOME/.local/share/containers/storage

cd docker/python && podman build -t home-app-python .

podman-compose up
podman generate systemd --new --files --name home-db
mkdir -p ~/.config/systemd/user/
cp -Z container-home-db.service ~/.config/systemd/user/
podman stop home-db && podman rm -a && podman volume prune
systemctl --user daemon-reload