from addons.UIdea.libs import ui as ui_class
import re
import requests

API_ENDPOINT = 'https://mcapi.us/server/status'


class UI(ui_class.UI):
    '''Minecraft server status UI class implementation'''
    def shouldCreate(msg):
        return collect_args(msg) is not None

    def onCreate(self, msg):
        args = collect_args(msg)
        is_good = True
        ip = args.group(1)
        if ':' in ip:
            splitip = ip.split(':')
            if len(splitip) == 2:
                payload = {'ip': splitip[0], 'port': splitip[1]}
            else:
                is_good = False
        else:
            payload = {'ip': ip}
        try:
            resp = requests.get(API_ENDPOINT, params=payload)
        except:
            is_good = False
        if not is_good:
            self.display_failure(ip)
        else:
            self.display_status(ip, resp.json())

    def display_failure(self, ip):
        self.embed.title = ':('
        self.embed.description = 'Failed to retrieve status info for `%s`' % ip
        self.embed.colour = 0xff1111
        self.update()

    def display_status(self, ip, resp_json):
        # online status
        if resp_json['online'] == True:
            self.embed.colour = 0x11ff11
        else:
            self.embed.title = ':('
            self.embed.description = '`%s` is offline or unreachable' % ip
            self.embed.colour = 0xff1111
            self.update()
            return
        # ip in title
        self.embed.title = ip
        # online players in field
        players = resp_json['players']
        self.embed.add_field(name='Online', value='%s/%s online' % (players['now'],players['max']))
        # mc version
        self.embed.add_field(name='Version', value='\n*%s*\n' % resp_json['server']['name'])
        # motd
        self.embed.add_field(name='MOTD', value='**%s**' % resp_json['motd'], inline=False)
        # debug
        # self.embed.description += 'Protocol: `%s`\n' % resp_json['server']['protocol']
        self.update()



def collect_args(msg):
    return re.search(r'\b(?:mc|minecraft)\s+(\S+)', msg.content, re.I)
