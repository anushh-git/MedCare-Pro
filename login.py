import streamlit as st
import hashlib


# PASSWORD HASHING

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# USERS

USERS = {
    "admin": hash_password("admin123"),
    "manager": hash_password("manager123"),
    "pharmacist": hash_password("pharma123")
}


# AUTHENTICATION

def authenticate(username, password):

    if username not in USERS:
        return False

    return USERS[username] == hash_password(password)


# LOGIN PAGE

def show_login():

    st.markdown("""
    <style>

    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    .stApp{
        background:
        radial-gradient(circle at top left,
        rgba(59,130,246,0.35),
        transparent 30%),

        radial-gradient(circle at bottom right,
        rgba(139,92,246,0.35),
        transparent 30%),

        linear-gradient(
        135deg,
        #07111f,
        #0f172a,
        #111827
        );
    }

    .main-title{
        text-align:center;
        font-size:52px;
        font-weight:800;
        color:white;
        margin-bottom:5px;
    }

    .sub-title{
        text-align:center;
        color:#cbd5e1;
        font-size:16px;
        margin-bottom:30px;
    }

    .stTextInput label{
        color:white !important;
        font-weight:600 !important;
    }

    .stTextInput input{

        background:rgba(
        255,
        255,
        255,
        0.08
        ) !important;

        border:1px solid rgba(
        255,
        255,
        255,
        0.12
        ) !important;

        border-radius:12px !important;

        color:white !important;
    }

    .stButton button{

        width:100%;

        height:55px;

        border:none !important;

        border-radius:12px !important;

        font-size:17px !important;

        font-weight:700 !important;

        color:white !important;

        background:
        linear-gradient(
        135deg,
        #3b82f6,
        #8b5cf6
        ) !important;
    }

    .stButton button:hover{

        transform:translateY(-2px);

        box-shadow:
        0 10px 25px
        rgba(
        59,
        130,
        246,
        0.4
        );
    }

    </style>
    """, unsafe_allow_html=True)

    
    left, center, right = st.columns([1, 1.2, 1])

    with center:

        st.markdown("<br><br>", unsafe_allow_html=True)

        with st.container(border=True):

            st.markdown(
                """
                <div class='main-title'>
                MedCare Pro
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class='sub-title'>
                👋 Hey! Let's Get You Logged In
                </div>
                """,
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Enter Username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter Password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            login = st.button(
                "Secure Login",
                use_container_width=True
            )

            if login:

                if authenticate(
                    username,
                    password
                ):

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success(
                        "Login Successful"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username or Password"
                    )

        st.markdown(
            """
            <div style="
            text-align:center;
            color:#94a3b8;
            margin-top:20px;
            ">
            © 2026 MedCare Pro Enterprise Edition
            </div>
            """,
            unsafe_allow_html=True
        )