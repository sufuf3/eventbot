#!/usr/bin/env python3
# coding=utf-8

import json
import subprocess


class LocalEventHandle():
    def __init__(self, path):
        self.path = path

    def get_event_files(self):
        get_files = subprocess.check_output(
            "du -a " +
            self.path +
            " | grep events.json | awk '{print $2}'",
            shell=True)
        ef_all = []
        for ef in get_files.splitlines():
            try:
                ef_all.append(str(ef).split("'")[1])
            except BaseException:
                ef_all.append(str(ef))
        return(ef_all)

    def get_event_list(self):
        all_files = self.get_event_files()
        local_events = []
        for efile in all_files:
            data = json.load(open(efile))
            num = 0
            for d in data:
                try:
                    if d["location"] is not None:
                        local_events.append({
                            "path": efile,
                            "group_ref":
                                efile.split('TGmeetup/', 1)[1].split('/events.json')[0],
                            "name": d["name"],
                            "datetime":
                                d["local_date"] + "T" + d["local_time"] + ":00.000",
                            "event_num": num
                        })
                except BaseException:
                    local_events.append({
                        "path": efile,
                        "group_ref":
                            efile.split('TGmeetup/', 1)[1].split('/events.json')[0],
                        "name": d["name"],
                        "datetime": d["local_date"] + "T" + d["local_time"] + ".000",
                        "event_num": num
                    })
                num = num + 1
        return local_events

    def get_event_detail(self, event):
        data = json.load(open(event["path"]))
        return data[event["event_num"]]
