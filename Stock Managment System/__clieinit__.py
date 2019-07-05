import sys, string, os, yaml
sys.path.insert(0, "Client/")
import client

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

client.runClient()
