#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# @Author: KevinMidboe
# @Date:   2017-10-02 16:29:25
# @Last Modified by:   KevinMidboe
# @Last Modified time: 2017-10-02 18:07:26

import itertools, os
import multiprocessing

def worker(filename):
    print(filename)

def main():
    with multiprocessing.Pool(48) as Pool: # pool of 48 processes

        walk = os.walk("/Volumes/mainframe/shows/")
        fn_gen = itertools.chain.from_iterable((os.path.join(root, file)
                                                for file in files)
                                               for root, dirs, files in walk)

        results_of_work = Pool.map(worker, fn_gen) # this does the parallel processing

if __name__ == '__main__':
    main()