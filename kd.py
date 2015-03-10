# -*- coding: utf-8 -*-

import requests
import re
import sys
from wox import Wox, WoxAPI

services = {    'ems': u'EMS',
                'shentong': u'申通快递',
                'shunfeng': u'顺丰速运',
                'yuantong': u'圆通速递',
                'yunda': u'韵达快运',
                'zhongtong': u'中通快递',
                'huitongkuaidi': u'汇通快运',
                'tiantian': u'天天快递',
                'zhaijisong': u'宅急送',
                'youzhengguonei': u'邮政国内包裹',
                'youzhengguoji':u'邮政国际包裹',
                'emsguoji': u'EMS国际快递',
                'aae': u'AAE-中国',
                'anjiekuaidi': u'安捷快递',
                'anxindakuaixi': u'安信达',
                'youzhengguonei': u'包裹/平邮/挂号信',
                'bht': u'BHT国际快递',
                'baifudongfang': u'百福东方',
                'cces': u'CCES（希伊艾斯）',
                'lijisong': u'成都立即送',
                'dhl': u'DHL',
                'dhlde': u'DHL德国',
                'dsukuaidi': u'D速物流',
                'debangwuliu': u'德邦物流',
                'datianwuliu': u'大田物流',
                'dpex': u'DPEX',
                'disifang': u'递四方',
                'ems': u'EMS - 国内',
                'emsguoji': u'EMS - 国际',
                'ems': u'E邮宝',
                'rufengda': u'凡客',
                'fedexus': u'FedEx - 美国',
                'fedex': u'FedEx - 国际',
                'lianbangkuaidi': u'FedEx - 国内',
                'feikangda': u'飞康达',
                'youzhengguonei': u'挂号信',
                'ganzhongnengda': u'能达速递',
                'gongsuda': u'共速达',
                'gls': u'GLS',
                'tiantian': u'海航天天',
                'huitongkuaidi': u'汇通快运',
                'tiandihuayu': u'华宇物流',
                'hengluwuliu': u'恒路物流',
                'haiwaihuanqiu': u'海外环球',
                'huaxialongwuliu': u'华夏龙',
                'jiajiwuliu': u'佳吉快运',
                'jialidatong': u'嘉里大通',
                'jiayiwuliu': u'佳怡物流',
                'jinguangsudikuaijian': u'京广速递',
                'jindawuliu': u'金大物流',
                'jinyuekuaidi': u'晋越快递',
                'jixianda': u'急先达',
                'jiayunmeiwuliu': u'加运美',
                'kuaijiesudi': u'快捷速递',
                'lianbangkuaidi': u'联邦快递',
                'longbanwuliu': u'龙邦速递',
                'lanbiaokuaidi': u'蓝镖快递',
                'lijisong': u'立即送',
                'lejiedi': u'乐捷递',
                'lianhaowuliu': u'联昊通',
                'minghangkuaidi': u'民航快递',
                'meiguokuaidi': u'美国快递',
                'menduimen': u'门对门',
                'ocs': u'OCS',
                'quanfengkuaidi': u'全峰快递',
                'quanyikuaidi': u'全一快递',
                'quanchenkuaidi': u'全晨快递',
                'quanjitong': u'全际通',
                'quanritongkuaidi': u'全日通',
                'rufengda': u'如风达',
                'shentong': u'申通E物流',
                'shentong': u'申通快递',
                'shunfeng': u'顺丰速运',
                'suer': u'速尔快递',
                'shenghuiwuliu': u'盛辉物流',
                'shengfengwuliu': u'盛丰物流',
                'shangda': u'上大国际',
                'santaisudi': u'三态速递',
                'haihongwangsong': u'山东海红',
                'saiaodi': u'赛澳递',
                'tnt': u'TNT',
                'tiantian': u'天天快递',
                'tiandihuayu': u'天地华宇',
                'tonghetianxia': u'通和天下',
                'ups': u'UPS',
                'usps': u'USPS（美国邮政）',
                'wanjiawuliu': u'万家物流',
                'wanxiangwuliu': u'万象物流',
                'weitepai': u'微特派',
                'xinhongyukuaidi': u'鑫飞鸿',
                'xinbangwuliu': u'新邦物流',
                'xinfengwuliu': u'信丰物流',
                'cces': u'希伊艾斯（CCES）',
                'yuantong': u'圆通速递',
                'yunda': u'韵达快运',
                'youzhengguonei': u'邮政国内包裹',
                'youzhengguoji': u'邮政国际包裹',
                'ems': u'邮政特快专递',
                'yuanchengwuliu': u'远成物流',
                'yafengsudi': u'亚风速递',
                'yuanweifeng': u'源伟丰',
                'youshuwuliu': u'优速快递',
                'yuanzhijiecheng': u'元智捷诚',
                'yuefengwuliu': u'越丰物流',
                'yuananda': u'源安达',
                'yuanfeihangwuliu': u'原飞航',
                'yinjiesudi': u'银捷速递',
                'yuntongkuaidi': u'运通中港',
                'zhaijisong': u'宅急送',
                'zhongtong': u'中通快递',
                'zhongtiewuliu': u'中铁快运',
                'ztky': u'中铁物流',
                'zhongyouwuliu': u'中邮物流',
                'zhimakaimen': u'芝麻开门',
                'zhongxinda': u'忠信达',
                'zhengzhoujianhua': u'郑州建华'   }


class QueryException(Exception):
    pass


def pxto(type_, postid):
    API = 'http://www.kuaidi100.com/query'
    payload = {'type': type_, 'postid': postid}
    rsp = requests.get(API, params=payload)
    rsp.encoding = 'utf-8'
    data = rsp.json()
    if data.get('status') == u'200':
        return data
    else:
        raise QueryException()


class Main(Wox):

    def query(self, param):

        def gen_rpc(method, *p):
            return {'method': method, 'parameters': list(p), 'dontHideAfterAction': True}

        type_ = re.findall(r'\D+', param)  # 快递公司
        id_ = re.findall(r'\d+', param)  # 运单号

        # 支持的快递公司名称提示
        if len(type_) < 1:
            result = [
                {
                    'Title': v,
                    'JsonRPCAction': gen_rpc('_pick_service', v)
                }
                for (_, v) in services.iteritems()
            ]
        elif len(type_) == 1:
            key = type_[0].strip()
            # 可根据缩写或汉字查找快递公司
            if len(id_) == 0:
                result = [{'Title': u'请输入您的运单号'}]
                result += [
                    {
                        'Title': v,
                       'JsonRPCAction': gen_rpc('_pick_service', v)
                    }
                    for (k, v) in services.iteritems() if k.find(key) != -1 or (v.find(key) != -1 and v != key)
                ]
            else:
                result = [{'Title': u'尚未支持该快递公司'}]
                for (k, v) in services.iteritems():
                    if k == key or v == key:
                        try:
                            result = self._get_status(k, id_[0].strip())
                        except QueryException:
                            result = [{'Title': u'未知查询错误, 请检查运单号是否填写正确'}]
                        except:
                            result = [{'Title': u'未知错误'}]
                        break
        return result

    def _pick_service(self, service):
        """
        供用户选取提示列表中的快递公司。
        """
        query = ['kd', service + ' ']
        WoxAPI.change_query(' '.join(query))

    def _get_status(self, service, id_):
        data = pxto(service, id_)
        result = [{
                      'Title': item.get('context'),
                      'SubTitle': item.get('time'),
                      'dontHideAfterAction': True
                  }
                  for item in data.get('data')
        ]
        return result


if __name__ == '__main__':
    Main()
