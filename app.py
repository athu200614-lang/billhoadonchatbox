import streamlit as st
from datetime import datetime

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Trà Sữa - Tính Hóa Đơn",
    page_icon="🧋",
    layout="wide"
)

# =========================
# DỮ LIỆU MENU
# =========================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa ô long": 38000,
    "Trà sữa thái xanh": 32000,
    "Trà sữa thái đỏ": 32000,
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000,
    "Đào miếng": 7000,
    "Nha đam": 5000,
}

SIZE_PRICE = {
    "Size M": 0,
    "Size L": 7000,
    "Size XL": 12000,
}

SUGAR_LEVEL = [
    "0% đường",
    "30% đường",
    "50% đường",
    "70% đường",
    "100% đường"
]

ICE_LEVEL = [
    "Không đá",
    "30% đá",
    "50% đá",
    "70% đá",
    "100% đá"
]

# =========================
# KHỞI TẠO SESSION STATE
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "paid" not in st.session_state:
    st.session_state.paid = False

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("🧾 Hệ thống tính hóa đơn")

st.divider()

# Nếu đã thanh toán thì hiển thị hóa đơn
if st.session_state.paid:

    st.success("✅ Thanh toán thành công!")

    st.markdown("## 🧾 HÓA ĐƠN THANH TOÁN")

    st.write(
        f"**Khách hàng:** "
        f"{st.session_state.customer_name}"
    )

    st.write(
        f"**Thời gian:** "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

    st.divider()

    total_bill = 0

    for i, item in enumerate(st.session_state.cart, start=1):

        item_total = item["total"]
        total_bill += item_total

        st.markdown(f"### {i}. {item['name']}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"**Size:** {item['size']}")
            st.write(f"**Số lượng:** {item['quantity']}")

        with col2:
            st.write(f"**Đường:** {item['sugar']}")
            st.write(f"**Đá:** {item['ice']}")

        with col3:
            st.write(
                f"**Đơn giá:** "
                f"{format_money(item['unit_price'])}"
            )

        if item["toppings"]:
            st.write(
                "**Topping:** "
                + ", ".join(item["toppings"])
            )
        else:
            st.write("**Topping:** Không")

        st.write(
            f"**Thành tiền:** "
            f"{format_money(item_total)}"
        )

        st.divider()

    st.markdown(
        f"""
        <div style="
            background-color:#fff3cd;
            padding:20px;
            border-radius:10px;
            text-align:right;
            border:1px solid #ffeeba;
        ">
            <h2>TỔNG THANH TOÁN</h2>
            <h1>{format_money(total_bill)}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "🔄 Tạo hóa đơn mới",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.paid = False
        st.session_state.customer_name = ""
        st.rerun()

    st.stop()


# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.markdown("### 👤 Thông tin khách hàng")

customer_name = st.text_input(
    "Tên khách hàng",
    value=st.session_state.customer_name,
    placeholder="Nhập tên khách hàng..."
)

st.session_state.customer_name = customer_name

st.divider()

# =========================
# KHU VỰC CHỌN MÓN
# =========================
st.markdown("### 🧋 Chọn món")

col1, col2 = st.columns(2)

with col1:

    drink = st.selectbox(
        "🥤 Loại trà sữa",
        list(MENU.keys())
    )

    size = st.selectbox(
        "🥛 Size ly",
        list(SIZE_PRICE.keys())
    )

    quantity = st.number_input(
        "🔢 Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )

with col2:

    sugar = st.selectbox(
        "🍬 Mức độ đường",
        SUGAR_LEVEL
    )

    ice = st.selectbox(
        "🧊 Mức độ đá",
        ICE_LEVEL
    )

    toppings = st.multiselect(
        "🍮 Thêm topping",
        list(TOPPINGS.keys())
    )


# =========================
# TÍNH GIÁ MÓN HIỆN TẠI
# =========================
drink_price = MENU[drink]
size_price = SIZE_PRICE[size]

topping_price = sum(
    TOPPINGS[topping]
    for topping in toppings
)

unit_price = drink_price + size_price + topping_price

item_total = unit_price * quantity


# =========================
# HIỂN THỊ GIÁ TẠM TÍNH
# =========================
st.markdown("### 💰 Giá món hiện tại")

price_col1, price_col2, price_col3, price_col4 = st.columns(4)

with price_col1:
    st.metric(
        "Giá trà sữa",
        format_money(drink_price)
    )

with price_col2:
    st.metric(
        "Giá size",
        format_money(size_price)
    )

with price_col3:
    st.metric(
        "Giá topping",
        format_money(topping_price)
    )

with price_col4:
    st.metric(
        "Thành tiền",
        format_money(item_total)
    )


# =========================
# THÊM MÓN
# =========================
if st.button(
    "➕ Thêm món vào hóa đơn",
    use_container_width=True
):

    item = {
        "name": drink,
        "size": size,
        "quantity": quantity,
        "sugar": sugar,
        "ice": ice,
        "toppings": toppings,
        "unit_price": unit_price,
        "total": item_total
    }

    st.session_state.cart.append(item)

    st.success(
        f"Đã thêm {quantity} ly {drink} vào hóa đơn!"
    )

    st.rerun()


st.divider()

# =========================
# DANH SÁCH MÓN ĐÃ CHỌN
# =========================
st.markdown("## 🛒 HÓA ĐƠN HIỆN TẠI")

if len(st.session_state.cart) == 0:

    st.info(
        "Chưa có món nào trong hóa đơn. "
        "Hãy chọn món và nhấn 'Thêm món vào hóa đơn'."
    )

else:

    total_bill = 0

    for index, item in enumerate(
        st.session_state.cart
    ):

        total_bill += item["total"]

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:

                st.markdown(
                    f"### 🧋 {index + 1}. {item['name']}"
                )

                st.write(
                    f"Size: **{item['size']}**"
                )

                st.write(
                    f"Đường: **{item['sugar']}** | "
                    f"Đá: **{item['ice']}**"
                )

                if item["toppings"]:

                    st.write(
                        "Topping: **"
                        + ", ".join(item["toppings"])
                        + "**"
                    )

                else:

                    st.write(
                        "Topping: **Không**"
                    )

            with col2:

                st.write(
                    f"Số lượng: **{item['quantity']}**"
                )

                st.write(
                    f"Đơn giá: "
                    f"**{format_money(item['unit_price'])}**"
                )

                st.write(
                    f"Thành tiền: "
                    f"**{format_money(item['total'])}**"
                )

            with col3:

                if st.button(
                    "🗑️ Xóa",
                    key=f"delete_{index}"
                ):

                    st.session_state.cart.pop(index)

                    st.rerun()


    # =========================
    # TỔNG TIỀN
    # =========================
    st.markdown("### 💵 Tổng tiền")

    st.markdown(
        f"""
        <div style="
            background-color:#f8f9fa;
            padding:20px;
            border-radius:12px;
            text-align:center;
            border:1px solid #ddd;
        ">
            <h3>TỔNG CỘNG</h3>
            <h1>{format_money(total_bill)}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # =========================
    # THANH TOÁN
    # =========================

    if not customer_name.strip():

        st.warning(
            "⚠️ Vui lòng nhập tên khách hàng trước khi thanh toán."
        )

    else:

        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True
        ):

            st.session_state.paid = True

            st.rerun()
