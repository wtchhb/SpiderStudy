# -*- coding: utf-8 -*-
from csv import DictWriter
import os

from qidian.items import *


class QidianPipeline(object):
    def __init__(self):
        self.book_csv = 'book.csv'
        self.juan_csv = 'juan.csv'
        self.seg_csv = 'segs.csv'

    def save_csv(self, item, filename):
        has_header = os.path.exists(filename)
        with open(filename, 'a') as f:
            writer = DictWriter(f, fieldnames=item.keys())
            if not has_header:
                writer.writeheader()
            writer.writerow(item)

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            self.save_csv(item, self.book_csv)

        elif isinstance(item, JuanItem):
            self.save_csv(item, self.juan_csv)

        return item
