from datetime import datetime


def log_activity(activity):
    try:
        with open("activity_log.txt", "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            file.write(f"[{timestamp}] {activity}\n")

    except OSError as error:
        print("Activity Log Error:", error)


if __name__ == "__main__":
    log_activity("RPMS Activity Logger Started")
    print("Activity Logged Successfully!")