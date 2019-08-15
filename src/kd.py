#!/usr/bin/env python
# coding=utf-8
'''
@date: 2017-10-10
@author: Jason.Cooper
@copyright: 2017, Jason.Cooper <master@deamwork.com>
@license: BSD-3-clause
'''

import os
import sys, json, random, time
from workflow import Workflow, ICON_INFO, ICON_ERROR, ICON_WARNING, web

COMPANY_CODE = {
    'shentong': u'申通快递',
    'ems': u'EMS',
    'shunfeng': u'顺丰速运',
    'yunda': u'韵达快递',
    'yuantong': u'圆通速递',
    'zhongtong': u'中通速递',
    'huitongkuaidi': u'汇通快运',
    'tiantian': u'天天快递',
    'zhaijisong': u'宅急送',
    'xinhongyukuaidi': u'鑫飞鸿',
    'cces': u'CCES(国通快递)',
    'quanyikuaidi': u'全一快递',
    'biaojikuaidi': u'彪记快递',
    'xingchengjibian': u'星晨急便',
    'yafengsudi': u'亚风速递',
    'yuanweifeng': u'源伟丰',
    'quanritongkuaidi': u'全日通',
    'anxindakuaixi': u'安信达',
    'minghangkuaidi': u'民航快递',
    'fenghuangkuaidi': u'凤凰快递',
    'jinguangsudikuaijian': u'京广速递',
    'peisihuoyunkuaidi': u'配思货运',
    'ztky': u'中铁物流',
    'ups': u'UPS',
    'fedex': u'FedEx-国际件',
    'tnt': u'TNT',
    'dhl': u'DHL-中国件',
    'aae': u'AAE-中国件',
    'datianwuliu': u'大田物流',
    'debangwuliu': u'德邦物流',
    'xinbangwuliu': u'新邦物流',
    'longbanwuliu': u'龙邦速递',
    'yibangwuliu': u'一邦速递',
    'suer': u'速尔快递',
    'lianhaowuliu': u'联昊通',
    'guangdongyouzhengwuliu': u'广东邮政',
    'zhongyouwuliu': u'中邮物流',
    'tiandihuayu': u'天地华宇',
    'shenghuiwuliu': u'盛辉物流',
    'changyuwuliu': u'长宇物流',
    'feikangda': u'飞康达',
    'yuanzhijiecheng': u'元智捷诚',
    'youzhengguonei': u'包裹/平邮',
    'youzhengguoji': u'国际包裹',
    'wanjiawuliu': u'万家物流',
    'yuanchengwuliu': u'远成物流',
    'xinfengwuliu': u'信丰物流',
    'wenjiesudi': u'文捷航空',
    'quanchenkuaidi': u'全晨快递',
    'jiayiwuliu': u'佳怡物流',
    'youshuwuliu': u'优速物流',
    'kuaijiesudi': u'快捷速递',
    'dsukuaidi': u'D速快递',
    'quanjitong': u'全际通',
    'ganzhongnengda': u'能达速递',
    'anjiekuaidi': u'青岛安捷快递',
    'yuefengwuliu': u'越丰物流',
    'dpex': u'DPEX',
    'jixianda': u'急先达',
    'baifudongfang': u'百福东方',
    'bht': u'BHT',
    'wuyuansudi': u'伍圆速递',
    'lanbiaokuaidi': u'蓝镖快递',
    'coe': u'COE',
    'nanjing': u'南京100',
    'hengluwuliu': u'恒路物流',
    'jindawuliu': u'金大物流',
    'huaxialongwuliu': u'华夏龙',
    'yuntongkuaidi': u'运通中港',
    'jiajiwuliu': u'佳吉快运',
    'shengfengwuliu': u'盛丰物流',
    'yuananda': u'源安达',
    'jiayunmeiwuliu': u'加运美',
    'wanxiangwuliu': u'万象物流',
    'hongpinwuliu': u'宏品物流',
    'gls': u'GLS',
    'shangda': u'上大物流',
    'zhongtiewuliu': u'中铁快运',
    'yuanfeihangwuliu': u'原飞航',
    'haiwaihuanqiu': u'海外环球',
    'santaisudi': u'三态速递',
    'jinyuekuaidi': u'晋越快递',
    'lianbangkuaidi': u'联邦快递',
    'feikuaida': u'飞快达',
    'quanfengkuaidi': u'全峰快递',
    'rufengda': u'如风达',
    'lejiedi': u'乐捷递',
    'zhongxinda': u'忠信达',
    'zhimakaimen': u'芝麻开门',
    'saiaodi': u'赛澳递',
    'haihongwangsong': u'海红网送',
    'gongsuda': u'共速达',
    'jialidatong': u'嘉里大通',
    'ocs': u'OCS',
    'usps': u'USPS',
    'meiguokuaidi': u'美国快递',
    'lijisong': u'立即送',
    'yinjiesudi': u'银捷速递',
    'menduimen': u'门对门',
    'disifang': u'递四方',
    'zhengzhoujianhua': u'郑州建华',
    'hebeijianhua': u'河北建华',
    'weitepai': u'微特派',
    'dhlde': u'DHL-德国件',
    'tonghetianxia': u'通和天下',
    'emsguoji': u'EMS-国际件',
    'fedexus': u'FedEx-美国件',
    'fengxingtianxia': u'风行天下',
    'kangliwuliu': u'康力物流',
    'kuayue': u'跨越速递',
    'haimengsudi': u'海盟速递',
    'shenganwuliu': u'圣安物流',
    'yitongfeihong': u'一统飞鸿',
    'zhongsukuaidi': u'中速快递',
    'neweggozzo': u'新蛋奥硕',
    'ontrac': u'OnTrac',
    'sevendays': u'七天连锁',
    'mingliangwuliu': u'明亮物流',
    'vancl': u'凡客配送',
    'huaqikuaiyun': u'华企快运',
    'city100': u'城市100',
    'sxhongmajia': u'红马甲物流',
    'suijiawuliu': u'穗佳物流',
    'feibaokuaidi': u'飞豹快递',
    'chuanxiwuliu': u'传喜物流',
    'jietekuaidi': u'捷特快递',
    'longlangkuaidi': u'隆浪快递',
    'emsen': u'EMS-英文',
    'zhongtianwanyun': u'中天万运',
    'hkpost': u'香港邮政',
    'bangsongwuliu': u'邦送物流',
    'guotongkuaidi': u'国通快递',
    'auspost': u'澳大利亚邮政',
    'canpost': u'加拿大邮政-英文版',
    'canpostfr': u'加拿大邮政-法文版',
    'upsen': u'UPS-全球件',
    'tnten': u'TNT-全球件',
    'dhlen': u'DHL-全球件',
    'shunfengen': u'顺丰-美国件',
    'huiqiangkuaidi': u'汇强快递',
    'xiyoutekuaidi': u'希优特',
    'haoshengwuliu': u'昊盛物流',
    'shangcheng': u'尚橙物流',
    'yilingsuyun': u'亿领速运',
    'dayangwuliu': u'大洋物流',
    'didasuyun': u'递达速运',
    'yitongda': u'易通达',
    'youbijia': u'邮必佳',
    'yishunhang': u'亿顺航',
    'feihukuaidi': u'飞狐快递',
    'xiaoxiangchenbao': u'潇湘晨报',
    'balunzhi': u'巴伦支',
    'aramex': u'Aramex',
    'minshengkuaidi': u'闽盛快递',
    'syjiahuier': u'佳惠尔',
    'minbangsudi': u'民邦速递',
    'shanghaikuaitong': u'上海快通',
    'xiaohongmao': u'北青小红帽',
    'gsm': u'GSM',
    'annengwuliu': u'安能物流',
    'kcs': u'KCS',
    'citylink': u'City-Link',
    'diantongkuaidi': u'店通快递',
    'fanyukuaidi': u'凡宇快递',
    'pingandatengfei': u'平安达腾飞',
    'guangdongtonglu': u'广东通路',
    'zhongruisudi': u'中睿速递',
    'kuaidawuliu': u'快达物流',
    'jiajikuaidi': u'佳吉快递',
    'adp': u'ADP国际快递',
    'fardarww': u'颿达国际快递',
    'fandaguoji': u'颿达国际快递(英文)',
    'shlindao': u'林道国际快递',
    'sinoex': u'中外运速递(中文)',
    'zhongwaiyun': u'中外运速递',
    'dechuangwuliu': u'深圳德创物流',
    'ldxpres': u'林道国际快递(英文)',
    'ruidianyouzheng': u'瑞典邮政包裹小包',
    'postenab': u'Posten AB',
    'nuoyaao': u'偌亚奥国际快递',
    'chengjisudi': u'城际速递',
    'xianglongyuntong': u'祥龙运通物流',
    'pinsuxinda': u'品速心达快递',
    'yuxinwuli': u'宇鑫物流',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Referer': 'http://www.kuaidi100.com'
}

def get_package_company(package_no):

    COPMPANY_QUERY_URL = 'http://www.kuaidi100.com/autonumber/autoComNum'

    try:
        rt = web.get(COPMPANY_QUERY_URL, params=dict(resultv2=1, text=package_no), headers=HEADERS)
        rt.raise_for_status()

        # 去掉前缀和多余空格，最长的即是最优解
        result = rt.json()
        wf.logger.debug('[D]: company1: ' + ''.join(json.dumps(result)))
        result = result['auto']
        wf.logger.debug('[D]: company2: ' + ''.join(json.dumps(result)))

        return [result[0]['comCode'], COMPANY_CODE[result[0]['comCode']]]
    except Exception as e:
        wf.logger.debug('[D]: exception: {}'.format(e))
        result = [u'Unknow', u'未知快递公司']

    return result

def query_package_info(package_no):

    ret = {}

    com_code = get_package_company(package_no)
    wf.logger.debug('[D]:Final company: ' + ''.join(com_code))

    if com_code[0] is u'Unknow':
        ret['status'] = False
        ret['company'] = com_code[1] + u"或单号不可用"
        return ret


    API = 'http://www.kuaidi100.com/query'
    param = {
        "type": com_code[0],
        "postid": package_no,
        "temp": (time.time() / 100000000000) + (random.randint(0,9) / 10),
        "phone": None
    }

    try:
        rt = web.get(API, params=param, headers=HEADERS)
        rt.raise_for_status()
        response = rt.json()
        wf.logger.debug('[D]: query response: ' + ''.join(json.dumps(response)))

        if response:
            ret['data'] = response["data"]
            ret['status'] = True
            ret['package_no'] = response["nu"]
            ret['company'] = com_code[1]
            ret['state'] = response['state']
            ret['condition'] = response['condition']
            pass
        else:
            ret['status'] = False
            ret['company'] = com_code[1] + u"或单号不可用"
            ret['state'] = response['state']
            ret['condition'] = response['condition']
            return

    except Exception:
        ret['status'] = False
        ret['company'] = com_code[1] + u"或单号不可用"
        ret['state'] = response['state']
        ret['condition'] = response['condition']
        pass

    return ret

def main(wf):

    truck = u'\U0001F69A'
    truck_icon = 'assets/truck.png'
    up_icon = 'assets/up.png'
    success = u'\U00002705'
    success_icon = 'assets/success.png'
    package_icon = 'assets/icon.png'

    # 去掉参数两边的空格
    param = (wf.args[0] if len(wf.args) else '').strip()
    if param:
        resu = query_package_info(param)
        wf.logger.debug('[D]:Final Output: {}'.format(json.dumps(resu)))

        if resu['state'] == '3' or resu['condition'] == 'F00':
            # 查无结果
            wf.add_item(title=resu["company"] + " " + resu["package_no"],
                    subtitle=u"查无结果（可能是接口调用过多，请稍后再试）",
                    arg="",
                    valid=True,
                    icon=package_icon)
        else:
            final = resu["company"] + " " + resu["package_no"] + u" 物流信息详情\n"
            for item in reversed(resu['data']):
                final += item["time"] + " " + item["context"] + " " + item["location"] or "" + "\n"
            wf.add_item(title=resu["company"] + " " + resu["package_no"],
                        subtitle=u"按 return(↵) 复制物流信息到剪贴板",
                        arg=final,
                        valid=True,
                        icon=package_icon)
            for item in resu['data']:
                if u'签收' in item["context"]:
                    wf.add_item(title=success + " " + item["context"] + " " + item["location"],
                        subtitle=item["time"],
                        arg=item["context"] + " " + item["location"] or "" ,
                        valid=True,
                        icon=success_icon)
                else:
                    wf.add_item(title=truck + " " + item["context"] + " " + item["location"],
                        subtitle=item["time"],
                        arg=item["context"] + " " + item["location"] or "" ,
                        valid=True,
                        icon=truck_icon)
    else:
        title = u"快递助手"
        subtitle = u"无需输入公司，直接输入单号即可"
        wf.add_item(title=title,
                    subtitle=subtitle,
                    arg="",
                    valid=True,
                    icon=package_icon)
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow(update_settings={
        'github_slug': 'deamwork/kuaidi-workflow',
        'frequency': 7
    })

    if wf.update_available:
        wf.add_item(u'发现新版本',
                u'选中本条目开始更新',
                autocomplete='workflow:update',
                icon=ICON_INFO)

    sys.exit(wf.run(main))
