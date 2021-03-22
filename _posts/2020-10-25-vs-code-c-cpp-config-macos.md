---
layout: post
title: VS Code 配置基本 C/C++ 开发环境[macOS]
date: 2020-10-25 22:12:19 +0800
categories: 工具
show_excerpt_image: true
hide_post: true
---

在了解如何使用 VS Code 编译调试 C/C++ 之前，先了解一下如何在终端里直接编译 C/C++ 文件。

macOS 系统不自带编译器，需要通过 Xcode 来获取必要的组件（主要为 clang）。可以直接在 App Store 安装 Xcode，但目前 Xcode 安装完大约占用 10 GB 以上空间，如果没有 iOS 开发的需要，可以在终端输入下方命令安装部分必要组件，只需**下载几百兆**即可。

```
sudo xcode-select -–install
```

## 在命令行编译 C++ 文件
安装好必要组件，创建一个 C 与 C++ 文件。编译指令上略有差异，如果不注意可能会报错 `clang: error: linker command failed with exit code 1`，这是因为 clang 默认将输入看作 C 语言文件，从而导致链接错误。

C++ 请使用 `clang -lstdc++ hello.cpp -o hello` 进行编译。
C 则可以不加 `-lstdc++` 这个选项，直接 `clang hello.cpp -o hello`进行编译。

> This is the case even with the old 4.2 GCC (I experienced this when I set up my unofficial iOS toolchain). gcc assumes C by default, and invokes the linker without linking to the C++ standard library; in contrast, g++ assumes C++ and links against the C++ standard library by default.  

参考资料来自 [StackOverflow](https://stackoverflow.com/questions/11852568/gcc-4-8-on-mac-os-x-10-8-throws-undefined-symbols-for-architecture-x86-64?lq=1)

## 安装 VS Code 必要插件
VS Code 有种类丰富的扩展插件，许多扩展插件更是编程语言官方或者大型厂商在维护，质量上有所保证。比如我们要用到的的 C/C++ 扩展就是微软在维护，点击 VS Code 扩展栏搜索“C++”然后安装即可。

## 用 VS Code 编译 C/C++ 文件
VS Code 编译功能采用 Task 的形式。在使用 Task 之前需要进行配置，告知编辑器具体的细节。

点击 VS Code 菜单栏 Terminal > Configure Tasks，选择 Clang++ build active file，之后会在工作目录创建 `.vscode/tasks.json` 配置文件。**按照下方配置好后**按下 `Command + Shift + B` 即可编译当前窗口的文件。编辑器中将鼠标移至各项名称可以查看参数的具体描述，也可以查看参考资料：[官网文档](https://code.visualstudio.com/docs/cpp/config-clang-mac)。

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "type": "shell",
            "label": "C/C++: clang++ build active file",
            "command": "/usr/bin/clang++",
            "args": [
                "--std=c++11",
                "${file}",
                "-o",
                "${workspaceFolder}/output/${fileBasenameNoExtension}"
            ],
            "options": {
                "cwd": "${workspaceFolder}"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

## 配置相关路径语言标准
按下 `Command + Shift + P` 选择 C/C++: Edit Configurations，然后进行下一步配置，这些信息可以帮助编辑器更准确的了解当前工程的信息，比如 C++ 的标准、头文件的位置等等。该项配置保存在 `.vscode/c_cpp_properties.json` 中。

```json
{
    "configurations": [
        {
            "name": "Mac",
            "includePath": [
                "${workspaceFolder}/**",
                "/Library/Developer/CommandLineTools/usr/include/c++/v1",
                "/usr/local/include",
                "/Library/Developer/CommandLineTools/usr/include"
            ],
            "defines": [],
            "macFrameworkPath": [
                "/Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk/System/Library/Frameworks"
            ],
            "compilerPath": "/usr/bin/clang",
            "cStandard": "c11",
            "cppStandard": "c++11",
            "intelliSenseMode": "clang-x64"
        }
    ],
    "version": 4
}
```

## 配置 Debug
菜单栏依次点击 Run > Add Configuration... 然后选择 C++ (GDB/LLDB)。之后会生成 `launch.json` 默认的配置文件。打上断点后，按下 F5 或者 Run > Start Debugging 进行调试。

## 配置代码格式化
在 VS Code 设置中找到 `C_Cpp.clang_format_fallbackStyle` ，通过以下选项来配置格式化风格。

```
{ BasedOnStyle: LLVM, UseTab: Never, IndentWidth: 4, TabWidth: 4, BreakBeforeBraces: Attach, AllowShortIfStatementsOnASingleLine: false, IndentCaseLabels: false, ColumnLimit: 0, AccessModifierOffset: -4 }
```

## 使用 Code Runner 插件快速编译运行
除了官方提供的 Task 形式编译，推荐一个非常优秀的插件，在 VS Code 插件中搜索 Code Runner 插件，作者为 Han Jun，然后在设置中找到 `code-runner.executorMap`。点击编辑设置找到 cpp 一项，参考下方形式配置，保存后点击编辑器右上角的三角按钮即可编译并运行：

```
"cpp": "cd $dir && clang++ --std=c++11 $fileName -o $workspaceRoot/output/$fileNameWithoutExt && $workspaceRoot/output/$fileNameWithoutExt",
```

如果你的程序需要在命令行交互，将 `code-runner.runInTerminal` 设置为 true，这样程序会在 Terminal 运行，此时可以在终端输入一些信息，对刷算法题非常友好。
