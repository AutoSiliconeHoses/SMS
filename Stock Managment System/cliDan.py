import sys, string, os, yaml
import Client.client as client

with open("config.yml", 'r') as cfg:
    config = yaml.load(cfg, Loader=yaml.FullLoader)

client.runClient("192.168.1.110")
