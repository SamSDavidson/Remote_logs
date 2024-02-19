import re


def logs_menu(c):
    result = c.run("cat /var/log/auth.log")
    standard_out = result.stdout.strip()
    c.close()
    log_list = standard_out.split("\n")
    selection = input(
        "Select a log type from auth.log:\n"
        "1. SSH Logs\n"
        "2. Systemd Logs\n"
        "3. Cron Logs\n"
        "4. All Logs\n"
        "Enter your selection: "
    )
    if selection == "1":
        filter_logs(log_list, "sshd")
    elif selection == "2":
        filter_logs(log_list, "systemd")
    elif selection == "3":
        filter_logs(log_list, "CRON")
    elif selection == "4":
        filter_logs(log_list)
    else:
        print("Invalid selection")
        logs_menu(c)


def filter_logs(log_list, filter=None):
    if filter:
        filtered_logs = [[log] for log in log_list if filter in log]
        parse_logs(filtered_logs, f"{filter}.txt")
    else:
        filtered_logs = [[log] for log in log_list]
        parse_logs(filtered_logs)


def parse_logs(logs, filter="auth.txt"):

    for log in logs:
        log = log[0]
        date = ""
        host = ""
        service_id = ""
        service_message = ""
        session_status = "N/A"
        ip_address = "N/A"
        access_user = "N/A"
        try:
            # Retrieve specifiv calues from the log
            date = " ".join(log.split()[:3])
            host = str.join(host + " ", log.split(" ")[3:4])

            # Select only the numeric value from the ID
            service = " ".join(log.split(" ")[4])

            s_id = re.search(r"\d+", service)
            service_id = check_regex(s_id)

            s_type = re.search(r"\w+", service)
            service_type = check_regex(s_type)

            # Get the rest of the log as a message
            service_message = log.split(" ")[5:]
            display_message = " ".join(service_message)

            for line in service_message:
                match line:
                    case line if re.search(r"opened", line):
                        session_status = "session opened"
                        continue
                    case line if re.search(r"closed", line):
                        session_status = "session closed"
                        continue
                    case line if re.search(r"Accepted", line):
                        session_status = "Key Accepted"
                        continue
                    case line if re.search(r"Declined", line):
                        session_status = "Key Declined"
                        continue
                    case line if (uid_match := re.search(r"(?<=uid=)(\d+)", line)):
                        access_user = uid_match.group(1)
                        break
                    case line if re.search(r"\d+\.\d+\.\d+\.\d+", line):
                        ip_address = line
                        continue

                write_string = f"{service_id}:{{ \n Session Type: {service_type},\n Full Details: {display_message},\n Date: {date}\n"
                if access_user != "N/A":
                    write_string += f"User: {access_user},\n"
                if ip_address != "N/A":
                    write_string += f"IP: {ip_address},\n"
                if session_status != "N/A":
                    write_string += f"Session Status: {session_status},\n"
                write_string += "}\n\n"

                with open(f'{host}_{filter}', "a") as f:
                    f.write(write_string)

        except:
            print("An error occurred collecting the log")
            break


def check_regex(search, args=None):
    if search:
        if args:
            return search.group(args)
        else:
            return search.group()
    else:
        return "N/A"
