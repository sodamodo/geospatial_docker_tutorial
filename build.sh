# Look up how to launch docker if not running ``

docker build -t backend ./backend/.
docker run -it --network=host backend
