# 路由設計文件 (API Design)

## 1. 路由總覽列表
| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 食譜列表 (首頁) | `GET` | `/` | `templates/recipes/index.html` | 顯示所有食譜，支援 `?q=` 查詢參數進行名稱/食材搜尋。 |
| 新增食譜頁面 | `GET` | `/recipes/new` | `templates/recipes/form.html` | 顯示空白的新增食譜表單。 |
| 建立食譜 | `POST` | `/recipes` | — | 接收表單資料、存入 DB，成功後重導回首頁。 |
| 食譜明細 | `GET` | `/recipes/<int:id>` | `templates/recipes/show.html` | 顯示特定食譜的食材與步驟。若查無資料回傳 404。 |
| 編輯食譜頁面 | `GET` | `/recipes/<int:id>/edit` | `templates/recipes/form.html` | 顯示現有食譜資料供修改。 |
| 更新食譜 | `POST` | `/recipes/<int:id>/update` | — | 接收更新表單並寫回 DB，完成後重導至食譜明細。 |
| 刪除食譜 | `POST` | `/recipes/<int:id>/delete` | — | 從 DB 中刪除該筆資料，完成後重導回首頁。 |

---

## 2. 路由詳細說明

### `GET /` (食譜列表)
- **輸入**: URL 查詢參數 `?q=keyword` (可選)
- **處理邏輯**: 
  - 若有 `q` 則呼叫 `Recipe.get_all(q)` 並搜尋。
  - 若無則呼叫 `Recipe.get_all()` 取得最新食譜清單。
- **輸出**: 渲染 `recipes/index.html`，傳入食譜列表變數 `recipes`。
- **錯誤處理**: 資料庫如讀取錯誤報 500。

### `GET /recipes/new` (新增輸入頁面)
- **輸入**: 無
- **處理邏輯**: 準備畫面即可。
- **輸出**: 渲染 `recipes/form.html`。
- **錯誤處理**: 無特殊錯誤。

### `POST /recipes` (建立食譜)
- **輸入**: Form Data 包含 `title`, `description`, `ingredients`, `steps`。
- **處理邏輯**: 接收 Form，呼叫 `Recipe.create(data)`。
- **輸出**: Http 302 重新導向至 `/` (首頁)。
- **錯誤處理**: 若 `title`, `ingredients`, `steps` 等必填欄位缺失，透過 Flash Message 提示並導回 `/recipes/new`。

### `GET /recipes/<int:id>` (食譜明細)
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 取得指定食譜。
- **輸出**: 渲染 `recipes/show.html`，傳入 `recipe`。
- **錯誤處理**: 若 `recipe` 為空 (None)，拋出 HTTP 404 (Not Found)。

### `GET /recipes/<int:id>/edit` (編輯食譜頁面)
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id(id)` 取得指定食譜。
- **輸出**: 渲染 `recipes/form.html`，傳入 `recipe` 將現有值帶入欄位。
- **錯誤處理**: 若查無結果，拋出 404。

### `POST /recipes/<int:id>/update` (更新食譜)
- **輸入**: URL 參數 `id` 與被更新的表單資料。
- **處理邏輯**: 呼叫 `Recipe.update(id, data)`。
- **輸出**: 更新成功後重新導向回詳細頁面 `/recipes/<id>`。
- **錯誤處理**: 查無食譜 (404) 或欄位缺失等驗證同建立食譜的處理方式。

### `POST /recipes/<int:id>/delete` (刪除食譜)
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Recipe.delete(id)` 進行刪除。
- **輸出**: 刪除成功後重新導向至 `/`。
- **錯誤處理**: 若查無食譜則拋出 404。

---

## 3. Jinja2 模板清單

以下檔案後續將於 `app/templates` 建立：
1. `base.html`: 包含全站共用的 `<head>`、導覽列與外觀樣式。
2. `recipes/index.html`: 繼承 `base.html`，以卡片或列表結構呈現食譜總覽。
3. `recipes/show.html`: 繼承 `base.html`，全版詳細呈現食材清單與步驟說明。
4. `recipes/form.html`: 繼承 `base.html`，一個頁面同時支援新增 (Create) 與編輯 (Update)。依據後端是否丟出已存在的 `recipe` 來判斷是 POST 到 `/recipes` 或 `/recipes/<id>/update`。
