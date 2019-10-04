from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from Retailers.settings import ERROR_PATH
from CeleryTask.tasks import sendDing
import time


class MiddleWareTest(MiddlewareMixin):
    def process_request(self, request):
        request_ip = request.META['REMOTE_ADDR']
        print(request.META)
        print(request.META['REMOTE_ADDR'])
        if request_ip == '10.10.14.224':
            return HttpResponse('非法IP')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        '''

        :param request: 请求
        :param callback: 对应视图函数，访问哪个就是哪个
        :param callback_args: 视图函数参数 元组类型
        :param callback_kwargs: 视图函数参数 字典类型
        :return:
        '''
        print('process_view')

    def process_exception(self, request, exception):
        '''
        :param request:
        :param exception:
        :return:
        '''
        if exception:
            with open(ERROR_PATH, 'a')as f:
                now = time.strftime('%Y-%m-%d %H:%M:%%S', time.localtime())
                content = '[%s]:%s\n' % (now, exception)
                f.write(content)
                sendDing.delay(content)
        return HttpResponse('代码写错了，错误如下：</br>%s') % exception

    def process_template_response(self, request, response):
        '''
        必须返回一个render才能触发
        :param request:
        :param response:
        :return:
        '''
        print('process_template_response')
        return HttpResponse('abc')

    def process_response(self, request, response):
        '''
        process_response和process_template_response必须有返回值
        :param request:
        :param response:
        :return:
        '''
        print('process_response')
        return response
