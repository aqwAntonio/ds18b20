exit
db_status=$(podman inspect home-db --format "{{.State.Status}}")
if [[ $db_status != "running" ]]
then
	podman start home-db
	sleep 10
	podman start home-python
else
	podman start home-python
fi
