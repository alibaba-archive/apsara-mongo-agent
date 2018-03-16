#! /usr/bin/python
# coding:utf-8


class DeepFilterMap(dict):
    def pick_value(self, arr):
        if isinstance(arr, list):
            tmp = self
            for k in arr:
                if tmp is None:
                    break
                tmp = tmp.get(k, None)
            return tmp
        elif isinstance(arr, str):
            return self.get(arr, None)
        else:
            raise KeyError


if __name__ == '__main__':
    d = {"1": {"2": {"3": "hahaha"}}}
    deepMap = DeepFilterMap(d)
    print deepMap.pick_value(["1", "2", "3"])
    print deepMap.pick_value(["4", "2", "3"])
    print deepMap.pick_value("1")
