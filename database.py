import sqlite3

DB_NAME = "species.db"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _add_missing_columns(cur, table_name, columns):
    cur.execute(f"PRAGMA table_info({table_name})")
    existing = [row[1] for row in cur.fetchall()]

    for column, definition in columns.items():
        if column not in existing:
            cur.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column} {definition}"
            )


def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # 생물 종 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inat_id INTEGER,
            name TEXT NOT NULL,
            scientific_name TEXT,
            habitat TEXT,
            risk TEXT,
            capture_status TEXT DEFAULT '포획 불가',
            image_url TEXT,
            image_data BLOB,
            memo TEXT
        )
    """)

    # 기존 테이블에 빠진 컬럼 추가
    _add_missing_columns(cur, "species", {
        "inat_id": "INTEGER",
        "name": "TEXT",
        "scientific_name": "TEXT",
        "habitat": "TEXT",
        "risk": "TEXT",
        "capture_status": "TEXT DEFAULT '포획 불가'",
        "image_url": "TEXT",
        "image_data": "BLOB",
        "memo": "TEXT"
    })

    # 개체 테이블
    cur.execute("""
        CREATE TABLE IF NOT EXISTS individuals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species_id INTEGER,
            nickname TEXT,
            age INTEGER,
            health TEXT,
            rating INTEGER,
            memo TEXT,
            image_url TEXT,
            image_data BLOB,
            FOREIGN KEY (species_id)
                REFERENCES species(id)
                ON DELETE CASCADE
        )
    """)

    # 기존 개체 테이블에 사진 컬럼 추가
    _add_missing_columns(cur, "individuals", {
        "species_id": "INTEGER",
        "nickname": "TEXT",
        "age": "INTEGER",
        "health": "TEXT",
        "rating": "INTEGER",
        "memo": "TEXT",
        "image_url": "TEXT",
        "image_data": "BLOB"
    })

    conn.commit()
    conn.close()


# =====================================
# 생물 종 관련 함수
# =====================================

def add_species(
    inat_id,
    name,
    scientific_name,
    habitat,
    risk,
    image_url=None,
    image_data=None,
    capture_status="포획 불가",
    memo=""
):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO species (
            inat_id, name, scientific_name, habitat, risk,
            capture_status, image_url, image_data, memo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inat_id,
        name,
        scientific_name,
        habitat,
        risk,
        capture_status,
        image_url,
        image_data,
        memo
    ))

    conn.commit()
    conn.close()


def get_species():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, inat_id, name, scientific_name,
               habitat, risk, capture_status,
               image_url, image_data, memo
        FROM species
        ORDER BY id DESC
    """)

    result = cur.fetchall()
    conn.close()

    return result


def get_species_by_id(species_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, inat_id, name, scientific_name,
               habitat, risk, capture_status,
               image_url, image_data, memo
        FROM species
        WHERE id = ?
    """, (species_id,))

    result = cur.fetchone()
    conn.close()

    return result


def update_species(
    species_id,
    name,
    scientific_name,
    habitat,
    risk,
    capture_status,
    image_url=None,
    image_data=None,
    update_image=False,
    memo=None
):
    conn = connect_db()
    cur = conn.cursor()

    if update_image:
        cur.execute("""
            UPDATE species
            SET name = ?,
                scientific_name = ?,
                habitat = ?,
                risk = ?,
                capture_status = ?,
                image_url = ?,
                image_data = ?,
                memo = ?
            WHERE id = ?
        """, (
            name,
            scientific_name,
            habitat,
            risk,
            capture_status,
            image_url,
            image_data,
            memo,
            species_id
        ))

    else:
        cur.execute("""
            UPDATE species
            SET name = ?,
                scientific_name = ?,
                habitat = ?,
                risk = ?,
                capture_status = ?,
                memo = ?
            WHERE id = ?
        """, (
            name,
            scientific_name,
            habitat,
            risk,
            capture_status,
            memo,
            species_id
        ))

    conn.commit()
    conn.close()


def update_species_memo(species_id, memo):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE species SET memo = ? WHERE id = ?",
        (memo, species_id)
    )

    conn.commit()
    conn.close()


def delete_species(species_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM individuals WHERE species_id = ?",
        (species_id,)
    )

    cur.execute(
        "DELETE FROM species WHERE id = ?",
        (species_id,)
    )

    conn.commit()
    conn.close()


def species_exists(inat_id=None, scientific_name=None):
    conn = connect_db()
    cur = conn.cursor()

    if inat_id is not None:
        cur.execute(
            "SELECT id FROM species WHERE inat_id = ?",
            (inat_id,)
        )

        if cur.fetchone():
            conn.close()
            return True

    if scientific_name:
        cur.execute("""
            SELECT id FROM species
            WHERE LOWER(scientific_name) = LOWER(?)
        """, (scientific_name,))

        if cur.fetchone():
            conn.close()
            return True

    conn.close()
    return False


# =====================================
# 개체 관련 함수
# =====================================

def add_individual(
    species_id,
    nickname,
    age,
    health,
    rating,
    memo,
    image_url=None,
    image_data=None
):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO individuals (
            species_id, nickname, age, health, rating,
            memo, image_url, image_data
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        species_id,
        nickname,
        age,
        health,
        rating,
        memo,
        image_url,
        image_data
    ))

    conn.commit()
    conn.close()


def get_individuals(species_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, species_id, nickname, age, health,
               rating, memo, image_url, image_data
        FROM individuals
        WHERE species_id = ?
        ORDER BY id DESC
    """, (species_id,))

    result = cur.fetchall()
    conn.close()

    return result


def update_individual(
    individual_id,
    nickname,
    age,
    health,
    rating,
    memo,
    image_url=None,
    image_data=None,
    update_image=False
):
    conn = connect_db()
    cur = conn.cursor()

    if update_image:
        cur.execute("""
            UPDATE individuals
            SET nickname = ?,
                age = ?,
                health = ?,
                rating = ?,
                memo = ?,
                image_url = ?,
                image_data = ?
            WHERE id = ?
        """, (
            nickname,
            age,
            health,
            rating,
            memo,
            image_url,
            image_data,
            individual_id
        ))

    else:
        cur.execute("""
            UPDATE individuals
            SET nickname = ?,
                age = ?,
                health = ?,
                rating = ?,
                memo = ?
            WHERE id = ?
        """, (
            nickname,
            age,
            health,
            rating,
            memo,
            individual_id
        ))

    conn.commit()
    conn.close()


def delete_individual(individual_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM individuals WHERE id = ?",
        (individual_id,)
    )

    conn.commit()
    conn.close()