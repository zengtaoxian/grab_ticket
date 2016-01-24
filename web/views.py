# -*- coding: utf-8 -*-
__author__ = 'zengtaoxian'

from django.views.generic.base import TemplateView, RedirectView
from selenium.webdriver import Chrome, ActionChains
from django.core.urlresolvers import reverse
import threading
import time
from common.models import IDCode
import const


def check_bit(int_type, offset):
    mask = 1 << offset
    return int_type & mask


def get_position(no):
    x_offset = (no % (const.IMAGE_MAX_NO >> 1)) * const.IMAGE_X_STEP
    x = const.IMAGE_X_START + x_offset

    y_offset = (no / (const.IMAGE_MAX_NO >> 1)) * const.IMAGE_Y_STEP
    y = const.IMAGE_Y_START + y_offset
    return x, y


def select_image(ac, img, no):
    if no > const.IMAGE_MAX_NO:
        return

    x, y = get_position(no)

    ac.move_to_element(img).move_by_offset(x, y).click()


def click_image(browser, img, result):
    ac = ActionChains(browser)

    # 点击图形验证码进行选择
    print 'click image, result:%s' % (bin(result),)

    for no in range(0, const.IMAGE_MAX_NO):
        if check_bit(result, no):
            select_image(ac, img, no)

    ac.perform()


def order_submit_success(browser):
    if browser.current_url.split('?')[0] == const.ORDER_SUCCESS_URL:
        # 购票成功
        print 'order success'


def order_submit_failed(browser):
    # 点击确认按钮
    qr_close_btn = browser.find_element_by_id(const.QR_CLOSE_ID)
    qr_close_btn.click()

    # 点击查询按钮
    query_ticket_btn = browser.find_element_by_id(const.QUERY_TICKET_ID)
    query_ticket_btn.click()


def user_login(browser):
    print 'user login'

    # 获取验证码图形元素
    imgs = browser.find_elements_by_css_selector(const.TOUCLICK_IMAGE_CSS)

    # 等待网页加载
    time.sleep(2)

    # 获取验证码选择元素
    hovs = browser.find_elements_by_css_selector(const.TOUCLICK_HOV_CSS)
    if imgs and not hovs:
        img = imgs[0]

        # 有效的验证码图形元素的'src'属性不为空
        src = img.get_attribute(const.SRC_ATTR)
        if src and img.is_displayed():
            # 获取图形验证码id
            code_id = src.split('=')[-1].split('&')[-1]
            print 'code_id:' + code_id

            # 保存图形验证码id
            code = IDCode.objects.get_or_create(code=code_id)[0]
            if code.result:
                # 图形验证码的结果已经存在
                print 'code exist, result:' + str(code.result)
                click_image(browser, img, code.result)
            else:
                # 图形验证码的结果不存在, 继续尝试
                print 'code not exist, index:' + str(code.index)

                click_image(browser, img, code.index)

            # 点击登录按钮
            login_submit_btn = browser.find_element_by_id(const.LOGIN_SUBMIT_ID)
            login_submit_btn.click()

            # 等待网页加载
            time.sleep(2)

            print browser.current_url
            if browser.current_url == const.LOGIN_SUCCESS_URL:
                # 图形验证码输入正确
                print 'success, result:' + str(code.index)

                code.result = code.index
                code.save()
            else:
                code.index += 1
                if code.index >= const.CODE_INDEX_MAX:
                    code.index = 1
                code.save()


def user_logout(browser):
    print 'user logout'

    # 点击登出按钮
    logout_btn = browser.find_element_by_id(const.LOGOUT_ID)
    logout_btn.click()

    # 填写用户名
    username = browser.find_element_by_id(const.USER_NAME_ID)
    username.clear()
    username.send_keys(const.USERNAME)

    # 填写密码
    password = browser.find_element_by_id(const.PASSWORD_ID)
    password.clear()
    password.send_keys(const.PASSWORD)


def left_ticket(browser):
    print 'left ticket'

    # 获取验证码图形元素
    imgs = browser.find_elements_by_css_selector(const.TOUCLICK_IMAGE_CSS)

    # 获取验证码选择元素
    hovs = browser.find_elements_by_css_selector(const.TOUCLICK_HOV_CSS)
    if imgs and not hovs:
        # 可能存在多个验证码图形元素
        for img in imgs:
            # 有效的验证码图形元素的'src'属性不为空
            src = img.get_attribute(const.SRC_ATTR)
            if src:
                # 检查验证码是否显示
                randcode_other = browser.find_element_by_name(const.RANDCODE_OTHER_NAME)
                if not randcode_other.is_displayed():
                    # 点击提交按钮
                    qr_submit_btn = browser.find_element_by_id(const.QR_SUBMIT_ID)
                    qr_submit_btn.click()

                # 获取图形验证码id
                code_id = src.split('=')[-1].split('&')[-1]
                print 'code_id:' + code_id

                # 保存图形验证码id
                code = IDCode.objects.get_or_create(code=code_id)[0]
                if code.result:
                    # 图形验证码的结果已经存在
                    print 'code exist, result:' + str(code.result)
                    click_image(browser, img, code.result)
                else:
                    # 图形验证码的结果不存在, 继续尝试
                    print 'code not exist, index:' + str(code.index)
                    click_image(browser, img, code.index)

                # 点击提交按钮
                qr_submit_btn = browser.find_element_by_id(const.QR_SUBMIT_ID)
                qr_submit_btn.click()

                # 等待网页加载
                time.sleep(5)

                res_info = browser.find_element_by_id(const.ORDER_RESULT_INFO_ID)
                if res_info.is_displayed():
                    # 图形验证码输入正确
                    code.result = code.index
                    code.save()

                    res_texts = res_info.find_elements_by_css_selector(const.ORDER_RESULT_TEXT_CSS)
                    if res_texts:
                        res_text = res_texts[0]
                        print 'res_text:' + res_text.text
                        if res_text.text == const.ORDER_SUBMIT_FAILED_TEXT:
                            # 订票失败
                            order_submit_failed(browser)
                        else:
                            # 订票成功
                            order_submit_success(browser)

                    # 等待网页加载
                    time.sleep(2)
                else:
                    code.index += 1
                    if code.index >= const.CODE_INDEX_MAX:
                        code.index = 1
                    code.save()


def browser_work(arg):
    # 打开浏览器
    browser = Chrome()

    # 访问用户登录url
    browser.get(const.USER_LOGIN_URL)

    # 等待网页加载
    time.sleep(2)

    while 1:
        if browser.current_url.split('#')[0] == const.USER_LOGIN_URL:
            try:
                user_login(browser)
            except Exception, e:
                pass
        elif browser.current_url == const.LOGIN_SUCCESS_URL:
            if arg:
                try:
                    user_logout(browser)
                except Exception, e:
                    pass

        elif browser.current_url == const.LEFT_TICKET_URL:
            try:
                left_ticket(browser)
            except Exception, e:
                pass

        time.sleep(1)

    browser.quit()


class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class StartView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, **kwargs):
        t = threading.Thread(target=browser_work, args=(0,))
        t.start()
        return reverse('web:index')


class CatchView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, **kwargs):
        t = threading.Thread(target=browser_work, args=(1,))
        t.start()
        return reverse('web:index')