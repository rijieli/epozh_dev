---
layout: post
title: 一种 Markdown 语法分析策略
date: 2021-06-06 12:12:40 +0800
categories: 开发
show_excerpt_image: false
---

> 原文链接：https://spec.commonmark.org/0.29/#appendix-a-parsing-strategy

> 未定翻译或者难以直译内容两端以百分号 % 标注，欢迎反馈 github@rijieli/commonmark-spec-translation


在本附录中，我们描述了 CommonMark 参考实现中使用的语法分析策略的一些特性。

## 概述

语法分析有两个阶段： 

1. 在第一阶段，输入的行被分析并且文档的块结构---段落、块引用、列表项等等被构建。文本会被分配给这些块但不会被进一步分析。链接引用定义会被解析并构建一个链接映射表。

2. 在第二阶段，段落原始文本内容和标题等被解析为 Markdown 内联元素序列（字符串、行内代码、链接、强调等），第一阶段构建的链接映射表将参与这个解析过程。

处理中的每个点，文档都被表示为一棵由 **blocks** 组成的树。树的根节点是一个 `document` 块。`document` 节点可以有任意数量的其他块作为**子节点**。相对的，这些子节点也可以将其他块作为子节点。一个块最后的子节点通常被认为是 **open** 的，这意味着后续的输入行可以改变其内容。（未打开的块是 **closed**。）举例而言，下方是一棵可能的文档树，其中打开的块用箭头标记：

``` tree
-> document
  -> block_quote
       paragraph
         "Lorem ipsum dolor\nsit amet."
    -> list (type=bullet tight=true bullet_char=-)
         list_item
           paragraph
             "Qui *quodsi iracundia*"
      -> list_item
        -> paragraph
             "aliquando id"
```

## 阶段 1：块结构

每一行的解析都有可能对这棵树的结构产生影响。输入的行会被解析，并且根据其内容，通过以下一种或多种方式进行改动： 

1. 一个或多个打开的块被关闭。
2. 创建一个或多个新块作为最后一个打开块的子代。
3. 文本会被附加到树上剩余的最后（深）的一个开放的块。

当一行被以如上方式合并到树中后，它可以被丢弃，因此可以以流的方式读取输入。

对于每一行，我们遵循以下过程：

1. 首先，我们遍历打开的块，从根节点 `document` 开始，向下遍历到最后一个子节点，直到最后一个打开的块。一个块如果处于打开状态则必须满足一定条件。例如，代表引用的块需要一个 `>` 字符。一个段落块至少需要一个非空行。在这个阶段，我们可能会匹配所有或部分开放块。但是不能关闭未匹配的块，因为可能存在一个惰性延续行[[lazy continuation line](https://spec.commonmark.org/0.29/#lazy-continuation-line)]。

2. 接下来，在使用现有块的延续标记（原文：continuation markers）之后，我们寻找新的块开始标记符号（例如，代表引用的`>`）。如果我们遇到一个新的开始标记，我们会在创建新的块之前关闭步骤 1 中未匹配的所有块，并将新的块作为最后一个匹配到的开放子块。

3. 最后，我们查看该行的剩余部分（在块标记如 `>`、列表标记和缩进被解析之后剩下的部分）。这些剩余的文本可以合并到最后一个打开的块（段落、代码块、标题或原始 HTML）中。

当我们看到段落块中的一行是[[setext heading underline](https://spec.commonmark.org/0.29/#setext-heading-underline)]时，构造一个 Setext 标题块。

当一个段落块被关闭时会解析引用链接定义；分析累积的行以检查它们是否以一个或多个引用链接定义标记开始。任何剩余部分标记为正常段落。

通过四行 Markdown 文本，我们来了解上面的树是如何生成的：

```
> Lorem ipsum dolor
sit amet.
> - Qui *quodsi iracundia*
> - aliquando id
```

一开始，我们的文档模型只包含根节点

``` tree
-> document
```

我们文字的第一行

```
> Lorem ipsum dolor
```

将创建一个 `block_quote` 节点作为第一个子节点，同时还将创建一个 `paragraph` 节点作为 `block_quote` 的子节点。剩余的文本被添加到最后一个打开的块节点 `paragraph` 中

``` tree
-> document
  -> block_quote
    -> paragraph
         "Lorem ipsum dolor"
```

下一行，

```
sit amet.
```

是打开的块节点 `paragraph` 的“惰性延续”，因此它也会被添加到`paragraph`节点的文本中：

``` tree
-> document
  -> block_quote
    -> paragraph
         "Lorem ipsum dolor\nsit amet."
```

第三行， 

```
> - Qui *quodsi iracundia*
```

导致 `paragraph` 块被关闭，同时还将创建一个新的 `list` 节点作为 `block_quote` 的子节点。一个新的 `list_item` 也被添加为 `list` 的子节点，一个 `paragraph` 节点作为 `list_item` 的子节点被创建。剩余的文本将被添加到这个 `paragraph` 中：

``` tree
-> document
  -> block_quote
       paragraph
         "Lorem ipsum dolor\nsit amet."
    -> list (type=bullet tight=true bullet_char=-)
      -> list_item
        -> paragraph
             "Qui *quodsi iracundia*"
```

第四行

```
> - aliquando id
```

导致上一行创建的 `list_item`（及其子节点 `paragraph`）被关闭，一个新的 `list_item` 作为 `list` 的子节点被打开。一个 `paragraph` 被添加为新的 `list_item` 的子节点用来保存剩余文本。

我们因此获得了最终的语法树：

``` tree
-> document
  -> block_quote
       paragraph
         "Lorem ipsum dolor\nsit amet."
    -> list (type=bullet tight=true bullet_char=-)
         list_item
           paragraph
             "Qui *quodsi iracundia*"
      -> list_item
        -> paragraph
             "aliquando id"
```

## 阶段 2: 内联结构

当所有的输入都被解析，所有打开的块都被关闭。

我们将遍历树访问每个节点，并将段落和标题的原始文本内容解析为内联节点。至此，我们已经获取了所有的链接引用定义，我们可以随时解析引用链接。

``` tree
document
  block_quote
    paragraph
      str "Lorem ipsum dolor"
      softbreak
      str "sit amet."
    list (type=bullet tight=true bullet_char=-)
      list_item
        paragraph
          str "Qui "
          emph
            str "quodsi iracundia"
      list_item
        paragraph
          str "aliquando id"
```

注意第一个 `paragraph` 中的换行符被解析为 `softbreak`，第一个列表项中的星号变成了一个 `emph` 节点。

### 解析嵌套强调和链接的算法

到目前为止，内联解析最棘手的部分是处理强调、加粗、链接和图像。下面的算法将帮助我们实现这个过程。

当我们开始解析内联节点并且遇到

- 一连串 `*` 或 `_` 字符，或者
- 一个 `[` 或 `![` 时

我们插入一个文本节点，并将这些符号作为内容，然后向 delimiter stack [分隔符堆栈](https://spec.commonmark.org/0.29/#delimiter-stack)添加这个节点的指针。

[分隔符堆栈](https://spec.commonmark.org/0.29/#delimiter-stack)是一个双向链表。每个元素都包含一个指向文本节点的指针，以及

- 分隔符的类型（`[`、`![`、`*`、`_`）
- 分隔符的数量，
- 分隔符是否为 *active* 状态（所有的起始标记都是激活状态的），以及
- 分隔符是否为潜在的 opener、潜在的 closer 还是两者（这取决于在分隔符之前和之后的字符）。

当我们遇到 `]` 字符时，我们调用 *查找链接或图像* 过程（见下文）。

当我们到达输入的末尾时，我们调用 *处理强调* 过程（见下文），同时赋值给 `stack_bottom` = NULL。

(译者注：该部分涉及的内联节点均具有两端为分隔符，中间为内容的特点，上文的 opener 和 closer 指代一个内联节点两端的分隔符)

#### *查找链接或图像*

从分隔符堆栈的顶部开始，我们向下查看堆栈寻找一个 opener `[` 或 `![` 分隔符。

- 如果我们没有找到，我们返回一个文字文本节点`]`。

- 如果我们确实找到了一个，但它不是 *active*，我们从堆栈中删除不活动的分隔符，并返回一个文字文本节点 `]`。

- 如果我们找到一个并且它处于 *active* 状态，那么我们会向前解析以查看是否有内联链接/图像、引用链接/图像、紧凑引用链接/图像或快捷方式引用链接/图像。

  + 如果我们不这样做，那么我们从分隔符堆栈中删除这个 opener 分隔符并返回一个文本节点 `]`。
  
  + 如果我们这样做，那么
  
    * 我们返回一个链接或图像节点，其子节点是内联在 opener 分隔符指向的文本节点之后。
    
    * 在将 opener `[` 分隔符指针赋值给 `stack_bottom` 之后，我们在这些内联节点上运行 *处理强调* 过程。
    
    * 从堆栈中删除 opener。
    
    * 如果我们有一个链接（而不是图像），我们还将 opener 之前的所有 `[` 分隔符设置为 *inactive*。（这将防止我们获得链接内的链接。）
    
#### *处理强调*

参数 `stack_bottom` 决定了我们在 *分隔符堆栈* 中向下查找的最终位置。如果它是 NULL，我们可以一直搜索堆栈的底部。否则我们会在 `stack_bottom` 之前停止。

让 `current_position` 指向 *分隔符堆栈* 上位于 `stack_bottom` 上方的元素（或者第一个元素，如果 `stack_bottom` 为 NULL 的话）。

%我们跟踪每个分隔符类型（`*`、`_`）和每个结束分隔符运行的长度（模 3）的 `openers_bottom`。将其初始化为 `stack_bottom`。%

然后我们重复以下操作，直到我们用尽所有潜在的 closer：

- 移动 `current_position` 在分隔符堆栈中向上搜索（如果需要），直到发现第一个潜在的 closer 分隔符（`*` 或 `_`）的位置。（这将是最接近%输入开头%的潜在 closer -- 解析顺序中的第一个。） 

- 现在，回看一下堆栈中（停留在此分隔符类型的 `stack_bottom` 和 `openers_bottom` 上方）第一个匹配的潜在 opener（“匹配”意味着相同的分隔符）。

- 如果找到一个（译者注：满足上方条件的情况，既潜在的 opener 和 closer 被找到）：
  
  + 弄清楚是强调还是加粗：如果 opener 和 closer 的长度 >= 2 为加粗，否则为强调。
  
  + 在 opener 之后插入一个 emph 或 strong emph 节点。
  
  + 从分隔符堆栈中删除 opener 和 closer 之间的所有分隔符。
  
  + 从开始和结束文本节点中删除 1（对于常规 emph）或 2（对于强 emph）分隔符。如果删除后变为空文本，则删除它们并删除定界符堆栈中相应元素。如果 closer 节点被移除，则将 `current_position` 重置为堆栈中的下一个元素。

- 如果没有找到：
  
  + 将 `openers_bottom` 设置为 `current_position` 上方的元素。（我们知道堆栈中没有 opener 对应的 closer，因此这一步为未来的搜索设置了下限。）
  
  + 如果 `current_position` 的 closer 不是潜在的 opener，将其从分隔符堆栈中删除（因为我们知道它也不是一个 closer）。
  
  + 将 `current_position` 移动到堆栈中的下一个元素。
  
完成后，我们从分隔符堆栈中删除 `stack_bottom` 上方的所有分隔符。
