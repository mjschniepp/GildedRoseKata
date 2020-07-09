# -*- coding: utf-8 -*-
import bisect

class GildedRose(object):
    maxQuality = 50
    minQuality = 0
    backstageIntervals = [0, 5, 10]
    ratePre = 1
    ratePost = 2
    conjRatePre = ratePre*2
    conjRatePost = ratePost*2

    def __init__(self, items):
        self.items = items # items is a list of Item objects

    def update_sell_in(self, item):
        item.sell_in -= 1

    def update_by_category(self, item):
        # crude string parse to get item category
        # handles one of 5 cases
        name = item.name.lower()
        if "sulfuras" in name:
            self.update_sulfuras(item)
        elif "backstage" in name:
            self.update_backstage(item)
        elif "aged brie" in name:
            self.update_basic(item, 'inc', self.ratePre, self.ratePost)
        elif "conjured" in name:
            self.update_basic(item, 'dec', self.conjRatePre, self.conjRatePost)
        else:
            self.update_basic(item, 'dec', self.ratePre, self.ratePost)

    def decrement_quality(self, item, val):
        # decrease quality by val; prevents going below 0
        stageUpdateVal = item.quality - val
        if stageUpdateVal < self.minQuality:
            item.quality = self.minQuality
        else:
            item.quality -= val

    def increment_quality(self, item, val):
        # increase quality by val; prevents going over 50
        stageUpdateVal = item.quality + val
        if stageUpdateVal > self.maxQuality:
            item.quality = self.maxQuality
        else:
            item.quality += val

    def update_basic(self, item, direction, rate_pre, rate_post):
        # update quality based on increasing/decreasing and sell_in val
        if direction == 'inc':
            if item.sell_in <= 0:
                self.increment_quality(item, rate_post)
            else:
                self.increment_quality(item, rate_pre)
        elif direction == 'dec':
            if item.sell_in <= 0:
                self.decrement_quality(item, rate_post)
            else:
                self.decrement_quality(item, rate_pre)
        # update sell_in
        self.update_sell_in(item)

    def update_backstage(self, item):
        # update quality based on sell_in's place in defined intervals
        intvl = self.backstageIntervals
        if bisect.bisect_left(intvl, item.sell_in) == 0:
            item.quality = 0
        elif bisect.bisect_left(intvl, item.sell_in) == 1:
            self.increment_quality(item, 3)
        elif bisect.bisect_left(intvl, item.sell_in) == 2:
            self.increment_quality(item, 2)
        elif bisect.bisect_left(intvl, item.sell_in) == 3:
            self.increment_quality(item, 1)
        # update sell_in
        self.update_sell_in(item)

    def update_sulfuras(self, item):
        # No action required for Sulfuras
        pass

    def update_quality(self):
        # update quality of all items
        for item in self.items:
            self.update_by_category(item)

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
