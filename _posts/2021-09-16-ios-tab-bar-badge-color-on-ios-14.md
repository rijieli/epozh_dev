---
layout: post
title: iOS Tab Bar Badge 颜色与样式配置
date: 2021-09-16 14:42:57 +0800
categories: iOS UI
show_excerpt_image: true
---

在配置 Tab Bar Badge 样式时发现 `badgeColor` 配置失效，开发版本 iOS 13.6+。

## badgeColor

根据文档描述 Tab Bar Badge 颜色可以直接在 `UITabBarItem.badgeColor` 进行配置。尝试如下配置，并在 Badge 更新后打印颜色。

```swift
tabBar.items!.forEach( $0.badgeColor = .orange)

func onBadgeUpdate() {
    print(self.tabBar.items!.map { $0.badgeColor })
}
```

实际效果与打印结果如下，可以见到属性确实被修改了，但展示出来的是 systemRed 颜色。

![](/assets/posts/ios-tab-bar-badge-color-on-ios-14/1.jpeg)

```
<UIDynamicCatalogColor: 0x281300af0; name = Orange>), 
<UIDynamicCatalogColor: 0x281300e10; name = Orange>), 
<UIDynamicCatalogColor: 0x2813010e0; name = Orange>)
```

## 无效原因

留意到在 UITabBarController 初始化时自定义了 `standardAppearance`，它的优先级高于直接在 UITabBarItem 配置的样式。

```swift
self.tabBar.standardAppearance = {
    let appearance = UITabBarAppearance()
    ...
    return appearance
}()
```

## 正确配置方式

`tabBar.standardAppearance` 包含 `stackedLayoutAppearance`属性，这里包含 badge 的配吹，可以在定义 Tab Bar 样式时修改该属性。方法如下:

```swift
let customTabItemAppearance = UITabBarItemAppearance()
customTabItemAppearance.configureWithDefault(for: .inline)
customTabItemAppearance.normal.badgeBackgroundColor = .systemBlue
customTabItemAppearance.selected.badgeBackgroundColor = .systemBlue

self.tabBar.standardAppearance = {
    let appearance = UITabBarAppearance()
    ...
    appearance.stackedLayoutAppearance = customTabItemAppearance
    return appearance
}()
```


## 结论

UITabBarAppearance 优先级高于其他配置，如果想要采用 `badgeColor` 这种简便的方式修改颜色，需要确认自己**没有**定义过 Tab Bar 的样式。或者在定义 Tab Bar 样式时，通过 `stackedLayoutAppearance` 对 badge 样式进行配置。