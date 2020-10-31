// 设置无匹配时返回数据
// 按分类展示关键字

(function () {
    "use strict";
    let siteMapData = { "post": [] };
    let searchAPIStatus = 200;
    let searchInputField = document.querySelector("#search-input-field");
    let searchIcon = document.querySelector("#search-icon");
    let searchResultDomNode = document.querySelector("#search-result");

    let globalSearchInputField = document.querySelector("#global-search-input-field");
    let globalSearchClearButton = document.querySelector("#global-search-clear");
    let globalSearchResultDomNode = document.querySelector("#global-search-result");

    let categoryMap = { "post": "博客", "work": "工作", "code": "CODE", "category": "分类" };

    searchIcon.addEventListener("click", toggleSearchInput);

    function toggleSearchInput() {
        searchInputField.classList.toggle("hidden");
        searchInputField.focus();
    }

    function debounce(func, wait) {
        let timeout;

        return function () {
            if (timeout) clearTimeout(timeout);
            timeout = setTimeout(function () {
                func.apply(this, arguments);
            }, wait);
        }
    }

    function parseQueryParameter() {
        let queryString = window.location.search;
        if (queryString.startsWith("?")) queryString = queryString.slice(1);
        let result = {};
        queryString.split("&").forEach(elm => {
            let element = elm.split("=");
            let queryValue = element[1].replaceAll("+", " ");
            queryValue = decodeURIComponent(queryValue).trim();
            result[decodeURIComponent(element[0])] = queryValue;
        })
        return result;
    }

    // 获取初始文档
    function fetchSitemap() {
        if (this.status != 200) {
            searchAPIStatus = 500;
            return;
        }

        let content = document.createElement("p");
        content.innerText = this.responseText;

        siteMapData = JSON.parse(this.responseText);
    }

    function matchPattern(keyword, item) {
        let result = false;
        // Not Safe
        // if(item.search(new RegExp(keyword, "i")) != -1) result = true;
        if (item.toLowerCase().indexOf(keyword.toLowerCase()) != -1) result = true;

        return result;
    }

    function processData(keyword, resultNode, resultLimit) {

        let result = {};
        let resultCount = 0;

        keyword = keyword.trim();

        for (let category in siteMapData) {
            result[category] = [];
            if (siteMapData[category].length > 0) {
                siteMapData[category].forEach(item => {
                    if (matchPattern(keyword, item["title"])) {
                        result[category].push(item);
                        resultCount++;
                    }
                })
            }
        }

        let searchResult = [];

        for (let category in result) {
            if (result[category].length > 0) {
                searchResult.push(assembleResult(keyword, category, result[category], resultLimit));
            }
        }

        searchResult.forEach(domNode => {
            resultNode.appendChild(domNode);
        })
    }

    function assembleResult(keyword, category, matchedItems, resultLimit) {
        let resultGroupDivNode = document.createElement("div");
        resultGroupDivNode.classList.add("result-group");
        let titleNode = document.createElement("div");
        titleNode.classList.add("search-result-title");
        let titleTextNode = document.createElement("h3");
        titleTextNode.innerText = categoryMap[category.toLowerCase()];

        titleNode.appendChild(titleTextNode);
        resultGroupDivNode.appendChild(titleNode);
        let ulNode = document.createElement("ul");

        if (resultLimit != -1 && matchedItems.length > resultLimit) {
            matchedItems = matchedItems.slice(0, resultLimit);
            let moreResultANode = document.createElement("a");
            moreResultANode.href = "/search?q=" + escape(keyword);
            moreResultANode.innerText = "MORE";
            titleNode.appendChild(moreResultANode);
        }

        matchedItems.forEach(item => {
            ulNode.appendChild(generateDom(item["title"], item["url"]));
        })

        resultGroupDivNode.appendChild(ulNode);

        return resultGroupDivNode;
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

    function searchInput() {
        searchResultDomNode.innerHTML = "";
        searchResultDomNode.classList.remove("hidden");

        let KEYWORD = searchInputField.value.trim();
        if (KEYWORD.length > 0) processData(KEYWORD, searchResultDomNode, 3);
    }

    function globalSearchInput() {
        globalSearchResultDomNode.innerHTML = "";
        let KEYWORD = globalSearchInputField.value.trim();
        if (KEYWORD.length > 0) processData(KEYWORD, globalSearchResultDomNode, -1);
    }

    function initSearchComponent() {

        let searchInputHander = debounce(searchInput, 300);
        let globalSearchInputHander = debounce(globalSearchInput, 300);

        searchInputField.addEventListener("input", searchInputHander);
        if (globalSearchInputField) globalSearchInputField.addEventListener("input", globalSearchInputHander);
        if (globalSearchClearButton) globalSearchClearButton.addEventListener("click", e => {
            globalSearchInputField.value = "";
        })

        document.body.addEventListener("click", () => {
            searchResultDomNode.classList.add("hidden");
        });

        if (globalSearchInputField) {
            let queryString = parseQueryParameter();
            if (queryString["q"]) {
                globalSearchInputField.value = queryString["q"];
                processData(queryString["q"], globalSearchResultDomNode, -1);
            }
        }
    }

    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", fetchSitemap);
    oReq.addEventListener("loadend", initSearchComponent);
    oReq.open("GET", "/sitemap.json");
    oReq.send();
})()

