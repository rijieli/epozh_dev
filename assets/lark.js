window.h5sdk.ready(() => {

    window.h5sdk.biz.navigation.setTitle({ title: "慢一 | 飞书" });

    window.h5sdk.biz.navigation.setMenu({
        items: [
            { id: "1", text: '分享' },
            { id: "2", text: "搜索" }
        ],
        onSuccess: data => {
            if (data.id === "1") {
                window.h5sdk.biz.util.share({
                    url: window.location.href,
                    title: document.title,
                    content: "分享来自 Manyi 的一篇文章",
                    image: "https://manyibit.cn/assets/img/global-share-image.png",
                    onSuccess: data => {
                    }
                });
            } else if (data.id === "2") {
                window.h5sdk.biz.util.openLink({
                    url: window.location.origin + "/search",
                    title: "搜索",
                    newTab: false
                });
            }
        }
    });
});
