import base64
from pathlib import Path

import streamlit as st

import api
import database as db


# =====================================
# 상수 (CSS)
# =====================================

APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, rgba(35, 76, 48, .22), transparent 36%),
            radial-gradient(ellipse at 90% 18%, rgba(24, 65, 43, .16), transparent 32%),
            #090e0b;
        color: #e8eee8;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    /* 상단 헤더 */
    [data-testid="stHeader"] {
        background: #090e0b !important;
        height: 64px !important;
        min-height: 64px !important;
        position: relative !important;
        top: auto !important;
        z-index: 999 !important;
        border-bottom: 1px solid #344333;
    }

    /* 헤더 안 로고 */
    [data-testid="stHeader"]::after {
        content: "";
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 100px;
        height: 48px;
        background-image: var(--header-logo);
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        pointer-events: none;
    }

    /* 사이드바 전체 디자인 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101a13 0%, #0b110d 100%);
        border-right: 2px solid #344b38;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: #e3ece3;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: #17251b;
        border: 1px solid #344b38;
        border-radius: 10px;
        padding: 12px 14px;
        margin: 0;
        transition: background 0.2s, border 0.2s;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #263d2c;
        border-color: #a0c47e;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label p {
        color: #e3ece3 !important;
        font-size: 15px;
        font-weight: 700;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #345c3b, #203d2a);
        border: 1px solid #a0c47e;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
        color: #f2d878 !important;
        font-weight: 800;
    }

    /* 사이드바 열기 버튼 - 접힌 상태 */
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 99999 !important;
    }

    [data-testid="stSidebarCollapsedControl"] button {
        width: 44px !important;
        height: 44px !important;
        background: #345c3b !important;
        border: 2px solid #f2d878 !important;
        border-radius: 10px !important;
        opacity: 1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stSidebarCollapsedControl"] svg {
        color: #ffffff !important;
        stroke: #ffffff !important;
        fill: none !important;
        opacity: 1 !important;
    }

    /* 사이드바 닫기 버튼 - 펼친 상태 */
    [data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarCollapseButton"] button {
        width: 40px !important;
        height: 40px !important;
        background: #345c3b !important;
        border: 2px solid #f2d878 !important;
        border-radius: 9px !important;
        opacity: 1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="stSidebarCollapseButton"] svg {
        color: #ffffff !important;
        stroke: #ffffff !important;
        fill: none !important;
        opacity: 1 !important;
    }

    [data-testid="stSidebarCollapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #527d4c !important;
        border-color: #ffe58a !important;
    }

    [data-testid="stSidebarCollapsedControl"] *,
    [data-testid="stSidebarCollapseButton"] * {
        opacity: 1 !important;
    }

    /* 로고 헤더 */
    .brand-header {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 4px 0 10px;
        margin: 0 auto 10px;
        background: transparent;
        border-bottom: 1px solid rgba(141, 99, 46, .16);
    }

    .brand-header img {
        display: block;
        width: 100px;
        max-width: 30vw;
        height: auto;
        object-fit: contain;
        filter: drop-shadow(0 3px 5px rgba(0,0,0,.35));
    }

    /* 메인 배너 */
    .home-banner-wrap {
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        overflow: hidden;
        line-height: 0;
    }

    .home-banner-wrap img {
        display: block;
        width: 100%;
        height: clamp(120px, 16vw, 280px);
        object-fit: cover;
        object-position: center center;
    }

    /* 공통 제목 */
    h1, h2, h3 {
        color: #edf5ed !important;
        letter-spacing: -.035em;
        font-weight: 800 !important;
    }

    p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
        color: #c0cec2;
    }

    .hero-kicker {
        color: #9dbb8e;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .22em;
        text-transform: uppercase;
        margin-bottom: .35rem;
    }

    .hero-title {
        color: #f0f5ee;
        font-size: clamp(2rem, 4vw, 3.1rem);
        font-weight: 800;
        letter-spacing: -.06em;
        line-height: 1.05;
        margin: 0;
    }

    .hero-subtitle {
        color: #9eafa1;
        margin-top: .65rem;
        font-size: .98rem;
    }

    .section-label {
        color: #a6c995;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .25rem;
    }

    /* 카드 */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(
            145deg,
            rgba(22, 34, 25, .96),
            rgba(13, 21, 16, .96)
        );
        border: 1px solid #2a3e30 !important;
        border-radius: 16px !important;
    }

    [data-testid="stExpander"] {
        background: rgba(16, 27, 20, .72);
        border: 1px solid #2a3d30;
        border-radius: 13px;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        color: #e5eee5;
        font-weight: 700;
    }

    /* 버튼 */
    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        border: 1px solid #45664b;
        background: linear-gradient(135deg, #24452e, #183322);
        color: #e9f4e8;
        font-weight: 700;
        transition: .18s ease;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        border-color: #8eb77c;
        color: #ffffff;
        background: linear-gradient(135deg, #315b3b, #21432d);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6b914f, #3e693e);
        border: 1px solid #91b978;
        color: #071009;
    }

    /* 입력창 */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background: #0d1710 !important;
        color: #eaf1e9 !important;
        border: 1px solid #354b39 !important;
        border-radius: 9px !important;
    }

    [data-baseweb="select"] > div {
        background: #0d1710;
        border-color: #354b39;
        color: #eaf1e9;
        border-radius: 9px;
    }

    [data-testid="stFileUploader"] section {
        background: #101b14;
        border: 1px dashed #49654d;
        border-radius: 12px;
    }

    /* 통계 */
    [data-testid="stMetric"] {
        background: #122017;
        border: 1px solid #2c4432;
        border-radius: 13px;
        padding: 12px 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #9eb39f;
    }

    [data-testid="stMetricValue"] {
        color: #e6f1e4;
    }

    hr {
        border-color: #2a3b2e;
    }

    [data-testid="stAlert"] {
        background: #17251b;
        border: 1px solid #3b5940;
        color: #dcebdd;
        border-radius: 10px;
    }

    .small-note {
        color: #91a394;
        font-size: .82rem;
    }

    /* 홈 화면 */
    .home-content {
        max-width: 1320px;
        margin: 0 auto;
        padding: 0 28px;
    }

    .home-title {
        text-align: center;
        color: #f2d36b !important;
        font-size: clamp(1.8rem, 3vw, 2.7rem);
        font-weight: 900;
        letter-spacing: -.04em;
        margin-top: 2.1rem;
        margin-bottom: .35rem;
    }

    .home-subtitle {
        text-align: center;
        color: #b7c8b7;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .home-card {
        background: linear-gradient(145deg, #192b1e, #101a13);
        border: 1px solid #405b3e;
        border-radius: 18px;
        padding: 25px 26px;
        min-height: 205px;
        margin-bottom: 18px;
        box-shadow: 0 8px 22px rgba(0,0,0,.18);
    }

    .home-card .number {
        color: #a7c58e;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .16em;
        margin-bottom: 10px;
    }

    .home-card h3 {
        color: #f3d778 !important;
        font-size: 1.4rem;
        margin: 0 0 12px 0;
    }

    .home-card p {
        color: #d0ddcf;
        font-size: 1rem;
        line-height: 1.85;
        margin: 0;
    }

    .home-footer {
        text-align: center;
        color: #819785;
        font-size: .82rem;
        letter-spacing: .12em;
        margin: 28px 0 10px 0;
    }

    @media (max-width: 700px) {
        .home-banner-wrap img {
            height: 250px;
        }

        .home-content {
            padding: 0 14px;
        }
    }

    /* 사이드바 토글 버튼 - 헤더 내부 직접 지정 */
    [data-testid="stHeader"] button {
        opacity: 1 !important;
        visibility: visible !important;
        background-color: #345c3b !important;
        border: 2px solid #f2d878 !important;
        border-radius: 9px !important;
        width: 42px !important;
        height: 42px !important;
        margin-left: 8px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.45) !important;
    }

    [data-testid="stHeader"] button svg {
        color: #ffffff !important;
        stroke: #ffffff !important;
        fill: none !important;
        opacity: 1 !important;
    }

    [data-testid="stHeader"] button svg path {
        stroke: #ffffff !important;
        opacity: 1 !important;
    }

    [data-testid="stHeader"] button:hover {
        background-color: #527d4c !important;
        border-color: #ffe58a !important;
    }

    [data-testid="stSidebar"] button {
        opacity: 1 !important;
        visibility: visible !important;
    }

    [data-testid="stSidebar"] button[kind="header"] {
        background-color: #345c3b !important;
        border: 2px solid #f2d878 !important;
        border-radius: 9px !important;
    }

    [data-testid="stSidebar"] button[kind="header"] svg {
        color: #ffffff !important;
        stroke: #ffffff !important;
        opacity: 1 !important;
    }

    /* 모든 화면 하단 여백 */
    [data-testid="stMainBlockContainer"] {
        padding-bottom: 80px !important;
    }

    [data-testid="stMainBlockContainer"] > div:last-child {
        padding-bottom: 20px;
    }

    [data-testid="stAppViewContainer"] {
        min-height: 100vh;
    }
</style>
"""

RISK_OPTIONS = ["정보 없음", "낮음", "보통", "높음"]
CAPTURE_OPTIONS = ["포획 불가", "포획 실패", "포획 성공"]
HEALTH_OPTIONS = ["양호", "보통", "주의 필요", "정보 없음"]
IMAGE_TYPES = ["png", "jpg", "jpeg"]


# =====================================
# 모델 클래스 (DB 행 -> 객체)
# =====================================

class Species:
    """species 테이블의 한 행을 감싸는 클래스"""

    def __init__(self, row):
        self.row = row

    @property
    def id(self):
        return self.row[0]

    @property
    def inat_id(self):
        return self.row[1]

    @property
    def name(self):
        return self.row[2]

    @property
    def scientific_name(self):
        return self.row[3]

    @property
    def habitat(self):
        return self.row[4]

    @property
    def risk(self):
        return self.row[5]

    @property
    def capture_status(self):
        return self.row[6]

    @property
    def image_url(self):
        return self.row[7]

    @property
    def image_data(self):
        return self.row[8]

    @property
    def memo(self):
        return self.row[9]

    def search_text(self):
        """종 정보 검색용 문자열"""
        return " ".join([
            str(self.name or ""),
            str(self.scientific_name or ""),
            str(self.habitat or "")
        ]).lower()

    def can_register_individual(self):
        return self.capture_status == "포획 성공"


class Individual:
    """individual 테이블의 한 행을 감싸는 클래스"""

    def __init__(self, row):
        self.row = row

    @property
    def id(self):
        return self.row[0]

    @property
    def nickname(self):
        return self.row[2]

    @property
    def age(self):
        return self.row[3]

    @property
    def health(self):
        return self.row[4]

    @property
    def rating(self):
        return self.row[5]

    @property
    def memo(self):
        return self.row[6]

    @property
    def image_url(self):
        return self.row[7]

    @property
    def image_data(self):
        return self.row[8]


# =====================================
# 저장소 클래스 (database.py, api.py 래핑)
# =====================================

class ZooRepository:
    """DB와 외부 API 접근을 한곳에 모은 클래스"""

    def __init__(self):
        db.create_tables()

    # 종
    def get_all_species(self):
        return [Species(row) for row in db.get_species()]

    def species_exists(self, inat_id=None, scientific_name=None):
        if inat_id is None:
            return db.species_exists(scientific_name=scientific_name)
        return db.species_exists(
            inat_id=inat_id,
            scientific_name=scientific_name
        )

    def add_species(self, **kwargs):
        db.add_species(**kwargs)

    def update_species(self, **kwargs):
        db.update_species(**kwargs)

    def delete_species(self, species_id):
        db.delete_species(species_id)

    # 개체
    def get_individuals(self, species_id):
        return [
            Individual(row)
            for row in db.get_individuals(species_id)
        ]

    def add_individual(self, *args, **kwargs):
        db.add_individual(*args, **kwargs)

    def update_individual(self, *args, **kwargs):
        db.update_individual(*args, **kwargs)

    def delete_individual(self, individual_id):
        db.delete_individual(individual_id)

    # 외부 API
    def search_external(self, keyword):
        return api.search_species(keyword)


# =====================================
# 세션 상태 관리 클래스
# =====================================

class SessionManager:
    DEFAULTS = {
        "search_results": [],
        "search_page": 1,
        "search_version": 0,
        "editing_species_id": None,
        "adding_individual_species_id": None,
        "editing_individual_id": None,
        "toast_message": None,
        "my_archive_search_result": ""
    }

    def __init__(self):
        for key, value in self.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = value

        if "active_menu" not in st.session_state:
            st.session_state["active_menu"] = "홈"

    @staticmethod
    def notify(message, icon="✅"):
        st.session_state["toast_message"] = (message, icon)

    @staticmethod
    def show_toast():
        if st.session_state["toast_message"]:
            message, icon = st.session_state["toast_message"]
            st.toast(message, icon=icon)
            st.session_state["toast_message"] = None


# =====================================
# 이미지 / 공통 UI 클래스
# =====================================

class ImageLoader:
    """이미지 파일을 data URI로 변환"""

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def to_data_uri(self, filename):
        image_path = self.base_dir / filename

        if not image_path.exists():
            return None

        mime = (
            "image/png"
            if image_path.suffix.lower() == ".png"
            else "image/jpeg"
        )

        encoded = base64.b64encode(
            image_path.read_bytes()
        ).decode("utf-8")

        return f"data:{mime};base64,{encoded}"


class UIHelper:
    """여러 화면에서 같이 쓰는 UI 함수 모음"""

    @staticmethod
    def show_image(image_data=None, image_url=None, fallback_text="사진 없음"):
        if image_data:
            st.image(image_data, use_container_width=True)
        elif image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.caption(fallback_text)

    @staticmethod
    def apply_style(logo_uri):
        st.markdown(APP_CSS, unsafe_allow_html=True)

        if logo_uri:
            st.markdown(
                f"""
                <style>
                [data-testid="stHeader"] {{
                    --header-logo: url("{logo_uri}");
                }}
                </style>
                """,
                unsafe_allow_html=True
            )


# =====================================
# 페이지 기본 클래스
# =====================================

class Page:
    def __init__(self, repo):
        self.repo = repo

    def render(self):
        raise NotImplementedError


# =====================================
# 홈 화면
# =====================================

class HomePage(Page):
    def __init__(self, repo, banner_uri):
        super().__init__(repo)
        self.banner_uri = banner_uri

    def render(self):
        if self.banner_uri:
            st.markdown(
                f"""
                <div class="home-banner-wrap">
                    <img
                        src="{self.banner_uri}"
                        alt="My Secret Zoos 메인 배너"
                    >
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning(
                "home_banner.png 파일을 app.py와 같은 폴더에 넣어주세요."
            )

        st.markdown('<div class="home-content">', unsafe_allow_html=True)

        st.markdown(
            '<div class="home-title">WELCOME TO MY SECRET ZOOS</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="home-subtitle">'
            '나만의 생물 도감을 만들고, 다양한 생물들을 기록해 보세요!'
            '</div>',
            unsafe_allow_html=True
        )

        guide_col1, guide_col2 = st.columns(2, gap="large")

        with guide_col1:
            st.markdown("""
            <div class="home-card">
                <div class="number">01 · MY ARCHIVE</div>
                <h3>📖 나만의 도감</h3>
                <p>
                    내가 등록한 생물들을 한눈에 확인할 수 있습니다.<br>
                    생물의 이름, 서식지, 위험도, 포획 상태 등의
                    정보를 확인하고 수정해 보세요.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with guide_col2:
            st.markdown("""
            <div class="home-card">
                <div class="number">02 · EXPLORE</div>
                <h3>🔎 새로운 생물 찾기</h3>
                <p>
                    외부 생물 검색 기능으로 다양한 생물들을 찾아볼 수 있습니다.<br>
                    마음에 드는 생물을 선택해 나만의 도감에 등록하세요.
                </p>
            </div>
            """, unsafe_allow_html=True)

        guide_col3, guide_col4 = st.columns(2, gap="large")

        with guide_col3:
            st.markdown("""
            <div class="home-card">
                <div class="number">03 · REGISTER</div>
                <h3>🌿 직접 등록하기</h3>
                <p>
                    검색되지 않는 생물도 직접 등록할 수 있습니다.<br>
                    생물의 사진과 정보를 입력해 나만의 도감을 완성해 보세요.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with guide_col4:
            st.markdown("""
            <div class="home-card">
                <div class="number">04 · INDIVIDUAL</div>
                <h3>🐾 개체 관리</h3>
                <p>
                    포획에 성공한 생물은 개체별로 관리할 수 있습니다.<br>
                    별명, 나이, 건강 상태, 평가와 메모를 기록해 보세요.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            '<div class="home-footer">'
            'MY SECRET ZOOS · BUILD YOUR OWN LITTLE WORLD'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)


# =====================================
# 외부 생물 검색 화면
# =====================================

class SearchPage(Page):
    PER_PAGE = 10

    def add_external_species(self, item):
        if self.repo.species_exists(
            inat_id=item["inat_id"],
            scientific_name=item.get("scientific_name")
        ):
            st.warning("이미 등록된 생물입니다.")
            return

        self.repo.add_species(
            inat_id=item["inat_id"],
            name=item["name"],
            scientific_name=item.get("scientific_name"),
            habitat="정보 없음",
            risk="정보 없음",
            image_url=item.get("image_url"),
            image_data=None,
            capture_status="포획 불가",
            memo=""
        )

        SessionManager.notify(f"{item['name']} 종을 도감에 등록했습니다.")
        st.rerun()

    @staticmethod
    def filter_results(results, keyword):
        keyword_lower = keyword.strip().lower()

        return [
            item
            for item in results
            if keyword_lower in (item.get("name") or "").lower()
            or keyword_lower in (item.get("scientific_name") or "").lower()
        ]

    def render_search_form(self):
        with st.form("search_form"):
            keyword = st.text_input(
                "검색할 생물 이름",
                placeholder="예: tiger, frog, red fox"
            )

            search_button = st.form_submit_button(
                "검색하기",
                use_container_width=True
            )

        if not search_button:
            return

        if not keyword.strip():
            st.warning("검색어를 입력해주세요.")
            return

        search_failed = False

        try:
            with st.spinner("생물 정보를 검색하고 있습니다..."):
                results = self.repo.search_external(keyword.strip())
        except Exception as error:
            st.error(f"생물 검색 중 오류가 발생했습니다: {error}")
            results = []
            search_failed = True

        results = self.filter_results(results, keyword)

        st.session_state["search_results"] = results
        st.session_state["search_page"] = 1
        st.session_state["search_version"] += 1

        if not search_failed and not results:
            st.warning("검색 결과가 없습니다.")

    def render_result_item(self, item):
        with st.container(border=True):
            image_col, info_col, button_col = st.columns([1.1, 3.2, 1.2])

            with image_col:
                if item.get("image_url"):
                    st.image(item["image_url"], use_container_width=True)
                else:
                    st.caption("대표 사진 없음")

            with info_col:
                st.markdown(f"### {item['name']}")
                st.caption(item.get("scientific_name") or "학명 정보 없음")

            with button_col:
                exists = self.repo.species_exists(
                    inat_id=item["inat_id"],
                    scientific_name=item.get("scientific_name")
                )

                st.write("")

                if exists:
                    st.button(
                        "등록 완료",
                        disabled=True,
                        key=f"done_{item['inat_id']}",
                        use_container_width=True
                    )
                elif st.button(
                    "도감에 등록",
                    key=f"add_{item['inat_id']}",
                    use_container_width=True
                ):
                    self.add_external_species(item)

    @staticmethod
    def get_visible_pages(current_page, total_pages):
        if total_pages <= 7:
            return list(range(1, total_pages + 1))

        start_page = max(2, min(current_page - 2, total_pages - 4))
        end_page = min(total_pages - 1, start_page + 4)

        visible_pages = [1]

        if start_page > 2:
            visible_pages.append("...")

        visible_pages.extend(range(start_page, end_page + 1))

        if end_page < total_pages - 1:
            visible_pages.append("...")

        visible_pages.append(total_pages)

        return visible_pages

    def render_pagination(self, current_page, total_pages):
        if total_pages <= 1:
            return

        visible_pages = self.get_visible_pages(current_page, total_pages)
        cols = st.columns(len(visible_pages) + 2)
        version = st.session_state["search_version"]

        with cols[0]:
            if st.button(
                "◀",
                disabled=current_page == 1,
                key=f"prev_{version}",
                use_container_width=True
            ):
                st.session_state["search_page"] -= 1
                st.rerun()

        for index, page in enumerate(visible_pages):
            with cols[index + 1]:
                if page == "...":
                    st.write("...")
                elif st.button(
                    str(page),
                    key=f"page_{version}_{page}",
                    type="primary" if page == current_page else "secondary",
                    use_container_width=True
                ):
                    st.session_state["search_page"] = page
                    st.rerun()

        with cols[-1]:
            if st.button(
                "▶",
                disabled=current_page == total_pages,
                key=f"next_{version}",
                use_container_width=True
            ):
                st.session_state["search_page"] += 1
                st.rerun()

    def render(self):
        st.markdown(
            '<div class="section-label">DISCOVER</div>',
            unsafe_allow_html=True
        )

        st.subheader("🔎 외부 생물 검색")
        st.caption("생물의 일반명 또는 학명을 검색할 수 있습니다.")

        self.render_search_form()

        results = st.session_state["search_results"]

        if not results:
            return

        total_items = len(results)
        total_pages = (total_items + self.PER_PAGE - 1) // self.PER_PAGE

        current_page = max(
            1,
            min(st.session_state["search_page"], total_pages)
        )
        st.session_state["search_page"] = current_page

        page_results = results[
            (current_page - 1) * self.PER_PAGE:
            current_page * self.PER_PAGE
        ]

        st.divider()
        st.subheader("검색 결과")
        st.caption(
            f"전체 {total_items}개 결과 · "
            f"{current_page} / {total_pages} 페이지"
        )

        for item in page_results:
            self.render_result_item(item)

        st.divider()

        self.render_pagination(current_page, total_pages)


# =====================================
# 직접 등록 화면
# =====================================

class RegisterPage(Page):
    def render(self):
        st.markdown(
            '<div class="section-label">NEW SPECIES</div>',
            unsafe_allow_html=True
        )

        st.subheader("➕ 생물 종 직접 등록")

        uploaded_file = st.file_uploader(
            "대표 사진 등록",
            type=IMAGE_TYPES,
            key="direct_image"
        )

        if uploaded_file:
            st.image(uploaded_file, width=260)

        with st.form("direct_register_form"):
            name = st.text_input(
                "일반명",
                placeholder="예: 크레스티드 게코"
            )

            scientific_name = st.text_input(
                "학명",
                placeholder="예: Correlophus ciliatus"
            )

            habitat = st.text_input(
                "서식지",
                placeholder="예: 뉴칼레도니아"
            )

            risk = st.selectbox("위험 등급", RISK_OPTIONS)

            capture_status = st.selectbox("포획 상태", CAPTURE_OPTIONS)

            species_memo = st.text_area(
                "종 메모",
                placeholder="이 종에 관한 특징이나 관찰 내용을 기록하세요."
            )

            submit = st.form_submit_button(
                "생물 등록",
                use_container_width=True
            )

        if submit:
            self.register(
                uploaded_file,
                name,
                scientific_name,
                habitat,
                risk,
                capture_status,
                species_memo
            )

    def register(
        self,
        uploaded_file,
        name,
        scientific_name,
        habitat,
        risk,
        capture_status,
        species_memo
    ):
        if not name.strip():
            st.warning("일반명을 입력해주세요.")

        elif not scientific_name.strip():
            st.warning("학명을 입력해주세요.")

        elif self.repo.species_exists(
            scientific_name=scientific_name.strip()
        ):
            st.warning("이미 등록된 생물입니다.")

        else:
            image_data = (
                uploaded_file.getvalue()
                if uploaded_file
                else None
            )

            self.repo.add_species(
                inat_id=None,
                name=name.strip(),
                scientific_name=scientific_name.strip(),
                habitat=habitat.strip(),
                risk=risk,
                image_url=None,
                image_data=image_data,
                capture_status=capture_status,
                memo=species_memo.strip()
            )

            SessionManager.notify(f"{name} 종을 등록했습니다.")
            st.rerun()


# =====================================
# 내 도감 화면
# =====================================

class ArchivePage(Page):

    # ---------- 종 수정 시작 ----------
    @staticmethod
    def start_species_edit(species):
        species_id = species.id

        st.session_state["editing_species_id"] = species_id
        st.session_state[f"edit_name_{species_id}"] = species.name or ""
        st.session_state[f"edit_scientific_{species_id}"] = (
            species.scientific_name or ""
        )
        st.session_state[f"edit_habitat_{species_id}"] = species.habitat or ""

        st.session_state[f"edit_risk_{species_id}"] = (
            species.risk
            if species.risk in RISK_OPTIONS
            else "정보 없음"
        )

        st.session_state[f"edit_capture_{species_id}"] = (
            species.capture_status
            if species.capture_status in CAPTURE_OPTIONS
            else "포획 불가"
        )

        st.session_state[f"edit_species_memo_{species_id}"] = (
            species.memo or ""
        )

    # ---------- 검색 ----------
    def render_search(self):
        st.markdown("### 🔎 도감 검색")

        with st.form("my_archive_search_form"):
            search_col, button_col = st.columns([5, 1.2])

            with search_col:
                search_input = st.text_input(
                    "생물 이름 또는 개체 별명 검색",
                    placeholder="예: Japanese Moon Moth, 초록이",
                    key="my_archive_search_input"
                )

            with button_col:
                st.write("")
                search_button = st.form_submit_button(
                    "🔎 검색하기",
                    use_container_width=True,
                    type="primary"
                )

            if search_button:
                st.session_state["my_archive_search_result"] = (
                    search_input.strip()
                )

        return st.session_state["my_archive_search_result"].lower()

    def filter_species(self, all_species_list, search_keyword):
        species_list = []
        matching_individual_ids = {}

        for species in all_species_list:
            individuals = self.repo.get_individuals(species.id)

            matched_individuals = [
                individual
                for individual in individuals
                if search_keyword in str(individual.nickname or "").lower()
            ]

            if not search_keyword or search_keyword in species.search_text():
                species_list.append(species)

            elif matched_individuals:
                species_list.append(species)
                matching_individual_ids[species.id] = {
                    individual.id
                    for individual in matched_individuals
                }

        return species_list, matching_individual_ids

    def get_visible_individuals(self, species_id, matching_individual_ids):
        individuals = self.repo.get_individuals(species_id)

        if species_id in matching_individual_ids:
            individuals = [
                individual
                for individual in individuals
                if individual.id in matching_individual_ids[species_id]
            ]

        return individuals

    def render_metrics(self, species_list, matching_individual_ids):
        metric_cols = st.columns(2)

        metric_cols[0].metric("검색된 종", f"{len(species_list)}종")

        total_individuals = 0

        for species in species_list:
            total_individuals += len(
                self.get_visible_individuals(
                    species.id,
                    matching_individual_ids
                )
            )

        metric_cols[1].metric("검색된 개체", f"{total_individuals}개체")

    # ---------- 종 삭제 ----------
    def render_delete(self, species):
        species_id = species.id
        name = species.name

        if st.button(
            "종 삭제",
            key=f"delete_species_{species_id}",
            use_container_width=True
        ):
            st.session_state[f"confirm_delete_{species_id}"] = True
            st.rerun()

        if st.session_state.get(f"confirm_delete_{species_id}", False):
            st.divider()

            st.warning(
                f"'{name}' 종과 해당 종에 속한 모든 개체를 삭제할까요?"
            )

            st.write("")

            confirm_col, cancel_col, empty_col = st.columns([1, 1, 3])

            with confirm_col:
                if st.button(
                    "삭제 확인",
                    key=f"confirm_delete_btn_{species_id}",
                    type="primary",
                    use_container_width=True
                ):
                    self.repo.delete_species(species_id)

                    st.session_state[f"confirm_delete_{species_id}"] = False

                    SessionManager.notify(
                        f"{name} 종과 소속 개체를 삭제했습니다.",
                        "🗑️"
                    )

                    st.rerun()

            with cancel_col:
                if st.button(
                    "취소",
                    key=f"cancel_delete_btn_{species_id}",
                    use_container_width=True
                ):
                    st.session_state[f"confirm_delete_{species_id}"] = False
                    st.rerun()

            st.divider()

    # ---------- 종 사진 ----------
    def render_species_photo(self, species, editing_species):
        UIHelper.show_image(
            species.image_data,
            species.image_url,
            "대표 사진 없음"
        )

        new_species_image = None
        remove_species_image = False

        if editing_species:
            new_species_image = st.file_uploader(
                "종 대표 사진 변경",
                type=IMAGE_TYPES,
                key=f"edit_species_image_{species.id}"
            )

            remove_species_image = st.checkbox(
                "대표 사진 삭제",
                key=f"remove_species_image_{species.id}"
            )

        return new_species_image, remove_species_image

    # ---------- 종 정보 보기 ----------
    def render_species_view(self, species):
        st.write(f"**일반명:** {species.name}")
        st.write(f"**학명:** {species.scientific_name or '정보 없음'}")
        st.write(f"**서식지:** {species.habitat or '정보 없음'}")
        st.write(f"**위험 등급:** {species.risk or '정보 없음'}")
        st.write(f"**포획 상태:** {species.capture_status or '포획 불가'}")

        st.write("**종 메모**")

        st.info(species.memo or "기록된 메모가 없습니다.")

        if st.button(
            "종 정보 수정하기",
            key=f"start_edit_{species.id}",
            use_container_width=True
        ):
            self.start_species_edit(species)
            st.rerun()

    # ---------- 종 정보 수정 ----------
    def render_species_edit(
        self,
        species,
        new_species_image,
        remove_species_image
    ):
        species_id = species.id

        st.subheader("종 정보 수정")

        edit_name = st.text_input("일반명", key=f"edit_name_{species_id}")

        edit_scientific = st.text_input(
            "학명",
            key=f"edit_scientific_{species_id}"
        )

        edit_habitat = st.text_input(
            "서식지",
            key=f"edit_habitat_{species_id}"
        )

        edit_risk = st.selectbox(
            "위험 등급",
            RISK_OPTIONS,
            key=f"edit_risk_{species_id}"
        )

        edit_capture = st.selectbox(
            "포획 상태",
            CAPTURE_OPTIONS,
            key=f"edit_capture_{species_id}"
        )

        edit_species_memo = st.text_area(
            "종 메모",
            key=f"edit_species_memo_{species_id}"
        )

        reset_col, cancel_col, save_col = st.columns(3)

        with reset_col:
            if st.button(
                "정보 초기화하기",
                key=f"reset_species_{species_id}",
                use_container_width=True
            ):
                self.start_species_edit(species)
                st.rerun()

        with cancel_col:
            if st.button(
                "취소하기",
                key=f"cancel_species_{species_id}",
                use_container_width=True
            ):
                st.session_state["editing_species_id"] = None
                st.rerun()

        with save_col:
            if st.button(
                "수정 완료하기",
                key=f"save_species_{species_id}",
                type="primary",
                use_container_width=True
            ):
                self.save_species_edit(
                    species,
                    edit_name,
                    edit_scientific,
                    edit_habitat,
                    edit_risk,
                    edit_capture,
                    edit_species_memo,
                    new_species_image,
                    remove_species_image
                )

    def save_species_edit(
        self,
        species,
        edit_name,
        edit_scientific,
        edit_habitat,
        edit_risk,
        edit_capture,
        edit_species_memo,
        new_species_image,
        remove_species_image
    ):
        if not edit_name.strip():
            st.warning("일반명을 입력해주세요.")
            return

        if not edit_scientific.strip():
            st.warning("학명을 입력해주세요.")
            return

        update_image = False
        image_url = species.image_url
        image_data = species.image_data

        if new_species_image:
            update_image = True
            image_url = None
            image_data = new_species_image.getvalue()

        elif remove_species_image:
            update_image = True
            image_url = None
            image_data = None

        self.repo.update_species(
            species_id=species.id,
            name=edit_name.strip(),
            scientific_name=edit_scientific.strip(),
            habitat=edit_habitat.strip(),
            risk=edit_risk,
            capture_status=edit_capture,
            image_url=image_url,
            image_data=image_data,
            update_image=update_image,
            memo=edit_species_memo.strip()
        )

        st.session_state["editing_species_id"] = None

        SessionManager.notify(f"{edit_name} 종 정보를 수정했습니다.")

        st.rerun()

    # ---------- 개체 한 마리 ----------
    def render_individual(self, species, individual):
        individual_id = individual.id

        with st.container(border=True):
            ind_image_col, ind_info_col, ind_delete_col = st.columns(
                [1, 3, 0.8]
            )

            with ind_image_col:
                if individual.image_data or individual.image_url:
                    UIHelper.show_image(
                        individual.image_data,
                        individual.image_url
                    )
                else:
                    UIHelper.show_image(
                        species.image_data,
                        species.image_url,
                        "개체/종 사진 없음"
                    )

            with ind_info_col:
                st.markdown(f"**{individual.nickname}**")

                st.caption(
                    f"나이 {individual.age} · "
                    f"건강 상태 {individual.health} · "
                    f"평가 {individual.rating}/5"
                )

                if individual.memo:
                    st.write(individual.memo)

                self.render_individual_edit(individual)

            with ind_delete_col:
                st.write("")

                if st.button(
                    "삭제",
                    key=f"delete_individual_{individual_id}",
                    use_container_width=True
                ):
                    self.repo.delete_individual(individual_id)

                    SessionManager.notify(
                        f"{individual.nickname} 개체를 삭제했습니다.",
                        "🗑️"
                    )

                    st.rerun()

    def render_individual_edit(self, individual):
        individual_id = individual.id

        with st.expander("개체 정보 수정"):
            with st.form(f"edit_individual_form_{individual_id}"):
                edit_nickname = st.text_input(
                    "별명",
                    value=individual.nickname or "",
                    key=f"edit_nickname_{individual_id}"
                )

                edit_age = st.number_input(
                    "나이",
                    min_value=0,
                    max_value=1000,
                    value=int(individual.age or 0),
                    key=f"edit_age_{individual_id}"
                )

                current_health = (
                    individual.health
                    if individual.health in HEALTH_OPTIONS
                    else "정보 없음"
                )

                edit_health = st.selectbox(
                    "건강 상태",
                    HEALTH_OPTIONS,
                    index=HEALTH_OPTIONS.index(current_health),
                    key=f"edit_health_{individual_id}"
                )

                rating_value = max(
                    1,
                    min(5, int(individual.rating or 3))
                )

                edit_rating = st.select_slider(
                    "평가",
                    options=[1, 2, 3, 4, 5],
                    value=rating_value,
                    key=f"edit_rating_{individual_id}"
                )

                edit_memo = st.text_area(
                    "메모",
                    value=individual.memo or "",
                    key=f"edit_memo_{individual_id}"
                )

                edit_individual_image = st.file_uploader(
                    "개체 사진 변경",
                    type=IMAGE_TYPES,
                    key=f"edit_individual_image_{individual_id}"
                )

                remove_individual_image = st.checkbox(
                    "개체 사진 삭제(종 대표 사진 사용)",
                    key=f"remove_individual_image_{individual_id}"
                )

                save_individual = st.form_submit_button(
                    "개체 정보 저장",
                    use_container_width=True
                )

            if save_individual:
                self.save_individual_edit(
                    individual,
                    edit_nickname,
                    edit_age,
                    edit_health,
                    edit_rating,
                    edit_memo,
                    edit_individual_image,
                    remove_individual_image
                )

    def save_individual_edit(
        self,
        individual,
        edit_nickname,
        edit_age,
        edit_health,
        edit_rating,
        edit_memo,
        edit_individual_image,
        remove_individual_image
    ):
        if not edit_nickname.strip():
            st.warning("별명을 입력해주세요.")
            return

        update_image = False
        image_url = individual.image_url
        image_data = individual.image_data

        if edit_individual_image:
            update_image = True
            image_url = None
            image_data = edit_individual_image.getvalue()

        elif remove_individual_image:
            update_image = True
            image_url = None
            image_data = None

        self.repo.update_individual(
            individual.id,
            edit_nickname.strip(),
            edit_age,
            edit_health,
            edit_rating,
            edit_memo.strip(),
            image_url=image_url,
            image_data=image_data,
            update_image=update_image
        )

        SessionManager.notify(f"{edit_nickname} 개체 정보를 수정했습니다.")

        st.rerun()

    # ---------- 개체 목록 ----------
    def render_individuals(self, species, matching_individual_ids):
        st.divider()

        individuals = self.get_visible_individuals(
            species.id,
            matching_individual_ids
        )

        st.markdown("#### 🐾 등록된 개체")
        st.caption(f"현재 {len(individuals)}개체")

        if individuals:
            for individual in individuals:
                self.render_individual(species, individual)
        else:
            st.caption("아직 등록된 개체가 없습니다.")

    # ---------- 개체 등록 ----------
    def render_add_individual(self, species):
        species_id = species.id

        if not species.can_register_individual():
            st.caption(
                "포획 상태가 '포획 성공'일 때 개체를 등록할 수 있습니다."
            )
            return

        left_space, register_col = st.columns([4, 1.35])

        with register_col:
            if st.button(
                "＋ 개체 등록",
                key=f"open_add_individual_{species_id}",
                use_container_width=True
            ):
                key = "adding_individual_species_id"

                st.session_state[key] = (
                    None
                    if st.session_state[key] == species_id
                    else species_id
                )

                st.rerun()

        if st.session_state["adding_individual_species_id"] != species_id:
            return

        st.divider()

        st.markdown("#### 새 개체 등록")

        with st.form(f"add_individual_form_{species_id}"):
            nickname = st.text_input(
                "개체 별명",
                placeholder="예: 초록이",
                key=f"new_nickname_{species_id}"
            )

            age = st.number_input(
                "나이",
                min_value=0,
                max_value=1000,
                value=0,
                key=f"new_age_{species_id}"
            )

            health = st.selectbox(
                "건강 상태",
                HEALTH_OPTIONS,
                key=f"new_health_{species_id}"
            )

            rating = st.select_slider(
                "평가",
                options=[1, 2, 3, 4, 5],
                value=3,
                key=f"new_rating_{species_id}"
            )

            individual_memo = st.text_area(
                "메모",
                key=f"new_memo_{species_id}"
            )

            individual_image = st.file_uploader(
                "개체 사진(선택)",
                type=IMAGE_TYPES,
                key=f"new_image_{species_id}"
            )

            st.caption(
                "사진을 등록하지 않으면 종의 대표 사진이 자동으로 표시됩니다."
            )

            add_col, close_col = st.columns(2)

            with add_col:
                add_button = st.form_submit_button(
                    "개체 저장",
                    type="primary",
                    use_container_width=True
                )

            with close_col:
                close_button = st.form_submit_button(
                    "닫기",
                    use_container_width=True
                )

        if close_button:
            st.session_state["adding_individual_species_id"] = None
            st.rerun()

        if add_button:
            if not nickname.strip():
                st.warning("개체 별명을 입력해주세요.")
            else:
                image_data = (
                    individual_image.getvalue()
                    if individual_image
                    else None
                )

                self.repo.add_individual(
                    species_id,
                    nickname.strip(),
                    age,
                    health,
                    rating,
                    individual_memo.strip(),
                    image_url=None,
                    image_data=image_data
                )

                st.session_state["adding_individual_species_id"] = None

                SessionManager.notify(f"{nickname} 개체를 등록했습니다.")

                st.rerun()

    # ---------- 종 카드 ----------
    def render_species_card(self, species, matching_individual_ids):
        species_id = species.id

        editing_species = (
            st.session_state["editing_species_id"] == species_id
        )

        with st.container(border=True):
            title_col, status_col, delete_col = st.columns([5, 1.5, 1])

            with title_col:
                st.markdown(f"### 🌱 {species.name}")
                st.caption(species.scientific_name or "학명 정보 없음")

            with status_col:
                st.write("")
                st.caption(species.capture_status or "포획 불가")

            with delete_col:
                st.write("")
                self.render_delete(species)

            with st.expander("종 정보 및 개체 보기", expanded=False):
                photo_col, info_col = st.columns([1.05, 2.1])

                with photo_col:
                    new_species_image, remove_species_image = (
                        self.render_species_photo(species, editing_species)
                    )

                with info_col:
                    if not editing_species:
                        self.render_species_view(species)
                    else:
                        self.render_species_edit(
                            species,
                            new_species_image,
                            remove_species_image
                        )

                self.render_individuals(species, matching_individual_ids)
                self.render_add_individual(species)

    # ---------- 전체 ----------
    def render(self):
        all_species_list = self.repo.get_all_species()

        search_keyword = self.render_search()

        species_list, matching_individual_ids = self.filter_species(
            all_species_list,
            search_keyword
        )

        self.render_metrics(species_list, matching_individual_ids)

        st.divider()

        if not all_species_list:
            st.info(
                "아직 등록된 생물이 없습니다. "
                "외부 생물 검색 또는 직접 등록을 이용해주세요."
            )

        elif not species_list:
            st.warning(
                f"'{search_keyword}'에 해당하는 생물을 찾을 수 없습니다."
            )

        for species in species_list:
            self.render_species_card(species, matching_individual_ids)


# =====================================
# 메인 앱 클래스
# =====================================

class MySecretZoosApp:
    MENUS = ["홈", "내 도감", "외부 생물 검색", "직접 등록"]

    PAGE_TITLES = {
        "내 도감": (
            "MY WILD ARCHIVE",
            "기록하고, 관찰하고, 나만의 생물 도감을 완성해 보세요."
        ),
        "외부 생물 검색": (
            "EXPLORE SPECIES",
            "iNaturalist에서 새로운 생물 종을 찾아보세요."
        ),
        "직접 등록": (
            "ADD TO ARCHIVE",
            "새로운 생물 종을 직접 기록합니다."
        )
    }

    def __init__(self):
        st.set_page_config(
            page_title="My Secret Zoos",
            page_icon="🌿",
            layout="wide"
        )

        self.repo = ZooRepository()

        base_dir = Path(__file__).resolve().parent
        image_loader = ImageLoader(base_dir)

        self.logo_uri = image_loader.to_data_uri("my_secret_zoos_logo.png")
        self.banner_uri = image_loader.to_data_uri("home_banner.png")

        UIHelper.apply_style(self.logo_uri)

        SessionManager()
        SessionManager.show_toast()

        self.pages = {
            "홈": HomePage(self.repo, self.banner_uri),
            "내 도감": ArchivePage(self.repo),
            "외부 생물 검색": SearchPage(self.repo),
            "직접 등록": RegisterPage(self.repo)
        }

    def render_sidebar(self):
        with st.sidebar:
            st.markdown(
                """
                <div style="
                    padding: 15px 5px 20px;
                    border-bottom: 1px solid #344333;
                    margin-bottom: 15px;
                ">
                    <div style="
                        color: #e9cf75;
                        font-size: 19px;
                        font-weight: 900;
                    ">MY SECRET ZOOS</div>
                    <div style="
                        color: #91a394;
                        font-size: 12px;
                        margin-top: 5px;
                    ">나만의 생물 도감</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    color: #a0c47e;
                    font-size: 11px;
                    font-weight: 800;
                    letter-spacing: 2px;
                    margin: 10px 0 12px 5px;
                ">
                    ☰ NAVIGATION MENU
                </div>
                """,
                unsafe_allow_html=True
            )

            menu = st.radio(
                "메뉴 선택",
                self.MENUS,
                key="active_menu",
                label_visibility="collapsed"
            )

        return menu

    def render_page_title(self, menu):
        if menu == "홈":
            return

        st.markdown(
            '<div class="hero-kicker">FIELD NOTES · SPECIES COLLECTION</div>',
            unsafe_allow_html=True
        )

        title, subtitle = self.PAGE_TITLES[menu]

        st.markdown(
            f'<div class="hero-title">{title}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="hero-subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )

    def run(self):
        menu = self.render_sidebar()

        self.render_page_title(menu)

        st.write("")

        self.pages[menu].render()


# =====================================
# 실행
# =====================================

app = MySecretZoosApp()
app.run()