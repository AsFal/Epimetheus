from logs import getLogs, parseLogs, Log, TextLog
from interface import cli

def main():
    logs = getLogs()
    logStringList = parseLogs(logs)
    logsArray = [TextLog(logString) for logString in logStringList]
    cli(logsArray)
    return logsArray

main()