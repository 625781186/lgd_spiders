# !/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/18 15:01
# @Author  : lgd
# @Project : lgd-Crawler
# @File    : xiaoshuo.py
# /***


import requests
import json
import os
import execjs
# from lxml import etree



url = 'https://g.hongshu.com/bookajax/chapterlist/bid/93416.do'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'referer': 'https://g.hongshu.com/chapterlist/93416.do',
    'cookie': 'pgv_pvi=5242139648; pgv_si=s7513097216; Hm_lvt_e966b218bafd5e76f0872a21b1474006=1566110745; yqksid=d53h5g86mq6n5vvjs0rcuprvq5; bookfav=%7B%22b93416%22%3A0%7D; Hm_lpvt_e966b218bafd5e76f0872a21b1474006=1566115219',

}

# res = requests.get(url, headers=headers, verify=False)
# text = json.loads(res.text)
# for i in text['list']:
#     print('https://g.hongshu.com/content/{0}/{1}.html'.format(i['bid'], i['chapterid']))


detail_url = 'https://g.hongshu.com/content/93416/13901181.html'
detail = requests.get(detail_url, headers=headers, verify=False)
print(detail.text)


jscode = execjs.compile("""
<script type="text/javascript">
    var bid = 93416, chpid = 13901181, isvip = 0, cidx = 2;
    var zhuangtai="";
    function changemode(num){
       if (num=='0') {
        var htmls='<a class="blackday radius4" onclick="changemode(1);"><img src="https://img2.hongshu.com/Public/Client/wap/1.3.5/images/ic_brightness.png" /></a>';
        $('#wz').removeClass('rdbg rdbg_black');
        writeCookie('blackwhite','0',9999999);
       }else{
        var htmls='<a class="whiteday radius4" onclick="changemode(0);"><img src="https://img2.hongshu.com/Public/Client/wap/1.3.5/images/ic_flare.png" /></a>';
        $('#wz').addClass('rdbg rdbg_black');
        writeCookie('blackwhite','1',9999999);
       }
       $('#mode').html(htmls);
    }
    
    //面包屑滚动
    function gundong(){
        var _top = scrollTop();
        var _height = $(window).height();
        var read_top = 48;

        //左侧菜单
        var pos = {top: 0}
        if(_top>read_top){
            pos.top = _top-read_top;
        }
        /*var zfd_height = $('.zuofudong').offset().height;
        if(read_height < zfd_height+pos.top){
            pos.top = read_height - zfd_height-100;
        }*/
        $('#mianbaoxie').css(pos);
    }

    Do.ready('common','functions', function(){
    gundong();
        document.onscroll=function(){
            gundong();
        }
    });

    //添加到书架
    function InsertFav(bid){
        if(!bid){
            hg_Toast('缺少参数');
            return false;
        }
        var data = {
            bid:bid,
        }
        var url = "/userajax/insertfav.do";
        $.ajax({
            type:'get',
            url: url,
            data:data,
            success: function (data){
                if(data.status == 1){
                   hg_Toast(data.message);
                   $('#collect').hide();
                }else{
                    hg_Toast(data.message);
                    if(data.url){
                        window.location.href = data.url;
                    }
                }
            }
        })
    }
    //获取上下章
    function getPreNextChapter(){
        var data = {
            bid:93416,
            chpid:13901181        }
        var url = "/bookajax/getprenextchapter.do";
        $.ajax({
            type:'get',
            url: url,
            data:data,
            success: function (data){
                if(data.status == 1){
                   var htmls=template('shangyizhang',data);
                   $('#zhangjieinfo').html(htmls);
                   if(zhuangtai=="isxiajia"){
                     var htmls=template('xiajia_tpl',data);
                   $('#zhangjieinfo').html(htmls);
                   }
                }
            }
        })
    }

    //设置字体,当前16px
    function ChangeFontSize(type){
        //获取当前字体
        var cookiefont = parseInt(cookieOperate("fontsize"));
        if(!cookiefont){
            var	fontsize = parseInt($(".rdtext").attr("fsize"));
        }else{
            var fontsize = cookiefont;
        }
        if(type == "add"){
            fontsize = fontsize+2;
        }else if(type == "minus"){
            fontsize = fontsize-2;
        }

        if(fontsize > 20){
            fontsize = 20;
        }else if(fontsize < 12){
            fontsize = 12;
        }

        writeCookie("fontsize",fontsize,86400);
        $(".rdtext>p").css("font-size",fontsize+"px");
        $(".rdtext").attr("fsize",fontsize);
    }

    //屏蔽一下可能会出现的复制等操作，虽然在移动端、手机浏览器端没多大用处
    document.onselectstart = function(e) {
        return false;
    }
    document.oncontextmenu = function(e) {
        return false;
    }

    function quxiao(){
        $('#collect').hide();
        writeCookie('shoucang',93416,99999);
    }

    //获取书籍状态
    function getBookStatus(){
        var data = {
                bid:'93416',
            }
        var url = "https://g.hongshu.com/getBookInfo.do";
        $.ajax({
            type:'post',
            url: url,
            data:data,
            success: function (data){
                //检测收藏
                if(data.isfav == 0){
                    Do.ready('template',function(){
                        $('#shoucang').show();
                        var quxiao=cookieOperate('shoucang');
                        if(quxiao == 93416){
                            $('#shoucang').hide();
                        }
                    });
                }
                //获取书籍状态
                if(data.isxiajia == true){
                    $('#collect').html("对不起，本书已下架！");
                    $('#bookname').attr("href","/book/xiajia.do");
                    $('#mulu').attr("href","/book/xiajia.do");
                    Do.ready('template',function(){
                       var htmls=template('xiajia_tpl');
                       $('#zhangjieinfo').html(htmls);
                    });
                    zhuangtai="isxiajia";
                }
            }
        });
    }

    //改变背景模式
    Do.ready('functions','template',function(){
        getPreNextChapter();
        //1 黑夜  0 白天
        var bgnum = cookieOperate('blackwhite');
        if(bgnum!=1) {
            bgnum = 0;
        }
        if (bgnum==1) {
            $('#wz').addClass('rdbg_black');
            var htmls='<a class="whiteday radius4" onclick="changemode(0);"><img src="https://img2.hongshu.com/Public/Client/wap/1.3.5/images/ic_flare.png" /></a>';
        }else{
            $('#wz').removeClass('rdbg_black');
            var htmls='<a class="blackday radius4" onclick="changemode(1);"><img src="https://img2.hongshu.com/Public/Client/wap/1.3.5/images/ic_brightness.png" /></a>';
        }
        //$('#wz').show();
        $('#mode').html(htmls);
        ChangeFontSize();
        updateReadLog(bid, chpid, cidx, isvip);
    });
    Do.ready('lazyload',function(){
            Lazy.Load();
            document.onscroll = function(){
                Lazy.Load();
        };
    });

    Do.ready("common", 'functions',function(){
        if(!checkBookFav(bid)) {
            var quxiao=cookieOperate('shoucang');
            if(quxiao == 93416){
                $('#shoucang').hide();
            } else {
                $('#shoucang').show();
            }
        }
        UserManager.addListener(function(userinfo){
            $('.okbtn').on('click',function(){
                if(userinfo.islogin){
                    InsertFav(93416,13901181);
                }else{
                    hg_Toast('请先登录');
                }
            });
        });
        getBookStatus();
    });

    Do.ready('template',function(){
        var data={};
        data.sex_flag=cookieOperate('sex_flag');
        if(!data.sex_flag){
            data.sex_flag="nv";
        }
        var htmls=template('shouyeinfo',data);
        $('#shouye').html(htmls);
    });

</script>
""")

# print(jscode)
# os.environ["EXECJS_RUNTIME"] = " PhantomJS"
# print(execjs.get().name)
# # print(execjs.eval("Date.now()"))
# print(execjs.eval(detail.text))



