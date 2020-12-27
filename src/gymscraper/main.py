from .controller import loadConfig, parseTarget


def main():
    config = loadConfig()

    if not config:
        exit(-1)

    outputDir = config["outputDir"]
    targets = config["targets"]

    for target in targets:
        parseTarget(target, outputDir)
