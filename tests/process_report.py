import subprocess
from collections import defaultdict
from datetime import datetime

from redis.cluster import command


def main():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Не удалось выполнить ps: {e}")

    lines = output.split("\n")[1:]

    user_processes = defaultdict(int)
    total_memory = 0.0
    total_cpu = 0.0
    max_mem_process = {"memory": 0, "name": ""}
    max_cpu_process = {"cpu": 0, "name": ""}
    users = set()

    for line in lines:
        if not line.split():
            continue

        parts = line.split()

        try:
            user = parts[0]
            cpu = float(parts[2])
            mem = float(parts[3])
            command = " ".join(parts[10:])

            users.add(user)
            user_processes[user] += 1
            total_memory += mem
            total_cpu += cpu

            if mem > max_mem_process["memory"]:
                max_mem_process["memory"] = mem
                max_mem_process["name"] = command[:20]

            if cpu > max_cpu_process["cpu"]:
                max_cpu_process["cpu"] = cpu
                max_cpu_process["name"] = command[:20]

        except (IndexError, ValueError) as e:
            raise ValueError(f"Ошибка при обработке строки: {line}\nОшибка: {e}")

    report = f"""
    Отчёт о состоянии системы:
    Пользователи системы: {', '.join(sorted(users))}
    Процессов запущено: {len(lines)}

    Пользовательских процессов:"""

    for user, count in sorted(user_processes.items(), key=lambda x: x[1], reverse=True):
        report += f"\n{user}: {count}"

    report += f"""

    Всего памяти используется: {total_memory:.1f}%
    Всего CPU используется: {total_cpu:.1f}%
    Больше всего памяти использует: {max_mem_process['name']} ({max_mem_process['memory']:.1f}%)
    Больше всего CPU использует: {max_cpu_process['name']} ({max_cpu_process['cpu']:.1f}%)
    """

    print(report)

    filename = datetime.now().strftime("%d-%m-%Y-%H:%M") + "-scan.txt"
    try:
        with open(filename, "w") as f:
            f.write(report)
        print(f"Отчёт сохранён в файл: {filename}")
    except IOError as e:
        raise IOError (f"Ошибка при сохранении отчёта: {e}")

if __name__ == "__main__":
    main()

