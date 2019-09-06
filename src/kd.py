#!/usr/bin/env python
# coding=utf-8
'''
@date: 2017-10-10
@author: Jason.Cooper
@copyright: 2017, Jason.Cooper <master@deamwork.com>
@license: BSD-3-clause
'''

import os, re, sys, json, random, time
import hashlib
from workflow import Workflow, ICON_INFO, ICON_ERROR, ICON_WARNING, web

DEFAULT_COOKIE = '2fd846a8d62b4116cc09b70b1fc69aa9_1567757074089;56da4ea5511e22b41c6d1815cfc82cba'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Referer': 'https://www.guoguo-app.com/queryExpress.htm',
    'Sec-Fetch-Mode': 'cros',
    'Accept': 'application/json',
    'Origin': 'https://www.guoguo-app.com',
    'Content-type': 'application/x-www-form-urlencoded',
    'DNT': '1'
}

def fetch_last_cookie():
    return wf.stored_data('cookie')

def store_last_cookie(cookie):
    wf.store_data('cookie', cookie)

def getToken(cookie):
    return cookie.split('_')[0]

def getSign(token, now, appKey, mailData):
    return hashlib.md5("{}&{}&{}&{}".format(token, now, appKey, mailData)).hexdigest()

def do_request(package_no, cookie):

    now = '{}'.format(int(time.time() * 1000))
    token = getToken(cookie)
    appKey = '12574478'
    data = '{{"mailNo":"{}","cpCode":""}}'.format(package_no)
    sign = getSign(token, now, appKey, data)

    # wf.logger.debug('[D] QUERY: \nnow:{}\ntoken:{}\ndata:{}\nsign:{}\n'.format(now,token,data,sign))

    API = 'https://h5api.m.taobao.com/h5/mtop.cnwireless.cnlogisticdetailservice.wapquerylogisticpackagebymailno/1.0/'
    param = {
        "jsv": "2.4.2",
        "appKey": appKey,
        "t": now,
        "sign": sign,
        "api": "mtop.cnwireless.CNLogisticDetailService.wapqueryLogisticPackageByMailNo",
        "AntiCreep": "true",
        "v": "1.0",
        "timeout": "5000",
        "type": "originaljson",
        "dataType": "json",
        "c": cookie,
        "data": data,
    }

    try:
        rt = web.get(API, params=param, headers=HEADERS, cookies={})
        rt.raise_for_status()
        response = rt.json()
        # wf.logger.debug('[D]: query response: ' + ''.join(json.dumps(response)))
        return response
    except Exception as e:
        # wf.logger.debug('[D]: Exception! query response: {}'.format(e))
        pass


def query_package_info(package_no):
    ret = {}

    try:
        response = do_request(
            package_no,
            cookie=fetch_last_cookie() or DEFAULT_COOKIE
        )

        # wf.logger.debug('[D]: last_cookie_1: {}'.format(fetch_last_cookie()))

        if 'c' in response.keys():
            store_last_cookie(response['c'])
            # wf.logger.debug('[D]: last_cookie_2: {}'.format(fetch_last_cookie()))
            response = do_request(package_no, cookie=response['c'])

        # wf.logger.debug('[D]: last_cookie_3: {}'.format(fetch_last_cookie()))

        if response['ret'][0] == u"SUCCESS::调用成功":
            data = response['data']
            ret['status'] = True
            ret['package_no'] = data['mailNo']
            ret['company'] = data['partnerName']
            ret['companyIcon'] = data['partnerIconUrl']
            ret['companyNumber'] = data['partnerContactPhone']
            ret['transitHistory'] = data['transitList']
            ret['transitStatus'] = data['packageStatus']['status']
            ret['transitDep'] = data['packageStatus']['departureName']
            ret['transitDst'] = data['packageStatus']['destinationName']
        elif response['ret'][0] == "RGV587_ERROR::SM":
            ret['status'] = False
            ret['package_no'] = package_no
            ret['company'] = u'临时封禁'

    except Exception as e:
        # wf.logger.debug('[D]: exception: {}'.format(e))
        ret['status'] = False
        ret['package_no'] = package_no
        ret['company'] = u'未知'
        pass

    return ret

def get_icon_status(item):
    truck_icon = 'assets/truck.png'
    up_icon = 'assets/up.png'
    success_icon = 'assets/success.png'
    package_icon = 'assets/icon.png'

    if 'sectionName' in item.keys(): # 是否存在 sectionName
        if item["sectionName"] == 'CONSIGN': # 等待揽收
            icon = package_icon
            deliver_status = u'等待揽收'
        if item["sectionName"] == 'TRANSPORT': # 运输中
            icon = truck_icon
            if item['action'] == 'TMS_ACCEPT': # 已揽收
                deliver_status = u'已揽收'
            elif item['action'] == 'TMS_STATION_IN': # 运输入站
                deliver_status = u'已到达'
            elif item['action'] == 'TMS_STATION_OUT': # 运输出站
                deliver_status = u'已离开'
            elif item['action'] == 'TMS_SENT_CITY': # 已抵达
                deliver_status = u'已抵达'
            elif item['action'] == 'TMS_DELIVERING': # 派送中
                deliver_status = u'派送中'
            else: # 未知情况
                deliver_status = u'运输中'
        if item["sectionName"] == 'SIGN': # 已签收
           icon=success_icon
           if item['action'] == 'TMS_SIGN': # 已签收
                deliver_status = u'已签收'
    else: # 无sectionName，当作普通信息对待
        if item['action'] == 'CREATE': # 下单
            icon = up_icon
            deliver_status = u'等待揽收'
        else:
            icon = up_icon
            deliver_status = ''

    return icon, deliver_status

def main(wf):

    truck_icon = 'assets/truck.png'
    up_icon = 'assets/up.png'
    success_icon = 'assets/success.png'
    package_icon = 'assets/icon.png'

    # 去掉参数两边的空格
    param = (wf.args[0] if len(wf.args) else '').strip()
    if param:
        resu = query_package_info(param)
        wf.logger.debug('[D]:Final Output: {}'.format(json.dumps(resu)))

        if resu['status'] == False:
            # 查无结果
            wf.add_item(
                title=u"查无结果，请稍后再试",
                subtitle=u"单号 {}, 错误信息: {}".format(resu['package_no'], resu['company']),
                arg="",
                valid=True,
                icon=package_icon
            )
        else:
            final = u'{company} {no} 物流信息详情\n从 {dep} 发往 {dst}，当前状态: {pkg_status}\n'.format(
                company=resu["company"],
                no=resu["package_no"],
                dep=resu['transitDep'],
                dst=resu['transitDst'],
                pkg_status=resu['transitStatus'],
            )
            for item in resu['transitHistory']:
                icon, deliver_status = get_icon_status(item)
                final += u'[{deliver_status}] {time} {message}\n'.format(
                        deliver_status=deliver_status,
                        time=item['time'],
                        message=item['message']
                    )

            wf.add_item(
                title=u'{company} {no}  {dep} 发往 {dst}'.format(
                    company=resu['company'],
                    no=resu['package_no'],
                    dep=resu['transitDep'],
                    dst=resu['transitDst'],
                ),
                subtitle=u"按 return(↵) 复制物流信息到剪贴板",
                arg=final,
                valid=True,
                icon=package_icon
            )

            for item in reversed(resu['transitHistory']):
                icon, deliver_status = get_icon_status(item)

                wf.add_item(
                    title=u'{deliver_status} {message}'.format(
                        deliver_status=deliver_status,
                        message=item['message']
                    ),
                    subtitle=item['time'],
                    arg=u'{deliver_status} {time} {message}'.format(
                        deliver_status=deliver_status,
                        time=item['time'],
                        message=item['message']
                    ),
                    valid=True,
                    icon=icon
                )
    else:
        wf.add_item(
            title=u"快递助手",
            subtitle=u"无需输入公司，直接输入单号即可",
            arg="",
            valid=True,
            icon=package_icon
        )

    wf.send_feedback()


if __name__ == u"__main__":

    wf = Workflow(update_settings={
        'github_slug': 'deamwork/kuaidi-workflow',
        'frequency': 7
    })

    if wf.update_available:
        wf.add_item(
            title=u'发现新版本',
            subtitle=u'选中本条目开始更新',
            autocomplete='workflow:update',
            icon=ICON_INFO
        )

    sys.exit(wf.run(main))
