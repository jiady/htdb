import os
def genConfig():
    dire = os.path.dirname(os.path.realpath(__file__))
    config_raw = open(dire + "/config_raw.private")
    content = ''.join(config_raw.readlines())
    lines = map(lambda x: x.strip(" ;"), content.split(';'))
    config = open(dire + "/config.private", 'w')
    config.write("[cookies]\n")
    for line in lines:
        config.write(line + "\n")
    config.close()

genConfig()