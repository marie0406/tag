import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="まちタグ")

# フォルダ作成
os.makedirs("uploads", exist_ok=True)

# CSV初期化
if not os.path.exists("posts.csv"):
    pd.DataFrame(
        columns=[
            "日時",
            "タグ",
            "コメント",
            "写真"
        ]
    ).to_csv("posts.csv", index=False)

st.title("📸 まちタグ")
st.write("タグを選んで写真を共有")

# 投稿フォーム

uploaded_file = st.file_uploader(
    "写真を選択",
    type=["jpg", "jpeg", "png"]
)

tag = st.selectbox(
    "タグ",
    [
        "道路点検",
        "街灯故障",
        "不法投棄",
        "防災",
        "公園",
        "イベント",
        "その他"
    ]
)

comment = st.text_area("コメント")

if st.button("投稿する"):

    photo_name = ""

    if uploaded_file is not None:

        photo_name = (
            datetime.now().strftime("%Y%m%d%H%M%S")
            + "_"
            + uploaded_file.name
        )

        with open(
            os.path.join("uploads", photo_name),
            "wb"
        ) as f:
            f.write(uploaded_file.getbuffer())

    new_post = pd.DataFrame([
        {
            "日時": datetime.now(),
            "タグ": tag,
            "コメント": comment,
            "写真": photo_name
        }
    ])

    try:
        old_posts = pd.read_csv("posts.csv")
    except:
        old_posts = pd.DataFrame(
            columns=[
                "日時",
                "タグ",
                "コメント",
                "写真"
            ]
        )

    all_posts = pd.concat(
        [old_posts, new_post],
        ignore_index=True
    )

    all_posts.to_csv(
        "posts.csv",
        index=False
    )

    st.success("投稿しました")
    st.rerun()

# 投稿一覧

st.divider()
st.header("📋投稿一覧")

# ⭐追加：タグフィルター
all_tags = ["すべて"] + [
    "道路点検",
    "街灯故障",
    "不法投棄",
    "防災",
    "公園",
    "イベント",
    "その他"
]

selected_tag = st.selectbox("表示するタグを選択", all_tags)

try:
    posts = pd.read_csv("posts.csv")
except:
    posts = pd.DataFrame()

# ⭐追加：タグで絞り込み
if not posts.empty:
    if selected_tag != "すべて":
        posts = posts[posts["タグ"] == selected_tag]

if not posts.empty:

    for index, row in posts.iloc[::-1].iterrows():

        st.subheader(f"#{row['タグ']}")

        if pd.notna(row["コメント"]):
            st.write(row["コメント"])

        st.caption(row["日時"])

        if (
            pd.notna(row["写真"])
            and row["写真"] != ""
        ):

            image_path = os.path.join(
                "uploads",
                row["写真"]
            )

            if os.path.exists(image_path):
                st.image(
                    image_path,
                    width=300
                )

        if st.button(
            "削除",
            key=f"delete_{index}"
        ):

            # 写真削除
            if (
                pd.notna(row["写真"])
                and row["写真"] != ""
            ):

                image_path = os.path.join(
                    "uploads",
                    row["写真"]
                )

                if os.path.exists(image_path):
                    os.remove(image_path)

            posts = posts.drop(index)

            posts.to_csv(
                "posts.csv",
                index=False
            )

            st.rerun()

        st.divider()

else:
    st.info("投稿はまだありません")
