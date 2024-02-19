from fabric import Connection
from auth_logs import logs_menu as auth_logs_menu
from system_logs import filter_logs as sys_logs_filter


def main():
    active = True

    host_name = input("Enter an host:\n")
    while active:
        try:

            command = input(
                "Select a log type:\n"
                "1. Auth Logs\n"
                "2. Syslogs\n"
                "3. Network Logs\n"
                "0. Exit\n"
            )

            with Connection(host_name) as c:
                if command == "1":
                    auth_logs_menu(c)
                elif command == "2":
                    sys_logs_filter(c)
                elif command == "0":
                    active = False
                    c.close()
                    break
                else:
                    print("Connection failed")
        except:
            print("An error occurred")


if __name__ == "__main__":
    main()
