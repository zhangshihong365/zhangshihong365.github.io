# Shihong Zhang 个人学术主页

这是根据用户提供的个人资料制作的英文个人主页。布局参考 [Zhe Wang 的主页](https://walterzwang.github.io/)：白色背景、顶部导航、左侧个人资料和右侧正文。参考网站中的个人信息、照片、新闻和外部账号均未移植。

网站已生成完整 HTML，可以直接打开 `index.html`，也可以把文件上传至 GitHub Pages。浏览网页不需要 Node.js、Python、数据库或在线第三方组件。Python 仅用于修改内容后重新生成 HTML。

导航使用 **Research**，最右侧新增 **Moments**。所有页面共享同一套导航与侧栏。

CV 入口保留，页面仅展示 Education 和 Experience；MIT 访学列于 Experience。网站不提供原始简历文件或下载功能，发布目录和代码包也不包含原始简历。

## 页面说明

| 文件 | 页面内容 |
| --- | --- |
| `index.html` | 个人介绍、研究兴趣、近期动态（包含简历中的全部荣誉奖项与资助）、研究平台预览 |
| `research.html` | Research：研究方向、15 篇已发表论文（标题链接到 DOI）、4 个研究项目、2 项专利 |
| `team.html` | 学生指导经历，未添加 CV 中没有提供的学生姓名 |
| `teaching.html` | HKUST 与 MIT 的课程、助教和授课经历 |
| `softwares.html` | CV 中的三个研究平台及原始截图；前两个含原 CV 提供的网址 |
| `talks.html` | 10 项会议报告与研讨会经历 |
| `service.html` | 实习经历（含期刊编辑团队工作）、会议服务、期刊审稿和学术组织会员 |
| `cv.html` | 仅 Education 与 Experience；MIT 访学列于 Experience，无简历下载 |
| `moments.html` | 生活动态，包含 Kennedy Town 三张横排照片及摄影作品集入口 |

## 代码结构

```text
.
├── index.html                 # 可直接访问的首页
├── research.html              # 研究与论文
├── team.html                  # 学生指导
├── teaching.html              # 教学
├── softwares.html             # 研究平台
├── talks.html                 # 报告
├── service.html               # 学术服务
├── cv.html                    # 教育与经历（不提供简历下载）
├── moments.html               # 生活动态
├── assets/
│   ├── css/style.css          # 布局、字体、配色、手机适配和打印样式
│   ├── js/main.js             # 手机菜单
│   └── images/
│       ├── favicon.svg        # SZ 浏览器图标
│       ├── profile photo.jpeg # 个人头像
│       ├── urban-energy.png   # CV 中的城市建筑能耗平台截图
│       ├── vehicle-to-building.png
│       └── building-retrofit.png
├── content/site.json          # 公开页面所需内容，日常维护入口
├── templates/base.html        # 所有页面共用的网页外壳
├── scripts/build.py           # 将内容与模板生成静态 HTML，无第三方依赖
├── .nojekyll                  # 告诉 GitHub Pages 直接提供静态文件
├── .gitignore                 # 排除临时文件和本地检查材料
└── README.md                  # 本说明
```

内容、外观和交互分别维护：

- **改信息**：修改 `content/site.json`，运行生成命令。
- **改颜色、宽度、字体、手机布局**：修改 `assets/css/style.css`，无需重新生成 HTML。
- **改顶部或侧边栏结构**：修改 `templates/base.html` 或 `scripts/build.py`，运行生成命令。
- **改菜单交互**：修改 `assets/js/main.js`，无需重新生成 HTML。

页面中的文字已经写入 HTML，搜索引擎可以读取；关闭 JavaScript 后仍可阅读全部内容。只使用相对路径，同时适用于 `用户名.github.io` 和 `用户名.github.io/仓库名/`。

## 本地打开与更新

直接双击 `index.html`，用浏览器打开。其余页面可以通过导航访问。建议修改内容数据，而非直接编辑已生成的 HTML，否则下次生成时会覆盖手动修改。

修改 `content/site.json` 后，在项目文件夹运行：

```bash
python3 scripts/build.py
```

如需本地网页服务器，可运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

然后在浏览器打开 `http://127.0.0.1:8000`。结束预览时按 `Ctrl+C`。这些命令只在本地运行，GitHub Pages 不需要安装 Python。

## 常见修改

### 更换头像

当前使用用户提供的 `assets/images/profile photo.jpeg` 作为头像，所有页面共享。路径中的空格在 `profile.portrait` 中写作 `%20`。

1. 将新头像放到 `assets/images/profile.jpg`（或直接替换当前头像文件）。
2. 修改 `content/site.json` → `profile.portrait` 为 `assets/images/profile.jpg`。
3. 运行 `python3 scripts/build.py`。

头像自动裁剪为圆形。正方形、人物居中的照片效果更好。

### 修改导航拼写

当前显示 `Research`。如需更改导航名称，可修改 `content/site.json` 中 `site.research_label`，再运行生成命令。地址仍为 `research.html`。

### 更新个人资料或联系方式

修改 `profile` 中的姓名、职务、学校、邮箱、Google Scholar、LinkedIn 等字段。Google Scholar 使用 CV 中有可见文字“Google scholar”的链接；原文件中另外一个仅关联不可见字符的历史链接未采用。

### 更新 CV 页

修改 `content/site.json` 中的 `education` 和 `experience` 数组，然后运行 `python3 scripts/build.py`。Education 包含 HKUST 博士、武汉大学硕士和武汉理工大学本科；Experience 包含 HKUST 博士后和 MIT 访学。CV 页面仅展示这两个栏目，不读取或链接原始简历文件。

### 新增论文

在 `publications` 数组中添加一条：

```json
{
  "title": "论文标题",
  "authors": "作者列表 (2027).",
  "venue": "期刊名称、卷号、页码。",
  "year": 2027,
  "status": "published",
  "url": ""
}
```

`status` 使用 `published`，仅添加已发表论文。`url` 留空则只展示论文标题；有 DOI 或出版社网址时可以填入。`publications` 数组顺序就是展示顺序。

### 更新研究平台

修改 `platforms` 中的标题、描述、截图路径和网址。第三个平台未提供公开链接，目前显示“Public link coming soon.”；填入正确的 `url` 后，生成器会自动显示访问按钮。前两个链接沿用 CV 中的 HTTP 地址，外部服务器是否可访问取决于原平台。

### 添加 Moments

将照片放在 `assets/images/moments/` 下，再把 `moments` 的空数组 `[]` 替换成例如：

```json
[
  {
    "date": "2026-11-15",
    "title": "在这里填写真实的动态标题",
    "text": "在这里填写照片背后的故事。",
    "image": "assets/images/moments/your-photo.jpg",
    "alt": "描述照片内容，方便无法看到图片的访客理解"
  }
]
```

上述内容仅为编辑示例，没有添加到网站中。填写自己的实际内容并使用真实存在的图片路径。运行生成命令后，空状态会自动替换为图文条目。新条目放在数组前面即可优先展示。纯文字动态可以省略 `image`。

### 修改颜色和更新时间

主色和链接色位于 `assets/css/style.css` 顶部的 `:root` 中。页脚年份和更新时间位于 `content/site.json` 的 `site.year`、`site.updated`；内容更新后可一并修改。

## 上传到 GitHub Pages

目前仅生成了本地代码，尚未创建 GitHub 仓库或发布网站。

1. 在 GitHub 新建公开仓库。个人主站建议命名为 `你的GitHub用户名.github.io`（用户名使用小写）；也可使用其他仓库名作为项目站点。
2. 上传项目内的所有发布文件，让 **`index.html` 位于仓库根目录**，不要多套一层文件夹。至少包含九个 HTML 文件、完整 `assets/` 文件夹及 `.nojekyll`。建议同时上传 `content/`、`templates/`、`scripts/` 和 `README.md`，方便以后维护。
3. 进入仓库 **Settings → Pages**。
4. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
5. 选择 **main** 分支和 **/(root)** 文件夹，点击 **Save**。
6. 等待 GitHub 完成发布，通过 Pages 设置页中的 **Visit site** 打开网站。

个人主站地址形如 `https://用户名.github.io/`；项目站点地址形如 `https://用户名.github.io/仓库名/`。以后修改内容、重新生成 HTML 并上传更新后，GitHub Pages 会再次发布。不要只上传修改后的 JSON，必须一起上传重新生成的 HTML。

无需配置自定义域名或 GitHub Actions 构建流程。`.nojekyll` 为隐藏文件，上传时请保留。

官方说明：[创建 GitHub Pages 站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) · [配置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

## 内容来源与验证范围

- 所有身份、时间、论文、资助、获奖、课程和学术服务信息来自用户提供的 CV；介绍和研究主题据此整理，Publications 仅保留已发表论文，在审稿件已从公开内容文件中移除。
- 平台图片直接取自 CV；没有使用参考网站的个人照片、新闻或账号信息。
- 头像使用用户提供的照片；未提供的生活照片或学生名单没有编造。
- 已检查页面的本地资源与锚点、桌面和手机布局、手机菜单。此次更新已检查 CV 入口、Education 与 Experience 的分类，以及发布包不包含原始简历下载文件。没有验证所有外部学术主页或研究平台的实时服务状态。
- 访客地图目前尚未启用，不发送访客统计请求；配置并在公网部署后，会使用 MapMyVisitors 统计服务。项目没有表单后台或外部字体依赖。


## 访客地图（待确定公网网址后接入）

共享页脚已移除 Get in touch，访客世界地图仅显示在 Moments 页面正文最下方。当前只显示没有访客标记的底图，并注明统计尚未启用；没有模拟访问量，也不会对第三方发起统计请求。

确定 GitHub Pages 网址后：

1. 在 [MapMyVisitors](https://mapmyvisitors.com/add) 为实际公网网址生成地图嵌入代码。
2. 从返回代码的 `map.js?d=...` 中复制 `d` 的值，填入 `content/site.json` → `visitor_map.widget_id`。不要使用服务商演示地图的 ID。
3. 将实际网站根地址填入 `visitor_map.site_url`，例如 `https://yourname.github.io/`；项目站点填写 `https://yourname.github.io/repository/`。
4. 保持 `visitor_map.enabled` 为 `true`，运行 `python3 scripts/build.py` 并重新上传网页文件。

地图仅位于 Moments 页面正文底部，接入后统计访问 Moments 页面的访客。脚本只会在配置的网址下通过 HTTPS 加载；本地文件、localhost 和其他预览地址不会进入正式统计。将 `enabled` 改为 `false` 并重新生成，可以移除地图。

该功能需要第三方统计服务保存和汇总访问记录，GitHub Pages 静态网页本身无法完成跨访客累计。地图显示基于 IP 推断的大致位置；配置启用后，服务商会接收访客连接信息用于统计。尚未获取正式 widget ID，因此真实数据加载需在接入后验证。

默认底图来自 [Natural Earth 的 1:110m 陆地数据](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_land.geojson)，本地 SVG 不包含真实访客信息。

### 摄影作品集

Moments 紧邻 CV 右侧。Kennedy Town 照片在 `assets/images/Moments/Kennedy Town/`，通过 `moments[].images` 配置，三张横排，点击可查看原图。访客地图仍位于 Moments 正文最底部。

第二个入口通往 `photography.html`。已加入 `assets/images/Moments/My Photography Portfolio/` 中的 Sydney 照片，保持原始比例，点击可查看原图。后续在 `content/site.json` 的 `photography` 数组中加入 `src`（图片路径）、`alt`（图片描述）及可选的 `caption`（说明），然后运行生成脚本即可。
