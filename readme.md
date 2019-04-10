## 说明文档
    
        
### 环境
```
python环境 == python3.6.3    
系统环境 == win10_64
```
### 安装包
```
requirements.txt文件里面
```
### 原理
```
主要运用Python+Selenium+ChromeDriver进行爬虫
由于反爬虫太厉害，而且难度较大，所以用这种方法进行爬虫
注意事项：
  爬虫时候时间尽量再1分钟左右，否则cnki发生点击频繁而拒绝点击
  如果 > 20s CNKI系统会死
  如果还不行，记得driver.delete_cookies()每爬一个，清一次cookie
```
### 启动文件
启动文件， main.py

### 环境安装
```
安装 Python -下载并配置好环境变量，shell输入：python -V 出现对应版本号即安装成功！
安装pip（Python包管理工具）
安装selenium-pip install selenium 提示：Successfully installed selenium-即安装成功！
安装ChromeDriver-
下载ChromeDriver，注意版本需与浏览器版本对应，附：版本号对应描述（64位浏览器下载32位即可），下载后与chrome安装目录放在一起，然后配置至环境变量即可，配置好后shell输入：chromedriver 无错误即安装成功！
安装python IDE pyCharm
```
