cat /home/hayasaka/.ssh/id_rsa.pub >> id_rsa.pub
export DOCKER_BUILDKIT=1 && docker image build --build-arg user=$USER -t nvietuk/v2en:latest .
rm id_rsa.pub