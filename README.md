# ATRI Extract Toolbox
此仓库是对视觉小说游戏《ATRI -My Dear Moments-》资源包结构和解包所需工具的总结与索引，并附带几个用于处理解包资源的脚本。
## 免责声明
* 游戏内容受到版权法律和国际公约的保护，任何未经授权的复制和公开传播均构成对原作者、开发商、发行商等的权利侵害。
* 解包内容仅用于个人欣赏与学习，严禁将解包内容用于任何商业和盈利活动。
* 本仓库为开源项目的总结与索引，仅供相关技术的学习与交流，不提供游戏本体及任何解包资源文件。
* 本README已尽到劝导义务，任何由于不当使用解包内容带来的纠纷均由使用者自行承担。

## 游戏解包
PC版游戏本体购买：[Steam](https://store.steampowered.com/app/1230140/ATRI_My_Dear_Moments/) | [DMM](https://dlsoft.dmm.com/detail/aniplex_0003/) | [DLsite](https://www.dlsite.com/soft/work/=/product_id/VJ014002.html)

游戏解包工具（于Steam版测试可用）：[morkt/GARbro](https://github.com/morkt/GARbro)
## 资源包结构与处理工具索引
<table>
    <tr>
        <td width="10%">资源包</td>
        <td width="10%">文件名</td>
        <td width="45%">解释</td>
        <td width="35%">处理工具</td>
    </tr>
    <tr>
        <td rowspan="6">vol1.xp3</td>
        <td>*.opus</td>
        <td>角色语音</td>
        <td>批量转换为其他格式：batch_convert.py</td>
    </tr>
    <tr>
        <td>b*.ks.scn</td>
        <td>剧本</td>
        <td>
            SCN反编译为JSON：<a href="https://github.com/UlyssesWu/FreeMote">UlyssesWu/FreeMote</a>
            <br>
            JSON解析为可读格式：parse_script.py
        </td>
    </tr>
    <tr>
        <td>ev*.png</td>
        <td>剧情CG</td>
        <td></td>
    </tr>
    <tr>
        <td>sd*.png</td>
        <td>Q版小剧场CG</td>
        <td></td>
    </tr>
    <tr>
        <td>OP_*.wmv</td>
        <td>各语言OP视频</td>
        <td></td>
    </tr>
    <tr>
        <td>ed.wmv</td>
        <td>ED视频</td>
        <td></td>
    </tr>
    <tr>
        <td rowspan="4">data.xp3</td>
        <td>bgm/*.ogg</td>
        <td>游戏音乐</td>
        <td>batch_convert.py</td>
    </tr>
    <tr>
        <td>image/*</td>
        <td>系统图像素材</td>
        <td></td>
    </tr>
    <tr>
        <td>sound/*.ogg</td>
        <td>游戏音效</td>
        <td>batch_convert.py</td>
    </tr>
    <tr>
        <td>video/*</td>
        <td>剧情过场动画</td>
        <td></td>
    </tr>
    <tr>
        <td rowspan="1">voice.xp3</td>
        <td>system/*.opus</td>
        <td>角色系统语音（主界面、菜单等语音）</td>
        <td>batch_convert.py</td>
    </tr>
    <tr>
        <td rowspan="1">fgimage.xp3</td>
        <td>*</td>
        <td>角色立绘零件，整体解包（解包时选择导出为PNG）后使用用atri-composite组装</td>
        <td>组装立绘零件：<a href="https://github.com/lictex/atri-composite">lictex/atri-composite</a></td>
    </tr>
    <tr>
        <td rowspan="1">bgimage.xp3</td>
        <td>*</td>
        <td>背景图片、场景效果图像素材</td>
        <td></td>
    </tr>
</table>

## 本仓库附带工具使用方法
### batch_convert.py
此脚本用于多线程批量转换解包音频文件，**需要正确部署 ffmpeg 并将其加入环境变量**。
```shell
python batch_convert.py -f mp3 -t 16
```
可指定的参数:
- `-i` | `--input`: 输入音频文件目录。默认值：当前工作目录
- `-o` | `--output`: 输入音频文件目录。默认值：当前工作目录下的converted目录
- `-f` | `--format`: 转换的格式（文件后缀，不带"."，如mp3、wav）。默认值：mp3
- `-t` | `--thread`: 线程数。默认值：16

### parse_script.py
此脚本用于将 <a href="https://github.com/UlyssesWu/FreeMote">FreeMote</a> 反编译得到的 json 剧本文件解析为可读的表格格式，可直接作为 [Novel2Anki](https://github.com/2DIPW/novel2anki) 的输入数据。

> FreeMote 反编译 scn 的方法：将 scn 文件拖拽至 PsbDecompile.exe 上。

格式为一句一行，**第1列为角色，第2列为日文原文，第3列为译文，第4列为对应的语音文件名**，默认列与列之间以制表符分隔。
```shell
python parse_script.py 
```
可指定的参数:
- `-i` | `--input`: 输入音频文件目录。默认值：当前工作目录
- `-o` | `--output`: 输入音频文件目录。默认值：当前工作目录下的parsed目录
- `-l` | `--language`: 译文的语言，0: JP; 1:EN; 2:ZHS; 3:ZHT, 默认值：2
- `-d` | `--delimiter`: 列分隔符。默认值：\\t
- `-af` | `--audio_format`: 语音文件名添加的后缀，如后期需要将此数据用于需要句子和语音文件对应的场景，请指定为转换后的格式。默认值：mp3
- `-s` | `--single_file`: 是否将所有内容合并为一个文件，合并后的文件将输出为all_in_one_parsed.txt

## 开源声明
本仓库文本内容基于 CC BY-NC-SA 4.0 协议共享

本仓库代码内容基于 GNU General Public License v3.0 开源