from logs import getLogs, parseLogs, Log, TextLog, LogList
from interface import cli

def main():
    logs = getLogs()
    logStringList = parseLogs(logs)
    logList = LogList(logs=[TextLog(logString).toTreeLog() for logString in logStringList])
    cli(logList)

main()