#! /usr/bin/env python
# -*- coding: utf-8 -*-
from functions import *
import sys
 
def main(file):
    commits = get_commits_info(file)

    stats_of_commits = get_stats_commits(commits)
                
    # вывод статистики за все время
    write_stats_of_all_time(stats_of_commits, len(commits))

    # вывод статистики по годам
    write_stats_of_years(stats_of_commits)
    
    # вывод статистики за последние три месяца относительно последнего коммита
    write_stats_of_last_months(commits, stats_of_commits)

if __name__ == '__main__':
    path = get_path_file()
    file = open(path, mode='r')
    main(file)