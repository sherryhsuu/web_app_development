import sqlite3
import os

# 設定資料庫檔案路徑 (對應到 instance/database.db)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳與 SQLite 資料庫的連線"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 將回傳結果結構化為 Dictionary 而不是 Tuple
    conn.row_factory = sqlite3.Row
    return conn

class Recipe:
    @staticmethod
    def create(title, ingredients, steps):
        """新增食譜"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO recipes (title, ingredients, steps) VALUES (?, ?, ?)',
            (title, ingredients, steps)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        """取得所有食譜清單"""
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return recipes

    @staticmethod
    def get_by_id(recipe_id):
        """用 ID 取得單一食譜"""
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return recipe

    @staticmethod
    def update(recipe_id, title, ingredients, steps):
        """更新食譜內容"""
        conn = get_db_connection()
        conn.execute(
            'UPDATE recipes SET title = ?, ingredients = ?, steps = ? WHERE id = ?',
            (title, ingredients, steps, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        """刪除食譜"""
        conn = get_db_connection()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_by_keyword(keyword):
        """透過關鍵字搜尋食譜名稱"""
        conn = get_db_connection()
        # 使用 LIKE 達成包含字串搜尋
        search_query = f"%{keyword}%"
        recipes = conn.execute(
            'SELECT * FROM recipes WHERE title LIKE ? ORDER BY created_at DESC', 
            (search_query,)
        ).fetchall()
        conn.close()
        return recipes

    @staticmethod
    def recommend_by_ingredients(ingredients_string):
        """利用食材比對推薦適合的食譜 (MVP簡易版)"""
        # MVP 階段直接對食材欄位做關鍵字搜尋
        conn = get_db_connection()
        search_query = f"%{ingredients_string}%"
        recipes = conn.execute(
            'SELECT * FROM recipes WHERE ingredients LIKE ? ORDER BY created_at DESC', 
            (search_query,)
        ).fetchall()
        conn.close()
        return recipes
