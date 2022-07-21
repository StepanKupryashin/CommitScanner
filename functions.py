#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from dateutil.parser import *
import codecs
import sys
def get_path_file():
    if len(sys.argv) < 2:
        return "test_data_commits.log"
    else:
        return sys.argv[1] 

def get_commits_info(file):
    commits = {}
    while True:
        line = file.readline()
        if not line: break
        if line.startswith("revno:"):
            rev_number = int(line.replace("revno:", "").replace("[merge]", "").strip())
        elif line.startswith("committer:"):
            committer = line.replace("committer:", "").strip()
        elif line.startswith("timestamp:"):
            timestamp = line.replace("timestamp:", "").strip()
        else:
            commits[rev_number] = { "user" : committer, "date" : timestamp}
    file.close()
    return commits

def get_stats_commits(commits):
    stats_of_commits = {}
    for i in commits.values():
        if i['user'] not in stats_of_commits:
            stats_of_commits[i['user']] = {"count" : 0}
        stats_of_commits[i['user']]["count"] += 1 
        year = parse(i['date']).year
        if year not in stats_of_commits[i['user']]:
            stats_of_commits[i['user']][year] = {}
        month = parse(i['date']).month
        if month not in stats_of_commits[i['user']][year]:
            stats_of_commits[i['user']][year][month] = 0
        stats_of_commits[i['user']][year][month] += 1
    return stats_of_commits

def get_stats_of_yaer(year, dict):
    stats = {"total" : 0}
    for i in dict:
        stats[i] = {}
        stats[i]["count"] = 0
        if year in dict[i]:
            for j in dict[i][year].values():
                stats[i]["count"] += j
        else: stats[i]["count"] = 0
    # подсчет общего кол-ва:
    for i in stats:
        if i == "total": continue
        stats["total"] += stats[i]["count"]
    return stats

def write_stats_of_all_time(dict, total_commits):
    file = codecs.open('result.txt', 'a', "utf-8")
    print(u"Список коммитов за всё время")
    file.write(u"Список коммитов за всё время")
    for i in dict:
        print(u"Комитер: %s, кол-во коммитов: %s, процент от общего кол-ва: %s" % (i, dict[i]['count'], round(float(dict[i]['count']) / float(total_commits) * 100, 2)))
        file.write(u"\n\nКомитер: %s, кол-во коммитов: %s, процент от общего кол-ва: %s" % (i, dict[i]['count'], round(float(dict[i]['count']) / float(total_commits) * 100, 2)))
    file.close()
    
    
def write_stats_of_years(dict):
    readed_years = []
    file = codecs.open('result.txt', 'a', "utf-8")
    for i in dict:
        for year in dict[i]:
            if year == "count": continue
            if year in readed_years: continue
            readed_years.append(year)
            stats = get_stats_of_yaer(year, dict)
            print(u"Список по %s году(всего коммитов: %s):\n" % (year, stats["total"]))
            file.write(u"\nСписок по %s году(всего коммитов: %s):\n" % (year, stats["total"]))
            for i in stats:
                if i == "total": continue
                print(u"Комитер: %s, кол-во коммитов: %s, процент от общего кол-ва: %s" % (i, stats[i]["count"], round(float(stats[i]["count"]) / float(stats["total"]) * 100, 2 )))
                file.write(u"Комитер: %s, кол-во коммитов: %s, процент от общего кол-ва: %s\n" % (i, stats[i]["count"], round(float(stats[i]["count"]) / float(stats["total"]) * 100, 2 )))
    file.close()

def get_last_date(dict):
    for i in dict.values():
        try:
            if last_date < parse(i["date"]).date():
                last_date = parse(i["date"]).date()
        except NameError:
            last_date = parse(i["date"]).date()
    return last_date
            
    
def write_stats_of_last_months(commits, dict):
    last_date = get_last_date(commits)
    file = codecs.open("result.txt", "a", "utf-8")
    stats = {"total": 0}
    for i in dict: 
        for year in dict[i]:
            if year == "count": continue
            for month in dict[i][year]:
                cur_date = parse("%s-%s-01" % (year, month)).date()
                diff = last_date - cur_date
                if diff.days <= 92:
                    if i not in stats:
                        stats[i] = {}
                        stats[i]["count"] = 0
                    stats[i]["count"] += 1
                    stats["total"] += 1
    print(u"Список коммитов за последние 3 месяца:")
    file.write(u"\nСписок коммитов за последние 3 месяца:")
    for i in stats:
        if i == "total": continue
        print(u"Комитер: %s, кол-во коммитов: %s, процент от общего кол-ва: %s" % (i, stats[i]["count"], round(float(stats[i]["count"]) / float(stats["total"]) * 100, 2 )))
        file.write(u"\nКомитер: %s, кол-во коммитов: %s, процент от общего кол-ва: %s" % (i, stats[i]["count"], round(float(stats[i]["count"]) / float(stats["total"]) * 100, 2 )))
    file.close()