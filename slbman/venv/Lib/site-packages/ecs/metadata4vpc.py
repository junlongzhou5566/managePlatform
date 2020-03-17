#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A tool to get meta for aliyun ecs.
"""
__authors__ = 'teachmyself@126.com'
__license__ = 'MIT License'
__version__ = '0.0.4'

import os
import sys
import platform

import logging
import ConfigParser
import argparse

import json
import requests


log_format = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def set_logging(log_level=40):
    """
    Set logging level.
    """
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(log_format)

    logger.addHandler(ch)

def exists(path, isdir=False):
    """
    Check if file or directory is exists when initialized, if not then create
    it.
    """
    if os.path.exists(path):
        return True
    else:
        if isdir == True:
            logger.debug("Directory %s is not exists, creating it.", path)
            os.makedirs(path)
        else:
            logger.debug("File %s is not exists, creating it.", path)
            with open(path, "wb") as fp:
                fp.write("")


class Metadata4vpc(object):
    """
    Metadata for aliyun ecs
    """
    url4vpc = os.getenv("URL4VPC", "http://100.100.100.200/latest/meta-data")

    def __init__(self, log_level=40, url4vpc=""):
        """
        Initialize metadata config file and parser.
        """
        set_logging(log_level)

        home = os.getenv("HOME", ".")
        self.aliyun = os.getenv("ALIYUN", os.path.join(home, ".aliyun"))

        self.ini = os.path.join(self.aliyun, "config.ini")
        self.ecs_dir = os.path.join(self.aliyun, "ecs")
        self.instanceid_file = os.path.join(self.aliyun, "ecs/instance-id")
        self.network_file = os.path.join(self.aliyun, "ecs/network-type")

        self.url4vpc = Metadata4vpc.url4vpc if url4vpc == "" else url4vpc

        exists(self.ecs_dir, isdir=True)
        exists(self.ini)
        exists(self.instanceid_file)
        exists(self.network_file)

        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.ini)

    def has_section(self, section="ecs"):
        """
        Check if "ecs" section is in config file. (not used yet)
        """
        c = self.conf
        ini = self.ini
        if c.has_section(section) == False:
            logger.debug("Section %s is not exists, adding to %s", section, ini)
            with open(ini, "wb") as fp:
                c.add_section(section)
                c.write(fp)


    def set(self, item, value, section="ecs"):
        """
        Set a item in config file. (not used yet)
        """
        logger.debug("set %s as %s in section %s", item, value, section)
        c = self.conf
        ini = self.ini
        with open(ini, "wb") as fp:
            c.set(section, item, value)
            c.write(fp)


    def get(self, item, section="ecs"):
        """
        Get a item fromn config file. (not used yet)
        """
        logger.debug("get %s in section %s", item, section)
        return self.conf.get(section, item)


    def metadata4vpc_item(self, item, url="", timeout=3):
        """
        Get metadata value of specified item.
        """
        url = os.path.join(self.url4vpc, item)
        localfiles = ["instance-id", "network-type"]
        logger.debug("Requesting url %s.", url)

        res = requests.get(url, timeout=timeout).content.split("\r\n")
        if len(res) == 1:
            if item in localfiles:
                localfile = os.path.join(self.aliyun, "ecs", item)
                if os.path.getsize(localfile) == 0:
                    logger.debug("File %s is empty initializing", localfile)
                    with open(localfile, "wb") as handler:
                        handler.write(res[0])
            return res[0]
        return res


    def metadata4vpc(self, timeout=3, item="", fmt=""):
        """
        Get metadata information of current aliyun ecs in vpc. (ecs in aliyun
        vpc only)
        """
        if item:
            return self.metadata4vpc_item(item=item, timeout=timeout)
        else:
            metadata = {}
            res = requests.get(self.url4vpc, timeout=timeout)
            metadata_items = res.content.split("\n")
            for k in metadata_items:
                res = self.metadata4vpc_item(item=k, timeout=timeout)
                if k.endswith("/"):
                    k = k.replace("/", "")
                    sub_items = res.split("\n")
                    metadata[k] = {}
                    for sub_item in sub_items:
                        sub_item_url = os.path.join(k, sub_item)
                        sub_res = self.metadata4vpc(item=sub_item_url)
                        metadata[k][sub_item] = sub_res
                else:
                    metadata[k] = res
            if fmt == "json":
                return json.dumps(metadata)
            return metadata


    def instanceid(self, timeout=3):
        """
        Get the instanceid of current aliyun ecs in vpc. (ecs in aliyun
        vpc only)
        """
        instanceid_file = self.instanceid_file
        if os.path.getsize(instanceid_file) == 0:
            return self.metadata4vpc(item="instance-id", timeout=timeout)
        return open(instanceid_file, "r").read()


    def ls(self, item="", fmt=""):
        """
        Show main metadata information of current aliyun ecs in vpc on the
        console.
        """
        if item == "":
            res = self.metadata4vpc()
            if fmt == "json":
                print json.dumps(res)
            else:
                item_len = len(max(res.keys(), key=len)) + 2
                value_len = len(max(res.values(), key=len)) + 2
                print 'Name'.center(item_len, '-'), 'Metadata'.center(value_len, '-')
                for k in res:
                    if isinstance(res[k], str):
                        key = ''.join([k, ':'])
                        print key.rjust(item_len, ' '),
                        if res[k] == "":
                            print None
                        else:
                            print res[k].ljust(value_len, ' ')
                print "-" * (item_len + value_len + 1)
        else:
            print self.metadata4vpc(item=item)


def update_motd():
    """
    Set update-motd for ecs in vpc.
    """
    motd_file = "/etc/update-motd.d/99-metadata4vpc"
    content = """#!/bin/bash
$(which ecs-metadata4vpc)"""

    dist, release, codename = platform.dist()
    if dist != "Ubuntu":
        print "This is not a Ubuntu distribution, %s %s %s" % (dist, release, codename)
        sys.exit(1)
    with open(motd_file, 'wb') as fhandler:
        fhandler.write(content)
    os.chmod(motd_file, 666)
    os.system("run-parts /etc/update-motd.d/")
    sys.exit(0)


def main(log_level=40):
    """
    Main function for class Metadata instance to used in command line.
    """

    def process_args(argv):
        """
        Arguments processor for command line.
        """
        parser = argparse.ArgumentParser(
            version=" ".join(["%(prog)s", __version__]),
            description="Get metadata of current aliyun ecs in vpc. (ecs in aliyun vpc only) ")
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-a", "--all", action="store_true", dest="all", default=False,
            help="show all metadata of current ecs")

        group.add_argument(
            "-i", "--instanceid", action="store_const", dest="item", const="instance-id",
            help="show instanceid of current ecs")
        group.add_argument(
            "-n", "--network", action="store_const", dest="item", const="network-type",
            help="show network type of current ecs")
        group.add_argument(
            "-e", "--eip", action="store_const", dest="item", const="eipv4",
            help="show eip binded on current ecs")
        group.add_argument(
            "-p", "--privateip", action="store_const", dest="item", const="private-ipv4",
            help="show privateid of current ecs")
        group.add_argument(
            "-V", "--vpc", action="store_const", dest="item", const="vpc-id",
            help="show vpcid of current ecs")
        group.add_argument(
            "-s", "--vswitch", action="store_const", dest="item", const="vswitch-id",
            help="show vswitchid of current ecs")
        group.add_argument(
            "-S", "--vswitch-block", action="store_const", dest="item", const="vswitch-cidr-block",
            help="show vswitch-cidr-block of current ecs")
        group.add_argument(
            "-z", "--zoneid", action="store_const", dest="item",
            const="zone-id", help="show zoneid of current ecs")

        parser.add_argument(
            "-j", "--json", action="store_const", dest="format", const="json",
            help="""show metadata by json format (works with -a option only, and
                can be pretty by 'python -m json.tool')""")
        parser.add_argument(
            "-D", "--debug", action="store_const", dest="log_level",
            const=logging.DEBUG, help="show debug information (set logging as logging.DEBUG)")

        parser.add_argument(
            "-m", "--motd", action="store_true", dest="motd",
            help="Set metadata of vpc as message of today.")

        return parser.parse_args(argv)


    argv_len = len(sys.argv[1:])
    if argv_len == 0:
        results = process_args(["-a"])
    else:
        results = process_args(sys.argv[1:])

    if results.log_level:
        log_level = results.log_level

    e = Metadata4vpc(log_level)
    if results.all == True:
        e.ls(fmt=results.format)
    if results.item:
        e.ls(item=results.item)
    if results.motd:
        update_motd()
    sys.exit(0)


if __name__ == "__main__":
    main()
