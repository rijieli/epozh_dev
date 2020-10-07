---
layout: post
title: Toc test new
date: 2020-10-07 09:55:16 +0800
categories: 技巧
show_excerpt_image: true
---

Spring 的核心是让事情变得简单一点。按照常理，简单背后往往需要一些规则来处理复杂的情况。学习框架没有必要提升到哲学角度，因此在学习 Spring 的核心理念只需要考虑一点“我学的和理解的是否在让事情变得简单”，如果没有则很可能是学习角度有误。

如何让事情变的简单一些。Spring 使用接口来使组件关系变得松散，并根据开发者的配置构建了组件依赖关系网络。而开发者需要的组件，常常由多个部分组成，Spring 根据预先配置好的关系网络匹配复杂组件所需要的基本组件并且装配好(context)，当开发者需要时可以直接向 Spring 索取(context.getBean)。

## 开始学习前的准备
配置一个可以快速运行并显示结果的 Spring Framework 项目。

## Spring 配置
Spring 配置意味着人为定义好组件的依赖关系，以便 Spring 初始化，当需要一个组件时候由 Spring 提供。包含 Java 配置与 XML 配置。对于 Java 配置`@Component @ComponentScan @Configuration @Bean @Named @Autowired @Import @ImportResource` 为常用注解。

## 自动装配也叫依赖注入
依赖注入并非完全的自动化，第一次使用仍然需要人来配置“注入”什么。核心价值在于通过 interface 降低代码之间的耦合， ~~让同一个组件具有更多不同的可能 ，同时~~在后续创建新组件时，受益于第一次配置，Spring 有能力自动找到组件需要的依赖。

使用 Spring 的依赖注入理念，最终得到的是一个不同组件之间的依赖关系网，这个依赖关系由开发者配置。当需要一个组件时候，该组件不再由开发者拼装，Spring 通过依赖网自动产生这个组件，也就是所谓的自动装配。

## 处理自动装配歧义
如果有多个 bean 都能满足依赖关系的话， Spring 将会抛出一个异常，表明没有明确指定要选择哪个 bean 进行自动装配。所以 Spring 提供了一些机制来指定一个要注入的 bean。

> 如果有多个 bean 都能满足依赖关系的话，Spring 将会抛出一个异常，表明没有明确指定要选择哪个 bean 进行自动装配。   

常规思维中最基本要做的就是命名加以区分，但仍然没有满足“装配哪个”的问题，而手动配置失去了自动装配的意义。

在实际中 Spring 使用了和我猜测接近的方式，给组件定义优先级`@Primary`同时还额外设计了限定符`@Qualifier("beanname")`来缩小范围，限定符可以多个叠加，但限定符采用文本来定义存在不稳定因素。Spring 支持 Conditional 注解，同样可以作为一个处理歧义的方式。

## Spring 托管的组件如何不创建单例
> 默认情况下，Spring 中的 bean 都是单例的，Spring 会拦截对 beanCreating()的调用并确保返回的是 Spring 所创建的 bean，也就是 Spring 本身在调用 beanCreating()时所创建的 bean。因此，多个地方bean 引用会得到相同的 bean 实例。   

对于易变的组件，数据改动会同步到所有使用了该组件的地方。Spring 提供了多种作用域，通过`@Scope` 来定义 bean 的创建，可以在 ConfigurableBeanFactory 查看支持的作用域。对于 XML 配置可以在 bean 元素的 scope 进行设置。可以通过代理选项 proxyMode 处理原型注入单例的情况，比如购物车与商店服务。

## Spring 环境变量
除了配置数据源，Spring 自身对于 Environment 有进一步支持，可以通过为 Environment 增加数据来实现运行时注入。通过 `@PropertySource` 注解来指定一个 properties 文件引入部分属性。（但直觉上这不是引入数据的正确方式，这项功能更适合定义环境变量）

## SpEL
SpEL 包含在 `#{…}` 中，使用 T() 可以调用一些类型的方法，例如 System，直接使用 bean.propertyName? 可以直接引用 bean 的属性以及方法，使用 systemProperties['key'] 可以引用系统或者环境属性。 `[]` 运算符除了可以饮用数组元素，还可以对字符串中的字母进行引用`#{'Hello'[3]}`，对于一个集合 `#{songs.?[artists eq 'Leehom']}` 可以过滤出指定条件的元素，`#{.^[]} / #{.$[]}` 用来获取第一个或最后一个匹配项目，`#{.![]}` 将集合的元素某个属性放在新的字符串集合中，支持连续使用`#{songs.?[artists eq 'Leehom'].![title]}`。

## 面向切面编程
```
@AspectJ --- 切面
@Pointcut("execution(* *.methodInvoke(..))") --- 切点
@Before("pointcut() && within(package.*)") --- 时间点
public class doSomething(){} --- 通知
@DeclareParents(value="Basic+",defaultImpl = ExtraImpl.class) --- 增加功能
```

在特定时间点，切面获得程序的上下文，并进行一些日志、权限验证、增加信息增加方法等处理。通过切面，原始的程序保持了简单干净。

切面为一个或多个切点的组合，但相似功能的切点不是必须放在同一个切面，当满足切点定义的情形时，会触发通知。

如果想实现面向切面编程，一种可能的方式为在编译或程序的其他周期，给源代码（或编译）“加料”。将切点配置的流程包裹起来，并在运行前、运行后、抛出错误时做对应的处理。想要让 Spring 识别到切面，首先需要把切面变成 bean 加入到 Spring 的依赖关系网中，同时启用`@EnableAspectJAutoProxy`。

可以参考的官网的文档[Aspect Oriented Programming with Spring](https://docs.spring.io/spring/docs/4.3.15.RELEASE/spring-framework-reference/html/aop.html)

Spring 支持的切点表达式语言包括 `arg() @args() excution() this() target() @target() within() @within() @annotation @bean()`。其中连接词 && 与 and 可以互换。

常见的通知有如下时间点 `@Before @After @AfterThrowing @AfterReturing` ，对于 `@Around` 环绕通知，通知方法需要使用 ProceedingJoinPoint 参数（这里不确定能否与 arg() 语法结合)，通过 try … catch 语法结合 jp.proceed() 来定义不同时间点的操作。

典型的切点描述：
```
任何位置、任意返回类型、使用任意参数的方法被调用时通知
execution(* com.location.of.Class.method(..))
限定特定包中才触发通知
execution(* com.location.of.Class.method(..)) && within(com.spetial.*)
除指定 bean 以外触发通知
execution(* com.location.of.Class.method(..)) and !bean('beanName')
通过 Pointcut 定义常用切点
@Pointcut("execution(** com.location.of.Class.method(String)) && args(param)")
public void method(String param){}
```

## 读取 Properties 中定义的数据
有两种方式可以进行调用:
```java
@Configuration
@PropertySource("classpath:application.properties")
public class AppConfig {
    @Bean
    public PropertyValue getVik(@Value("${vik}") String value){ 
        return new PropertyValue(value); 
    }
}

@Configuration
@PropertySource("classpath:application.properties")
public class AppConfig {
    @Autowired
    private Environment env;     

    @Bean
    public PropertyValue getVik(){ 
        return new PropertyValue(env.getProperty("vik")); 
    }
}
```
