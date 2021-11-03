import datetime
import json
import random

import pandas as pd
import requests
import streamlit as st

page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])

API_URL = 'http://api:8000'

# if page == 'users':
#     st.title('APIテスト画面（ユーザー）')

#     with st.form(key='user'):
#         user_id: int = random.randint(0, 10)
#         username: str = st.text_input('ユーザー名', max_chars=12)
#         data = {
#             'user_id': user_id,
#             'username': username
#         }
#         submit_button = st.form_submit_button(label='送信')

#     if submit_button:
#         st.write('## 送信データ')
#         st.json(data)
#         st.write('## レスポンス結果')
#         url = 'http://127.0.0.1:8000/users/'
#         res = requests.post(url, data=json.dumps(data))
#         st.write(res.status_code)
#         st.json(res.json())

# elif page == 'rooms':
#     st.title('APIテスト画面（会議室）')

#     with st.form(key='room'):
#         room_id: int = random.randint(0, 10)
#         room_name: str = st.text_input('会議室名', max_chars=12)
#         capacity: int = st.number_input('定員', step=1)
#         data = {
#             'room_id': room_id,
#             'room_name': room_name,
#             'capacity': capacity
#         }
#         submit_button = st.form_submit_button(label='送信')

#     if submit_button:
#         st.write('## 送信データ')
#         st.json(data)
#         st.write('## レスポンス結果')
#         url = 'http://127.0.0.1:8000/rooms/'
#         res = requests.post(url, data=json.dumps(data))
#         st.write(res.status_code)
#         st.json(res.json())


# elif page == 'bookings':
#     st.title('APIテスト画面（会議室予約）')

#     with st.form(key='booking'):
#         booking_id: int = random.randint(0, 10)
#         user_id: int = random.randint(0, 10)
#         room_id: int = random.randint(0, 10)
#         booked_num: int = st.number_input('予約人数', step=1)
#         date = st.date_input('日付を入力', min_value=datetime.date.today())
#         start_time = st.time_input('開始時刻：', value=datetime.time(hour=9, minute=0))
#         end_time = st.time_input('終了時刻：', value=datetime.time(hour=20, minute=0))
#         data = {
#             'booking_id': booking_id,
#             'user_id': user_id,
#             'room_id': room_id,
#             'booked_num': booked_num,
#             'start_datetime': datetime.datetime(
#                 year=date.year,month=date.month, day=date.day, hour=start_time.hour, minute=start_time.minute
#             ).isoformat(),
#             'end_datetime': datetime.datetime(
#                 year=date.year,month=date.month, day=date.day, hour=end_time.hour, minute=end_time.minute
#             ).isoformat()
#         }
#         submit_button = st.form_submit_button(label='送信')

#     if submit_button:
#         st.write('## 送信データ')
#         st.json(data)
#         st.write('## レスポンス結果')
#         url = 'http://127.0.0.1:8000/bookings/'
#         res = requests.post(url, data=json.dumps(data))
#         st.write(res.status_code)
#         st.json(res.json())

if page == "users":
    st.title("ユーザー登録画面")

    with st.form(key="user"):
        user_id: int = random.randint(0, 10)
        username: str = st.text_input("ユーザー名", max_chars=12)
        data = {
            # 'user_id': user_id,
            "username": username
        }
        submit_button = st.form_submit_button(label="ユーザー登録")

    if submit_button:
        st.write("## 送信データ")
        st.json(data)
        st.write("## レスポンス結果")
        # url = "http://127.0.0.1:8000/users/"
        url = f"{API_URL}/users"
        res = requests.post(url, data=json.dumps(data))
        st.write(res.status_code)
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        st.json(res.json())

elif page == "rooms":
    st.title("会議室登録画面")

    with st.form(key="room"):
        room_id: int = random.randint(0, 10)
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", step=1)
        data = {
            # 'room_id': room_id,
            "room_name": room_name,
            "capacity": capacity,
        }
        submit_button = st.form_submit_button(label="会議室登録")

    if submit_button:
        st.write("## 送信データ")
        st.json(data)
        st.write("## レスポンス結果")
        url = f"{API_URL}/rooms"
        res = requests.post(url, data=json.dumps(data))
        st.write(res.status_code)
        if res.status_code == 200:
            st.success("会議室登録完了")
        st.json(res.json())


elif page == "bookings":
    st.title("会議室予約画面")
    # ユーザー一覧
    url_users = f"{API_URL}/users"
    res = requests.get(url_users)
    users = res.json()
    # st.json(users)
    users_dict = {}
    for user in users:
        users_dict[user["username"]] = user["user_id"]
    # st.write(users_dict)

    # 会議室一覧
    url_rooms = f"{API_URL}/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()
    # st.json(rooms)
    rooms_dict = {}
    for room in rooms:
        rooms_dict[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"],
        }
    # st.write(rooms_dict)

    st.write("### 会議室一覧")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ["会議室名", "定員", "会議室ID"]
    st.table(df_rooms)

    url_bookings = f"{API_URL}/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()

    st.write("### 予約一覧")
    df_bookings = pd.DataFrame(bookings)

    users_id = {}
    for user in users:
        users_id[user["user_id"]] = user["username"]

    rooms_id = {}
    for room in rooms:
        rooms_id[room["room_id"]] = {
            "room_name": room["room_name"],
            "capacity": room["capacity"],
        }

    # IDを各値に変更する無名関数
    to_username = lambda x: users_id[x]
    to_room_name = lambda x: rooms_id[x]["room_name"]
    to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime(
        "%Y/%m/%d %H:%M"
    )

    # 特定の列に無名関数適用
    df_bookings["user_id"] = df_bookings["user_id"].map(to_username)
    df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)

    df_bookings = df_bookings.rename(
        columns={
            "user_id": "予約者名",
            "room_id": "会議室名",
            "booked_num": "予約人数",
            "start_datetime": "開始時刻",
            "end_datetime": "終了時刻",
            "bookings_id": "予約番号",
        }
    )

    st.table(df_bookings)

    with st.form(key="booking"):
        username: str = st.selectbox("予約者名", users_dict.keys())
        room_name: str = st.selectbox("会議室名", rooms_dict.keys())
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("日付: ", min_value=datetime.date.today())
        start_time = st.time_input("開始時刻: ", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input("終了時刻: ", value=datetime.time(hour=20, minute=0))
        submit_button = st.form_submit_button(label="予約登録")

    if submit_button:
        user_id: int = users_dict[username]
        room_id: int = rooms_dict[room_name]["room_id"]
        capacity: int = rooms_dict[room_name]["capacity"]

        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute,
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute,
            ).isoformat(),
        }
        # 予約人数が定員超過の場合
        if booked_num > capacity:
            st.error(f"{room_name}の定員は{capacity}です。{capacity}名以下の予約人数を入力ください")
        # 開始時刻 >= 終了時刻
        elif start_time >= end_time:
            st.error("開始時刻が終了時刻を越えています")

        elif start_time < datetime.time(
            hour=9, minute=0, second=0
        ) or end_time > datetime.time(hour=20, minute=0, second=0):
            st.error("利用時間は9時から20時になります")

        else:
            st.write("## 送信データ")
            st.json(data)
            st.write("## レスポンス結果")
            url = f"{API_URL}/bookings"
            res = requests.post(url, data=json.dumps(data))
            st.write(res.status_code)
            if res.status_code == 200:
                st.write("予約完了しました")
            if res.status_code == 404 and res.json()['detail'] == 'Already booked':
                st.write('指定の時間には既に予約が入っています')
            st.json(res.json())
