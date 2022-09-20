# Example of tweets search using marqo package

Before running the app assuming that **python 3.8.xx** is installed on development machine

1. Run the marko docker 
```shell
docker rm -f marqo;docker run --name marqo -it --privileged -p 8882:8882 --add-host host.docker.internal:host-gateway marqoai/marqo:0.0.3
```
2.Create virtual environment with python3.8.xx and run the margo docker
```shell
python3.8 -m venv env
```
3.Activate the virtual environment
```shell
source env/bin/activate
```
4.Install requisite packages:
```shell
pip install -r requirements.txt
```

5.Populate the margo index first
```shell
python twitter_search.py --populate-index
```

6.Search using query from margo index
```shell
python twitter_search.py --query "bitcoin"
```