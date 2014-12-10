function escape_command(str) {
  var alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  var result = "";
  for (var i = 0; i < str.length; i++) {
     if (str[i] == '/')
      result += '_';
    else if (alpha.indexOf(str[i]) == -1)
      result += "\\"+str[i];
    else
      result += str[i];
  }
  return result;
};

function thunder_url_fix(lixian_url, filename) {
    var tid = lixian_url.match(/&tid=([^&]+)/)[1];
    var fid = lixian_url.match(/fid=([^&]+)/)[1];
    if (fid && tid)
      return ThunderEncode("http://sendfile.vip.xunlei.com/"+encodeURIComponent(filename)+"?fid="+fid+"&mid=666&threshold=150&tid="+tid);
    return "";
}

var LE = {
  export: function(gen) {
    LE.show(gen(LE.taskname, LE.links(), LE.cookie));
  },
  download: function(gen) {
    gen(LE.taskname, LE.links(), LE.cookie);
  },
  wget_links: function() {
    LE.export(function(taskname, links, cookie) {
      var str = "";
      $.each(links, function(i, n) {
        str += "wget -c -O "+escape_command(n.title)+" --header 'Cookie:"+cookie+";' '"+n.url+"'\n";
      });
      return str;
    });
  },
  aria2_links: function() {
    function multiple_server_fix(url) {
       return "'"+url.replace("gdl", "'{gdl,dl.{f,g,h,i,twin}}'")+"'";
    }
    LE.export(function(taskname, links, cookie) {
      var str = "";
      $.each(links, function(i, n) {
        str += "aria2c -c -s16 -x16 -k1M --out "+escape_command(n.title)+" --header 'Cookie:"+cookie+";' "+multiple_server_fix(n.url)+"\n";
      });
      return str;
    });
  },
  to_aria2: function() {
    LE.download(function(taskname, links, cookie) {
      var path = $.cookie('aria2-jsonrpc');
      if (path && path != '') {
        var aria2 = new ARIA2(path);
        $.each(links, function(i, n) {
          aria2.addUri(n.url, {out: n.title, header: 'Cookie: '+cookie});
        });
        $("#tip-box").css("left", "48%").html("导出完成").show(0).delay(3000).hide(0);
      } else {
        $("#tip-box").css("left", "44%").html("尚未设置 Aria2 JSON-RPC Path").show(0).delay(3000).hide(0);
      }

    });
  },

  lixian_links: function() {
    LE.export(function(taskname, links, cookie) {
      var str = "";
      $.each(links, function(i, n) {
        str += thunder_url_fix(n.url, n.title)+"\n";
      });
      return str;
    });
  },

  default_script: function sample(taskname, links, cookie) {
  var str = "====== sample output ======\n== 右键点击\"自定义\"编辑 ==\n";
  str += "taskname = "+taskname+"\n";
  str += "escape_command(taskname) = "+escape_command(taskname)+"\n";
  str += "cookie = "+cookie+"\n";
  str += "==========================\n";
  $.each(links, function(i, n) {
    str += "links["+i+"].title = "+n.title+"\n";
    str += "links["+i+"].url = "+n.url+"\n";
  });
  return str;
},
  custom: function() {
    LE.export(LE.custom_script || LE.default_script);
  },
};
if (localStorage && localStorage.custom_script) {
  eval("LE.custom_script = "+localStorage.custom_script);
}

var LS = {
  share: function(url) {
    window.open(url,"","width=480,height=480,left="+Number((window.screen.width-480)/2)+",top="+Number((window.screen.width-480)/2)+",scrollbars=no");
  },
  share_copy: function() {
    window.prompt("复制分享地址", LS.share_url);
  },
  share_google: function() {
    LS.share("https://plusone.google.com/_/+1/confirm?url="+LS.share_url+"&title="+LS.share_title);
  },
  share_twitter: function() {
    LS.share("https://twitter.com/intent/tweet?source=webclient&text="+LS.share_title+"&url="+LS.share_url);
  },
  share_sina: function() {
    LS.share("http://v.t.sina.com.cn/share/share.php?url="+LS.share_url+"&title="+LS.share_title);
  },
  share_qq: function() {
    LS.share("http://v.t.qq.com/share/share.php?url="+LS.share_url+"&title="+LS.share_title);
  },
  share_douban: function() {
    LS.share("http://www.douban.com/recommend/?url="+LS.share_url+"&title="+LS.share_title);
  },
};
