import logging
import re
import sys
if sys.version_info < (3, 0):
    from urllib import urlencode
else:
    from urllib.parse import urlencode

from pyquery import PyQuery

from .base_extractor import BaseExtractor
from pycis import utils


class WiseUnpacker(object):
    param_regex = re.compile(
        r";\}\('(?P<param_w>\w+)'[\s,]+'(?P<param_i>\w+)'[\s,]+'(?P<param_s>\w+)'[\s,]+'(?P<param_e>\w+)'\)\);")

    @staticmethod
    def unpack(w, i, s, e):
        """
        function (w, i, s, e) {
          var lIll = 0;
          var ll1I = 0;
          var Il1l = 0;
          var ll1l = [];
          var l1lI = [];
          while (true) {
              if (lIll < 5) l1lI.push(w.charAt(lIll));
              else if (lIll < w.length) ll1l.push(w.charAt(lIll));
              lIll++;
              if (ll1I < 5) l1lI.push(i.charAt(ll1I));
              else if (ll1I < i.length) ll1l.push(i.charAt(ll1I));
              ll1I++;
              if (Il1l < 5) l1lI.push(s.charAt(Il1l));
              else if (Il1l < s.length) ll1l.push(s.charAt(Il1l));
              Il1l++;
              if (w.length + i.length + s.length + e.length == ll1l.length + l1lI.length + e.length) break;
          }
          var lI1l = ll1l.join('');
          var I1lI = l1lI.join('');
          ll1I = 0;
          var l1ll = [];
          for (lIll = 0; lIll < ll1l.length; lIll += 2) {
              var ll11 = -1;
              if (I1lI.charCodeAt(ll1I) % 2) ll11 = 1;
              l1ll.push(String.fromCharCode(parseInt(lI1l.substr(lIll, 2), 36) - ll11));
              ll1I++;
              if (ll1I >= l1lI.length) ll1I = 0;
          }
          return l1ll.join('');
        }
        """

        va = 0
        vb = 0
        vc = 0
        vd = []
        ve = []
        while True:
            if va < 5:
                ve.append(w[va])
            elif va < len(w):
                vd.append(w[va])

            va += 1

            if vb < 5:
                ve.append(i[vb])
            elif vb < len(i):
                vd.append(i[vb])

            vb += 1

            if vc < 5:
                ve.append(s[vc])
            elif vc < len(s):
                vd.append(s[vc])

            vc += 1

            if (len(w) + len(i) + len(s) + len(e)) == (len(vd) + len(ve) + len(e)):
                break

        vf = "".join(vd)  # vf = vd.join('')
        vg = "".join(ve)  # vg = ve.join('')

        vb = 0
        vi = []
        for va in range(0, len(vd), 2):  # (va = 0; va < vd; va += 2)
            vj = -1
            if ord(vg[vb]) % 2:  # (vg.charCodeAt(vb) % 2):
                vj = 1

            # vi.append(String.fromCharCode(parseInt(vf.substr(va, 2), 36) - vj))
            vi.append(chr(int(vf[va:va + 2], 36) - vj))

            vb += 1

            if vb >= len(ve):
                vb = 0

        result = ''.join(vi)  # vi.join('')

        rgx = WiseUnpacker.param_regex
        if re.search(rgx, result):
            w = re.search(rgx, result).group('param_w')
            i = re.search(rgx, result).group('param_i')
            s = re.search(rgx, result).group('param_s')
            e = re.search(rgx, result).group('param_e')

            result = WiseUnpacker.unpack(w, i, s, e)

        return result


class DivxStageExtractor(BaseExtractor):

    """ divxstage extractor
    """

    def __init__(self):
        # super().__init__(self)
        super(DivxStageExtractor, self).__init__()
        self.host_list = ["divxstage.eu"]
        self.holder_url = "http://embed.divxstage.eu/embed.php?&width=653&height=438&v={}"
        self.regex_url = re.compile(
            r"(http|https)://(www|embed)\.(?P<host>divxstage\.eu)/(embed\.php\?v=http://www\.divxstage\.eu/)?(file/|video/)(?P<id>\w+$|\w+)(.*?$)"
        )
        self.example_urls = [
            "http://www.divxstage.eu/video/oef0hwolepndo",
            "http://embed.divxstage.eu/embed.php?v=http://www.divxstage.eu/file/b04c4b011a81e&height=438&width=653"
        ]

    def get_raw_url(self, video_id_or_url, show_progress=False):
        video_id = None
        if self.regex_url.match(video_id_or_url):
            video_id = self.regex_url.match(video_id_or_url).group('id')
        else:
            video_id = video_id_or_url
        dest_url = self.holder_url.format(video_id)

        logging.info("Destination url {}".format(dest_url))
        html_embed = utils.fetch_page(dest_url)

        pq = PyQuery(html_embed)
        scripts_text = pq('body script').text()

        rgx = re.compile(
            b"}\('(?P<param_w>\w+)'[,\s]+'(?P<param_i>\w+)'[\s,]+'(?P<param_s>\w+)'[\s,]'(?P<param_e>\w+)'"
        )
        # unpack script
        unpacked_script = None

        if rgx.search(html_embed):
            # find unpack function params

            w = rgx.search(html_embed).group('param_w').decode('ascii')
            i = rgx.search(html_embed).group('param_i').decode('ascii')
            s = rgx.search(html_embed).group('param_s').decode('ascii')
            e = rgx.search(html_embed).group('param_e').decode('ascii')

            unpacked_script = WiseUnpacker.unpack(w, i, s, e)

        # find "key" param
        key_var_rgx = re.search(r'filekey=(\w+)', unpacked_script).group(1)
        key_param = re.search(key_var_rgx + r'="([\w\.\-]+)"', unpacked_script).group(1)
        # key_param = re.search(r'll="([\w\.\-]+)', unpacked_script).group(1)

        # find "file" param
        file_param = re.search(
            r'advURL="http://www\.divxstage\.eu/video/(\w+)"', unpacked_script).group(1)

        qparams = {
            "key": key_param,
            "file": file_param,
        }

        # call api to get result string containing raw url
        api_call = "http://www.divxstage.eu/api/player.api.php?" + urlencode(qparams)
        api_result = str(utils.fetch_page(api_call))

        # extract raw url from api_call result
        url_found = None
        try:
            rgx = re.compile(r'url=(?P<rurl>http://[\w\.\-/=]+\.flv|mp4|avi|mk4|m4a)')
            url_found = rgx.search(api_result).group('rurl')
        except (IndexError, AttributeError):
            return None

        if show_progress:
            if url_found:
                sys.stdout.write('.')
            else:
                sys.stdout.write('F')
            sys.stdout.flush()

        return url_found
