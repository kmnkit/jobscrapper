import csv


def save_to_file(jobs, job_name):
    file = open(f"{job_name}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company"])
    for job in jobs:
        writer.writerow(list(job.values())[0:-1])
    return
