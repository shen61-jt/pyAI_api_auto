**首先安装本项目所需的依赖库，cmd命令为：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r E:\py69_api_auto\requirements.txt
其中：E:\py69_api_auto路径替换自己项目的磁盘路径。**

# **接口自动化测试框架规则说明**

python的版本需要3.10+



**1、接口关联。**

提取：

    如:jsonpath提取方式：
        expires_in: $.expires_in

取值：

    如测试用例获取access_token值：
    ${access_token}

断言支持状态码、响应结果，关键字：status_code、text、$

**2、框架使用说明。**

各目录含义：

    AI_result：保存响应结果。
    common：工具类。
    data：接口数据。
    config：配置文件。
    logs：日志文件。
    reports：allure报告、html报告。
    testcases：测试用例。
    environment.xml：allure报告环境设置。
    categories.json：allure报告categories设置。
    pytest.ini：pytest运行集。
    conftest.py：pytest的配置文件。
    requiremens.txt:框架所需的第三方库。
    run.py：框架运行入口。




**3、持续集成文件。**

allure报告Categories：分类（测试用例结果的分类），默认情况下，有两类缺陷：

    Product defects：产品缺陷（测试结果：failed）。
    Test defects：测试缺陷（测试结果：error/broken）。

categories.json的参数解释：

    name：分类名称。
    
    matchedStatuses：测试用例的运行状态，默认[“failed”, “broken”, “passed”, “skipped”, “unknown”]。
    
    messageRegex：测试用例运行的错误信息，默认是 .* ，是通过正则去匹配的。
    
    traceRegex：测试用例运行的错误堆栈信息，默认是 .* ，是通过正则去匹配的。
