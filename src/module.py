from injector import Module

from src.crawler import Crawler


class BanJinroLogCrawlerModule(Module):
    def configure(self, binder):
        binder.bind(Crawler)
