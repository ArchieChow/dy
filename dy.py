import streamlit as st
import pandas as pd
import time
import random
from DrissionPage import ChromiumPage

# 初始化 ChromiumPage（推荐提前启动 ChromeDriver，或使用已安装的 Chrome 浏览器）
page = ChromiumPage()

# Streamlit 页面标题
st.title("抖音评论抓取工具")
st.write("请输入抖音视频的 ID，每行一个（例如：7276166950474575134）")

# 用户输入抖音视频 ID
url_input = st.text_area("粘贴视频ID列表：", height=200)

# 抓取评论的函数
def get_comments(video_id):
    try:
        url = f'https://www.douyin.com/video/{video_id}'
        page.get(url)
        time.sleep(random.uniform(1, 2.5))  # 控制访问频率

        # 尝试获取评论内容
        elements = page.eles('xpath://*[@id="douyin-right-container"]/div[2]/div/div/div/div[5]/div/div/div[3]/div/div/div[2]/div/div[2]/span/span/span/span/span/span/span')
        comments = [ele.text for ele in elements][:3]

        # 保证长度为3
        while len(comments) < 3:
            comments.append('')

        return comments
    except Exception as e:
        return [f'获取失败: {e}', '', '']

# 提交按钮逻辑
if st.button("开始抓取评论"):
    if not url_input.strip():
        st.warning("请输入至少一个视频ID。")
    else:
        video_ids = [line.strip() for line in url_input.strip().splitlines() if line.strip()]
        data_rows = []

        # 设置进度条
        progress = st.progress(0)
        status_text = st.empty()

        for i, video_id in enumerate(video_ids):
            comments = get_comments(video_id)
            data_rows.append({
                '视频ID': video_id,
                '评论1': comments[0],
                '评论2': comments[1],
                '评论3': comments[2],
            })
            progress.progress((i + 1) / len(video_ids))
            status_text.text(f"已完成 {i + 1}/{len(video_ids)}")

        # 展示抓取结果
        df = pd.DataFrame(data_rows)
        st.success("评论抓取完成！")
        st.dataframe(df)

        # 下载按钮
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("下载 CSV 文件", data=csv, file_name="douyin_comments.csv", mime='text/csv')

        # 关闭浏览器窗口
        page.close()