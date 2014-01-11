# -*- encoding: utf-8 -*-
# author: binux<17175297.hk@gmail.com>

import re
from tornado import gen
from tornado.web import HTTPError, UIModule, asynchronous, authenticated, RequestHandler
from tornado.options import options
from functools import partial
from base import BaseHandler
from libs.util import AsyncProcessMixin, _now
import requests
import logging
from pprint import pformat

DEBUG = logging.debug

add_task_info_map = {
     0: u"添加任务失败",
    -1: u"获取任务信息失败",
    -2: u"服务器尚未索引该资源!",
    -3: u"未知的链接类型",
    -4: u"任务已存在",
    -5: u"添加任务失败",
    -6: u"请输入验证码",
    -7: u"验证码错误",
    -99: u"与迅雷服务器通信失败，请稍候再试...",
}
_split_re = re.compile(u"[,|，, ]")
class AddTaskHandler(BaseHandler, AsyncProcessMixin):
    def get(self, anonymous):
        render_path = "add_task_anonymous.html" if anonymous else "add_task.html"
        if not self.current_user:
            message = "Please login first."
        elif anonymous and not self.has_permission("add_anonymous_task"):
            message = u"您没有添加任务的权限。"
        elif not anonymous and not self.has_permission("add_task"):
            message = u"您没有发布资源的权限。"
        elif self.user_manager.get_add_task_limit(self.current_user["email"]) <= 0:
            message = u"您今天添加的任务太多了！请重新登录以激活配额或联系管理员。"
        else:
            message = ""

        self.render(render_path, message=message, timestamp=_now())

    @authenticated
    @asynchronous
    @gen.engine
    def post(self, anonymous):
        if options.using_xsrf:
            self.check_xsrf_cookie()
        url = self.get_argument("url", None)
        btfile = self.request.files.get("btfile")
        btfile = btfile[0] if btfile else None
        title = self.get_argument("title", None)
        tags = self.get_argument("tags", "")
        anonymous = True if anonymous else False
        render_path = "add_task_anonymous.html" if anonymous else "add_task.html"
        email = self.current_user['email']
        verifycode = self.get_argument("verifycode", None)
        DEBUG(pformat('verifycode is %s.' % verifycode))
        verifykey = self.get_cookie("verifykey") or None
        DEBUG(pformat('verifykey is %s.' % verifykey))

        if anonymous and not self.has_permission("add_anonymous_task"):
            raise HTTPError(403, "You might not have permission to add anonymous task.")
        elif not anonymous and not self.has_permission("add_task"):
            raise HTTPError(403, "You might not have permission to add task.")
        elif self.user_manager.get_add_task_limit(self.current_user["email"]) <= 0:
            raise HTTPError(403, "You had reach the limit of adding tasks.")

        if not url and not btfile:
            self.render(render_path, message=u"任务下载地址不能为空！", timestamp=_now())
            return
        if btfile and len(btfile['body']) > 500*1024:
            self.render(render_path, message=u"种子文件过大！", timestamp=_now())
            return

        if tags:
            tags = set([x.strip() for x in _split_re.split(tags)])

        result, task = yield gen.Task(self.call_subprocess, partial(
            self.task_manager.add_task, btfile or url, title, tags, email, anonymous, self.has_permission("need_miaoxia"), verifycode, verifykey
        ))

        if result == 1:
            if task:
                self.write("""<script>
    parent.$('#fancybox-content').css({height: "350px"});
	parent.$.fancybox.resize();
    location='/get_lixian_url?task_id=%d'
</script>""" % task.id)
            else:
                self.write("<script>top.location='/'</script>")
            self.user_manager.incr_add_task_limit(self.current_user["email"])
            self.finish()
        else:
            if anonymous:
                self.render("add_task_anonymous.html", message=add_task_info_map.get(result, u"未知错误"), timestamp=_now())
            else:
                self.render("add_task.html", message=add_task_info_map.get(result, u"未知错误"), timestamp=_now())

class VerifycodeImageHandler(RequestHandler):
    def get(self):
        verifycode_image_url = 'http://verify2.xunlei.com/image?cachetime=%s' % _now()
        r = requests.get(verifycode_image_url)
        verifycode_image = r.content
        verifykey = r.cookies['VERIFY_KEY']
        self.set_header('Content-Type', 'image/jpeg')
        self.set_cookie('verifykey', verifykey, domain=self.request.host, path='/')
        self.write(verifycode_image)

handlers = [
        (r"/add_task(_anonymous)?", AddTaskHandler),
        (r"/verifycode\.jpg", VerifycodeImageHandler)
]
ui_modules = {
}
