from resources.proxy_resource import ProxyResource


def setup(api):
    api.add_resource(ProxyResource, '/<path:endpoint>')
