from logs import getLogs, parseLogs, Log
from interface import cli

def main():
    logs = getLogs()
    logStringList = parseLogs(logs)
    logsArray = [Log(logString) for logString in logStringList]
    cli(logsArray)
    return logsArray

main()