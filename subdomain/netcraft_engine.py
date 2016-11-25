import threading
import re
import urlparse
import hashlib
import urllib

from engine import EngineThreaded

class NetcraftEnum(EngineThreaded):
    def __init__(self, domain, sub_domains=None, q=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        self.base_url = 'http://searchdns.netcraft.com/?restriction=site+ends+with&host={domain}'
        self.engine_name = "Netcraft"
        self.lock = threading.Lock()
        super(NetcraftEnum, self).__init__(self.base_url, self.engine_name, domain, sub_domains, q=q, silent=silent,
                                           verbose=verbose)
        self.q = q
        return

    def req(self, url, cookies=None):
        cookies = cookies or {}
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-GB,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate',
                   }
        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout, cookies=cookies)
        except Exception as e:
            self._print(e)
            resp = None
        return resp

    def get_next(self, resp):
        link_regx = re.compile('<A href="(.*?)"><b>Next page</b></a>')
        link = link_regx.findall(resp)
        link = re.sub('host=.*?%s' % self.domain, 'host=%s' % self.domain, link[0])
        url = 'http://searchdns.netcraft.com' + link
        return url

    def create_cookies(self, cookie):
        cookies = dict()
        cookies_list = cookie[0:cookie.find(';')].split("=")
        cookies[cookies_list[0]] = cookies_list[1]
        cookies['netcraft_js_verification_response'] = hashlib.sha1(urllib.unquote(cookies_list[1])).hexdigest()
        return cookies

    def get_cookies(self, headers):
        if 'set-cookie' in headers:
            cookies = self.create_cookies(headers['set-cookie'])
        else:
            cookies = {}
        return cookies

    def enumerate(self):
        start_url = self.base_url.format(domain='example.com')
        resp = self.req(start_url)
        cookies = self.get_cookies(resp.headers)
        url = self.base_url.format(domain=self.domain)
        while True:
            resp = self.get_response(self.req(url, cookies))
            self.extract_domains(resp)
            if 'Next page' not in resp:
                return self.sub_domains
                break
            url = self.get_next(resp)

    def extract_domains(self, resp):
        link_regx = re.compile('<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                subdomain = urlparse.urlparse(link).netloc
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain and subdomain not in self.sub_domains and subdomain != self.domain:
                    if self.verbose:
                        self._print("%s%s: %s%s" % (R, self.engine_name, W, subdomain))
                    self.sub_domains.append(subdomain.strip())
        except Exception as e:
            pass
        return links_list