import streamlit as st
import pandas as pd
from datetime import datetime
import os
import folium
from streamlit_folium import st_folium


# ====================
# 設定
# ====================

st.set_page_config(
    page_title="市民協働インフラ管理アプリ",
    layout="wide"
)


# ====================
# フォルダ作成
# ====================

os.makedirs(
    "uploads",
    exist_ok=True
)


# ====================
# CSV初期化
# ====================

if not os.path.exists("posts.csv"):

    pd.DataFrame(
        columns=[
            "日時",
            "タグ",
            "コメント",
            "写真",
            "緯度",
            "経度"
        ]
    ).to_csv(
        "posts.csv",
        index=False
    )



# ====================
# メニュー
# ====================

menu = st.sidebar.radio(
    "メニュー",
    [
        "ホーム",
        "新規投稿"
    ]
)



# ====================
# ホーム
# ====================

if menu == "ホーム":


    st.title(
        "🏗 市民協働インフラ管理"
    )


    st.write(
        "道路・設備の異常を共有するアプリ"
    )


    try:

        posts = pd.read_csv(
            "posts.csv"
        )

    except:

        posts = pd.DataFrame()



    # ====================
    # 地図表示
    # ====================

    st.header(
        "🗺 投稿マップ"
    )


    if not posts.empty:


        map_data = posts[
            [
                "緯度",
                "経度"
            ]
        ].dropna()



        if not map_data.empty:


            m = folium.Map(

                location=[
                    map_data["緯度"].mean(),
                    map_data["経度"].mean()
                ],

                zoom_start=15
            )



            for _, row in posts.iterrows():


                folium.Marker(

                    [
                        row["緯度"],
                        row["経度"]
                    ],

                    popup=f"""
                    タグ：{row['タグ']}<br>
                    コメント：{row['コメント']}
                    """

                ).add_to(m)



            st_folium(

                m,

                width=1000,

                height=500

            )


        else:

            st.info(
                "位置情報付き投稿がありません"
            )


    else:

        st.info(
            "まだ投稿がありません"
        )



    st.divider()



    # ====================
    # タグ一覧
    # ====================

    st.header(
        "📂 タグ一覧"
    )


    if not posts.empty:


        tag_counts = posts[
            "タグ"
        ].value_counts()



        for tag, count in tag_counts.items():

            st.write(
                f"#{tag}（{count}件）"
            )


    else:

        st.info(
            "投稿なし"
        )



    st.divider()



    # ====================
    # 最近の投稿
    # ====================

    st.header(
        "🖼 最近の投稿"
    )


    if not posts.empty:


        recent_posts = posts.iloc[::-1].head(6)


        cols = st.columns(3)



        for i, (_, row) in enumerate(
            recent_posts.iterrows()
        ):


            with cols[i % 3]:


                st.subheader(
                    f"#{row['タグ']}"
                )



                if row["写真"] != "":


                    image_path = os.path.join(

                        "uploads",

                        row["写真"]

                    )



                    if os.path.exists(
                        image_path
                    ):


                        st.image(

                            image_path,

                            use_container_width=True

                        )



                st.caption(
                    row["コメント"]
                )



                st.caption(
                    row["日時"]
                )



# ====================
# 新規投稿
# ====================

if menu == "新規投稿":


    st.title(
        "📷 新規投稿"
    )



    uploaded_file = st.file_uploader(

        "写真",

        type=[
            "jpg",
            "jpeg",
            "png"
        ]

    )



    tag = st.selectbox(

        "部位",

        [

            "道路",

            "ガードレール",

            "縁石",

            "街灯",

            "建物",

            "その他"

        ]

    )



    comment = st.text_area(

        "現象・コメント"

    )



    st.subheader(
        "📍位置情報"
    )



    latitude = st.number_input(

        "緯度",

        value=35.681236

    )


    longitude = st.number_input(

        "経度",

        value=139.767125

    )



    if st.button(
        "投稿する"
    ):



        photo_name = ""



        if uploaded_file:



            photo_name = (

                datetime.now()
                .strftime(
                    "%Y%m%d%H%M%S"
                )

                +

                "_"

                +

                uploaded_file.name

            )



            with open(

                os.path.join(

                    "uploads",

                    photo_name

                ),

                "wb"

            ) as f:


                f.write(

                    uploaded_file.getbuffer()

                )



        new_post = pd.DataFrame([

            {

                "日時":

                datetime.now(),


                "タグ":

                tag,


                "コメント":

                comment,


                "写真":

                photo_name,


                "緯度":

                latitude,


                "経度":

                longitude

            }

        ])




        old_posts = pd.read_csv(

            "posts.csv"

        )



        all_posts = pd.concat(

            [

                old_posts,

                new_post

            ],

            ignore_index=True

        )



        all_posts.to_csv(

            "posts.csv",

            index=False

        )



        st.success(

            "投稿しました"

        )


        st.rerun()



    st.divider()



    # ====================
    # 投稿一覧
    # ====================


    st.header(
        "📋 投稿一覧"
    )


    posts = pd.read_csv(
        "posts.csv"
    )



    if not posts.empty:



        for index,row in posts.iloc[::-1].iterrows():



            st.subheader(

                f"#{row['タグ']}"

            )


            st.write(

                row["コメント"]

            )


            st.caption(

                row["日時"]

            )



            if row["写真"]:



                image_path = os.path.join(

                    "uploads",

                    row["写真"]

                )


                if os.path.exists(

                    image_path

                ):


                    st.image(

                        image_path,

                        width=300

                    )



            if st.button(

                "🗑 削除",

                key=f"delete{index}"

            ):


                posts = posts.drop(

                    index

                )


                posts.to_csv(

                    "posts.csv",

                    index=False

                )


                st.rerun()



            st.divider()



    else:

        st.info(
            "投稿なし"
        )
