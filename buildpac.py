import sys
import os

def build():
    temprule = ""
    rule1_content = ""
    fh = open(sys.argv[1], 'r')
    for line in fh:
        rule1_content += line
    temprule += rule1_content

    for i in range(2,7,2):
        temp_sub = ""
        rule1_content = ""
        fh = open(sys.argv[i], 'r')
        for line in fh:
            rule1_content += """    shExpMatch(host, "%s") || shExpMatch(host, "*.%s") ||
    """ % (line.rstrip(), line.rstrip())
        temp_sub = 'if ( ' + rule1_content.strip() + """false) return '"""+sys.argv[i+1]+"""';
    """
        temprule += temp_sub

    tempfun = """function FindProxyForURL(url, host)
{
    %s
    return "DIRECT";
}""" % temprule
    fundef = """var shExpMatch = function (){
    var _map = { '.': '\\.', '*': '.*?', '?': '.' };
    var _rep = function (m){ return _map[m] };
    return function (text, exp){
        return new RegExp(exp.replace(/\.|\*|\?/g, _rep)).test(text);
    };
}();
var isInNet = function (){
    function convert_addr(ipchars) {
        var bytes = ipchars.split('.');
        return ((bytes[0] & 0xff) << 24) |
            ((bytes[1] & 0xff) << 16) |
            ((bytes[2] & 0xff) <<  8) |
            (bytes[3] & 0xff);
    }
    return function (ipaddr, pattern, maskstr) {
        var match = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.exec(ipaddr);
        if (match[1] > 255 || match[2] > 255 ||
            match[3] > 255 || match[4] > 255) {
            return false;    // not an IP address
        }
        var host = convert_addr(ipaddr);
        var pat  = convert_addr(pattern);
        var mask = convert_addr(maskstr);
        return ((host & mask) == (pat & mask));
    };
}();
"""
    testfun = """var assert = require('assert');
assert.equal("DIRECT",FindProxyForURL('http://t.cn', 't.cn'));
assert.equal("%s",FindProxyForURL('http://www.youtube.com', 'www.youtube.com'));
""" % os.environ['TESTPXY']

    fh = open('wpad.dat', 'w')
    fh.write(tempfun)
    fh.close()
    fh = open('wpadtest.js', 'w')
    fh.write(fundef)
    fh.write(tempfun)
    fh.write('\n'+testfun);
    fh.close()
    argc = len(sys.argv)
    print "param size: %d" % argc
    for i in range(1,argc,2):
        print "i=%d argv=%s" % (i, sys.argv[i])
    print 'done'

if __name__ == '__main__':
    build()
