import re
from auth_logs import check_regex


def filter_logs(c):
    log_list = c.run("cat /var/log/syslog").stdout.splitlines()
    c.close()
    all_logs = [log for log in log_list]
    docker_logs = [log for log in log_list if "docker" in log]
    systemd_logs = [log for log in log_list if "systemd" in log and "docker" not in log]
    dbus_logs = [log for log in log_list if "dbus-daemon" in log]
    other_logs = [
        log
        for log in log_list
        if "systemd" not in log and "dbus-daemon" not in log and "docker" not in log
    ]
    print("1. Docker Logs\n2. Systemd Logs\n3. Dbus Logs\n4. Other Logs\n5. All Logs")
    command = input("Select a log type: ")
    if command == "1":
        parse_logs(docker_logs, "docker-logs.txt")
    elif command == "2":
        parse_logs(systemd_logs, "systemd-logs.txt")
    elif command == "3":
        parse_logs(dbus_logs, "dbus-logs.txt")
    elif command == "4":
        parse_logs(other_logs, "other-syslogs.txt")
    elif command == "5":
        parse_logs(all_logs, "all-syslogs.txt")
    else:
        print("Invalid input")


def parse_logs(log_list, file_name):
    for log in log_list:
        date = " ".join(log.split()[:3])
        host = " ".join(log.split(" ")[3:4])
        service = "".join(log.split(" ")[4])
        service_message = " ".join(log.split(" ")[5:])

        with open(file_name, "a") as f:
            f.write(
                f"{service}{{\nDate: {date}\nHost: {host}\n Service Message: {service_message}\n}}\n"
            )
