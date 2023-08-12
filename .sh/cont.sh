docker run --gpus all -it -v .:/v2en --cap-add=NET_ADMIN --network="bridge" -p 2564:2564 -e TZ=Asia/Ho_Chi_Minh -m 8G nvietuk/v2en:latest
