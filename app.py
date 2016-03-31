# -*- coding: utf-8 -*-

import web
# Jinja2 template engine.
from web.contrib.template import render_jinja


# Debug set False on production.
web.config.debug = False
db = web.database(dbn='mysql', user='root', pw='', db='webpy')
urls = (
    '/', 'Index',
    '/about', 'About',
    '/proxy', 'Proxy',
    '/login', 'Login',
    '/search', 'ProxySearch',
    '/add', 'ProxyAdd',
    '/delete', 'ProxyDelete',
    '/manage', 'Manage',
    '/contact', 'Contact'
)
t_globals = {'datestr': web.datestr}
render = render_jinja('templates', encoding='utf-8')


def need_login(func):

    def login_check(self):
        if(globals().get('u_name') and globals().get('u_password')):
            return func(self)
        else:
            return render.login()

    return login_check


class Index:

    def GET(self):
        return render.index()


class About:

    def GET(self):
        return render.about()


class Proxy:

    def GET(self):
        return render.proxy()

    def POST(self):
        post_data = web.input()
        name = post_data.get('wx_name', '')
        if not name:
            return render.proxy()
        ret = db.select('proxy_weixin_names', where='name="%s"' % (name))
        data = []
        if ret:
            for o in ret:
                o['create_time'] = str(o.get('create_time', ''))
                data.append(dict(**o))
        return render.proxy(proxies=data, name=name)


class Login:

    def GET(self):
        return render.login()

    def POST(self):
        post_data = web.input()
        name = post_data.get('name', '')
        password = post_data.get('password', '')
        if name != 'username' or password != 'password':
            return render.login()
        else:
            globals()['u_name'] = name
            globals()['u_password'] = password
            return render.manage()


class Manage:

    @need_login
    def GET(self):
        return render.manage()

    @need_login
    def POST(self):
        post_data = web.input()
        name = post_data.get('wx_name', '')
        if not name:
            return render.manage()
        name = '%'+name+'%'
        ret = db.query("select * from proxy_weixin_names where name like $x", vars=dict(x=name))
        data = []
        if ret:
            for o in ret:
                o['create_time'] = str(o.get('create_time', ''))
                data.append(dict(**o))
        return render.manage(proxies=data, name=name)


class ProxySearch:

    def GET(self):
        return render.manage()

    @need_login
    def POST(self):
        post_data = web.input()
        name = post_data.get('wx_name', '')
        if not name:
            return render.manage()
        temp = '%'+name+'%'
        ret = db.query("select * from proxy_weixin_names where name like $x", vars=dict(x=temp))
        data = []
        if ret:
            for o in ret:
                o['create_time'] = str(o.get('create_time', ''))
                data.append(dict(**o))
        return render.manage(proxies=data, name=name)


class ProxyAdd:

    def GET(self):
        return render.manage()

    @need_login
    def POST(self):
        post_data = web.input()
        name = post_data.get('wx_name', '')
        if not name:
            return render.proxy()
        db.insert('proxy_weixin_names', name=name)
        return render.manage(name=name)


class ProxyDelete:

    @need_login
    def GET(self):
        id = web.input().id
        db.delete('proxy_weixin_names', where='id = $id', vars=dict(id=id))
        return render.manage()


class Contact:

    def GET(self):
        return render.contact()


# For serving using any wsgi server
wsgi_app = web.application(urls, globals()).wsgifunc()


if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    app.run()
