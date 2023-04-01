// ==UserScript==
// @name         url验证
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       weaponchua
// @match        http://*/*
// @match        https://*/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @require      https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js
// @grant        none
// ==/UserScript==

window.alert = alert;
function alert(data, callback) { //回调函数
    var alert_bg = document.createElement('div'),
    alert_box = document.createElement('div'),
        alert_text = document.createElement('div'),
        alert_btn = document.createElement('div'),
        textNode = document.createTextNode(data ? data : ''),
        btnText = document.createTextNode('确 定');

    // 控制样式
    css(alert_bg, {//背景颜色设置
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'right': '0',
        'bottom': '0',
        'background-color': 'rgba(0, 0, 0, 0.1)',
        'z-index': '999999999'
    });

    css(alert_box, {//控制盒子大小、背景颜色上下边距
        'width': '540px',
        'max-width': '90%',
        'font-size': '16px',
        'text-align': 'center',
        'background-color': '#fff',
        'border-radius': '15px',
        'position': 'absolute',
        'top': '50%',
        'left': '50%',
        'transform': 'translate(-50%, -50%)'
    });

    css(alert_text, {
        'padding': '10px 15px',
        'border-bottom': '1px solid #ddd'
    });

    css(alert_btn, {
        'padding': '10px 0',
        'color': '#007aff',
        'font-weight': '600',
        'cursor': 'pointer'
    });

    // 内部结构套入
    alert_text.appendChild(textNode);
    alert_btn.appendChild(btnText);
    alert_box.appendChild(alert_text);
    alert_box.appendChild(alert_btn);
    alert_bg.appendChild(alert_box);

    // 总体显示到页面内
    document.getElementsByTagName('body')[0].appendChild(alert_bg);

    // 肯定绑定点击事件删除标签
    alert_btn.onclick = function() {
        alert_bg.parentNode.removeChild(alert_bg);
        if (typeof callback === 'function') {
            callback(); //回调
        }
    }
}

function css(targetObj, cssObj) {
    var str = targetObj.getAttribute("style") ? targetObj.getAttribute('style') : '';
    for (var i in cssObj) {
        str += i + ':' + cssObj[i] + ';';
    }
    targetObj.style.cssText = str;
}

var url = window.location.href; //获取网页的url
    console.log(url)
    async function getResult() {
        try {
            const response = await axios.get('http://127.0.0.1:8001/bishe/testioc/', {
                params: {
                    url: url
                }
            });
            let data = response.data;
            if (data.flag==1) {
                // 说明, 成功发送请求,且网站有问题
                alert(data.str)
            }

        } catch (error) {
          console.error(error);
        }
    }
    getResult();