# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""

import argparse
import string
import time
from datetime import datetime 
from function.search import Search
from utils.spider_controller import Controller
from utils.config import global_config
from utils.logger import logger
from utils.spider_config import spider_config

parser = argparse.ArgumentParser()

parser.add_argument('--normal', type=int, required=False, default=1,
                    help='spider as normal(search->detail->review)')
parser.add_argument('--detail', type=int, required=False, default=0,
                    help='spider as custom(just detail)')
parser.add_argument('--review', type=int, required=False, default=0,
                    help='spider as custom(just review)')
parser.add_argument('--shop_id', type=str, required=False, default='',
                    help='custom shop id')
parser.add_argument('--need_more', type=bool, required=False, default=False,
                    help='need detail')
args = parser.parse_args()


# 文件路径用于记录已经处理过的 city_id
PROCESSED_FILE = 'processed_city_ids.txt'

def read_location():
    fin = open('location_city.txt')
    city_ids = []
    strippables = string.punctuation + string.whitespace
    for line in fin:
        line = line.strip(strippables)
        city, city_id = line.split(':')
        city_ids.append(city_id)
    return city_ids

def read_processed_city_ids():
    """读取已经处理过的城市ID列表"""
    try:
        with open(PROCESSED_FILE, 'r') as file:
            processed_city_ids = {line.strip() for line in file}  # 使用集合去重
    except FileNotFoundError:
        processed_city_ids = set()
    return processed_city_ids


def write_processed_city_id(city_id):
    """将处理过的城市ID写入文件"""
    with open(PROCESSED_FILE, 'a') as file:  # 追加模式
        file.write(f"{city_id}\n")


def process_city(city_id):
    """模拟爬取城市数据的操作"""
    try:
        # 这里是你的爬取逻辑
        controller = Controller(city_id)
        controller.main()

        # 成功后记录已经处理的 city_id
        write_processed_city_id(city_id)
        print(f"城市 {city_id} 爬取成功，已记录。")

    except Exception as e:
        print(f"城市 {city_id} 爬取失败，错误：{e}")
        time.sleep(10)  # 如果失败，等待 10 秒后重试
        

if __name__ == '__main__':
    city_ids = read_location()
    print(f'此时获取到的city_ids数据是：{city_ids}')
    
    # 读取已经处理的 city_ids，确保不重复爬取
    processed_city_ids = read_processed_city_ids()
    city_ids_to_process = [city_id for city_id in city_ids if city_id not in processed_city_ids]
    
    print(f'待处理的城市ID有: {city_ids_to_process}')
    
    for city_id in city_ids_to_process:
        print(f'爬取城市的location_id是: {city_id}')
        if args.normal == 1:
            process_city(city_id)  # 调用处理函数
            
            # controller = Controller(city_id)  # 每次创建 Controller 实例时传入不同的 city_id
            # controller.main()
            
        # if args.detail == 1:
        #     shop_id = args.shop_id
        #     logger.info('爬取店铺id：' + shop_id + '详情')
        #     controller.get_detail(shop_id, detail=args.need_more)
        # if args.review == 1:
        #     shop_id = args.shop_id
        #     logger.info('爬取店铺id：' + shop_id + '评论')
        #     controller.get_review(shop_id, detail=args.need_more)
