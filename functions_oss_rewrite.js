function handler(event) {
    //获取request，request中字段信息可参考https://docs.aws.amazon.com/zh_cn/AmazonCloudFront/latest/DeveloperGuide/functions-event-structure.html#functions-event-structure-query-header-cookie
    var request = event.request;
    var uri = request.uri;
    // console.log('1:'+request.querystring['x-oss-process'].value);
    var re = /(.+)_([0-9,a-z]+).png/i; 
    //通过正则匹配抓出后缀中_前一段的字符串以及size的大小
    var arr = uri.match(re);
    var re_num = /([0-9]+)/i;
    var size = arr[2].match(re_num);
    //构造新uri
    var new_uri = arr[1] + '.png';
    // var query_value = 'image/resize,m_lfit,w_' + size[1]+ '/format,webp/quality,Q_80';
    //基于size，构造查询字符串，并放进request.querystring中
    request.querystring['x-oss-process'] = {value: 'image/resize,m_lfit,w_' + size[1]+ '/format,webp/quality,Q_80'};
    console.log('2:'+request.querystring['x-oss-process'].value);
    console.log('3'+new_uri)
    //新uri放进request.uri中
    request.uri = new_uri;
    //返回request
    return request;
}
