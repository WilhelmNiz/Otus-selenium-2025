import os
import re
import json
from collections import defaultdict


def parse_log_line(line):
    """Парсит одну строку лога и возвращает компоненты"""
    pattern = r'^(\S+) \S+ \S+ \[([^\]]+)\] "([A-Z]+) ([^ ]+) HTTP/\d\.\d" (\d+) (\d+) "([^"]*)" "([^"]*)" (\d+)$'
    match = re.match(pattern, line.strip())
    if not match:
        return None

    return {
        'ip': match.group(1),
        'date': match.group(2),
        'method': match.group(3),
        'url': match.group(4),
        'status': int(match.group(5)),
        'bytes': int(match.group(6)),
        'referer': match.group(7),
        'user_agent': match.group(8),
        'duration': int(match.group(9))
    }


def update_top_requests(top_requests, new_request, max_items=3):
    """Обновляет список самых долгих запросов"""
    if len(top_requests) < max_items:
        top_requests.append(new_request)
        top_requests.sort(key=lambda x: x['duration'], reverse=True)
    elif new_request['duration'] > top_requests[-1]['duration']:
        top_requests[-1] = new_request
        top_requests.sort(key=lambda x: x['duration'], reverse=True)
    return top_requests


def parse_log_file(file_path):
    """Анализирует файл лога и возвращает статистику"""
    ip_counts = defaultdict(int)
    method_counts = defaultdict(int)
    top_longest = []
    total_requests = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            total_requests += 1
            parsed = parse_log_line(line)
            if not parsed:
                continue

            ip_counts[parsed['ip']] += 1
            method_counts[parsed['method']] += 1

            request_info = {
                'ip': parsed['ip'],
                'date': f"[{parsed['date']}]",
                'method': parsed['method'],
                'url': parsed['url'],
                'duration': parsed['duration']
            }
            top_longest = update_top_requests(top_longest, request_info)

    top_ips = dict(sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:3])

    stats = {
        'total_requests': total_requests,
        'total_stat': dict(method_counts),
        'top_ips': top_ips,
        'top_longest': top_longest
    }

    return stats


def save_stats(stats, input_path):
    """Сохраняет статистику в JSON файл"""
    output_file = os.path.splitext(input_path)[0] + '_stats.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    return output_file


def print_stats(filename, stats):
    """Выводит статистику в читаемом формате"""
    print(f"\nАнализ файла: {filename}")
    print(f"Общее количество запросов: {stats['total_requests']}")

    print("\nКоличество запросов по методам:")
    for method, count in stats['total_stat'].items():
        print(f"  {method}: {count}")

    print("\nТоп 3 IP по количеству запросов:")
    for ip, count in stats['top_ips'].items():
        print(f"  {ip}: {count}")

    print("\nТоп 3 самых долгих запросов:")
    for i, req in enumerate(stats['top_longest'], 1):
        print(f"  {i}. IP: {req['ip']}")
        print(f"     Метод: {req['method']}")
        print(f"     URL: {req['url']}")
        print(f"     Дата: {req['date']}")
        print(f"     Длительность: {req['duration']} мс")


def process_logs(input_path):
    """Обрабатывает лог-файлы по указанному пути"""
    results = {}

    if os.path.isfile(input_path):
        stats = parse_log_file(input_path)
        results[input_path] = stats
        save_stats(stats, input_path)
        print_stats(input_path, stats)

    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith('.log'):
                file_path = os.path.join(input_path, filename)
                stats = parse_log_file(file_path)
                results[filename] = stats
                save_stats(stats, file_path)
                print_stats(filename, stats)

    return results


def main():
    import sys

    if len(sys.argv) != 2:
        print("Использование: python parse_log.py <файл_лога_или_директория>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.exists(input_path):
        print(f"Ошибка: путь '{input_path}' не существует")
        sys.exit(1)

    process_logs(input_path)


if __name__ == "__main__":
    main()