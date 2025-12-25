import streamlit as st
import random
import time

# ページ設定
st.set_page_config(
    page_title="神経衰弱ゲーム",
    page_icon="🎴",
    layout="centered"
)

# かわいい絵文字のリスト
EMOJIS = ["🐶", "🐱", "🐰", "🦄", "🌸", "🍓", "🍎", "🌈", "⭐", "💖"]

# セッション状態の初期化
if 'cards' not in st.session_state:
    # カードを2枚ずつ用意
    cards = EMOJIS[:6] * 2  # 6種類×2枚=12枚
    random.shuffle(cards)
    st.session_state.cards = cards
    st.session_state.revealed = [False] * 12
    st.session_state.matched = [False] * 12
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.moves = 0
    st.session_state.pairs_found = 0
    st.session_state.checking = False

# タイトル
st.title("🎴 かわいい神経衰弱ゲーム")
st.write("同じ絵柄のカードを2枚見つけてね！")

# スコア表示
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💖 見つけたペア", f"{st.session_state.pairs_found}/6")
with col2:
    st.metric("👆 めくった回数", st.session_state.moves)
with col3:
    if st.button("🔄 もう一回遊ぶ"):
        # リセット
        cards = EMOJIS[:6] * 2
        random.shuffle(cards)
        st.session_state.cards = cards
        st.session_state.revealed = [False] * 12
        st.session_state.matched = [False] * 12
        st.session_state.first_card = None
        st.session_state.second_card = None
        st.session_state.moves = 0
        st.session_state.pairs_found = 0
        st.session_state.checking = False
        st.rerun()

st.markdown("---")

# カードをクリックした時の処理
def card_clicked(index):
    # すでにめくられている、または揃ったカードはクリックできない
    if st.session_state.revealed[index] or st.session_state.matched[index]:
        return
    
    # 2枚選択中はクリックできない
    if st.session_state.checking:
        return
    
    # カードをめくる
    st.session_state.revealed[index] = True
    
    if st.session_state.first_card is None:
        # 1枚目を選択
        st.session_state.first_card = index
    elif st.session_state.second_card is None:
        # 2枚目を選択
        st.session_state.second_card = index
        st.session_state.moves += 1
        st.session_state.checking = True

# カードの表示（4列×3行）
cols_per_row = 4
for row in range(3):
    cols = st.columns(cols_per_row)
    for col_idx in range(cols_per_row):
        card_idx = row * cols_per_row + col_idx
        
        with cols[col_idx]:
            # カードの状態を判定
            if st.session_state.matched[card_idx]:
                # 揃ったカード（常に表示）
                st.button(
                    st.session_state.cards[card_idx],
                    key=f"card_{card_idx}",
                    disabled=True,
                    use_container_width=True
                )
            elif st.session_state.revealed[card_idx]:
                # めくられたカード
                st.button(
                    st.session_state.cards[card_idx],
                    key=f"card_{card_idx}",
                    disabled=True,
                    use_container_width=True
                )
            else:
                # 裏向きのカード
                if st.button(
                    "❓",
                    key=f"card_{card_idx}",
                    use_container_width=True,
                    on_click=card_clicked,
                    args=(card_idx,)
                ):
                    pass

# 2枚選択した後の判定
if st.session_state.first_card is not None and st.session_state.second_card is not None:
    first = st.session_state.first_card
    second = st.session_state.second_card
    
    # 絵柄が同じか判定
    if st.session_state.cards[first] == st.session_state.cards[second]:
        # 正解！
        st.session_state.matched[first] = True
        st.session_state.matched[second] = True
        st.session_state.pairs_found += 1
        st.success(f"✨ やったね！ {st.session_state.cards[first]} のペアを見つけたよ！")
        
        # リセット
        st.session_state.first_card = None
        st.session_state.second_card = None
        st.session_state.checking = False
        
        # 全部揃ったか確認
        if st.session_state.pairs_found == 6:
            st.balloons()
            st.success(f"🎉 すごい！全部見つけたね！{st.session_state.moves}回でクリアだよ！")
    else:
        # 不正解
        st.warning("💭 ちがったね！もう一回チャレンジ！")
        time.sleep(1.5)
        
        # カードを裏返す
        st.session_state.revealed[first] = False
        st.session_state.revealed[second] = False
        st.session_state.first_card = None
        st.session_state.second_card = None
        st.session_state.checking = False
        st.rerun()

# フッター
st.markdown("---")
st.caption("💡 同じ絵柄のカードを2枚見つけてね！全部で6ペアあるよ")
st.caption("Created with ❤️ for パパの娘ちゃん")
