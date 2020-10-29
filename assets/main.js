// 数据结构
// JSON - 自定义分类 - 自定义数据 URL
// 分类
// - 标题
// - URL

// 获取索引 JSON
// 匹配关键字并返回结果
// 设置无匹配时返回数据
// 按分类展示关键字
// TODO: 阻止 submit 提交
// TODO：默认渲染最新几篇文章
(function () {
    "use strict";
    let searchData = { "post": [] };
    let searchAPIStatus = 200;
    let searchInputField = document.querySelector("#search-input-field");
    let searchListDomNode = document.querySelector("#search-list");

    function debounce(func, wait) {
        let timeout;

        return function () {
            if (timeout) clearTimeout(timeout);
            timeout = setTimeout(function () {
                func.apply(this, arguments);
            }, wait);
        }
    }

    function requestListener() {
        if (this.status != 200) {
            searchAPIStatus = 500;
            return;
        }

        let content = document.createElement("p");
        content.innerText = this.responseText;
        // document.querySelector("#content").appendChild(content);

        searchData = JSON.parse(this.responseText);
    }

    function processData(keyword) {

        let result = {"post": []};

        for(let item of searchData["post"]) {
            if(item["title"].search(new RegExp(keyword, "i")) != -1) {
                result["post"].push(item)
            }
        }

        console.log(result);
        searchListDomNode.appendChild(generateDom(result["post"][0]["title"], result["post"][0]["url"]));
    }

    function generateDom(title, url) {
        let liDomNode = document.createElement("li");
        liDomNode.classList.add("search-list-item");
        let domNode = document.createElement("a");
        domNode.href = url;
        domNode.appendChild(document.createTextNode(title));
        liDomNode.appendChild(domNode);
        return liDomNode;
    }

    function handleInput() {

        let KEYWORD = searchInputField.value.trim();

        processData(KEYWORD);
    }

    let inputFunc = debounce(handleInput, 500);

    searchInputField.addEventListener("input", inputFunc);

    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", requestListener);
    oReq.open("GET", "/search.json");
    oReq.send();
})()

