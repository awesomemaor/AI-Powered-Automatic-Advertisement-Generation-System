from fastapi import FastAPI
from .auth_login import router as login_router

app = FastAPI()
app.include_router(login_router)

# קובץ זה משמש כנקודת כניסה מרכזית ל-FastAPI עבור האפליקציה.
# הוא מרכז את כל הנתיבים (routes) ממודולים שונים – לדוגמה: auth_login, auth_register וכו'.
# שימוש ב-routers (באמצעות APIRouter) מאפשר:
# ✅ הפרדת אחריות – כל מודול מכיל רק את הנתיבים והלוגיקה שקשורים אליו.
# ✅ תחזוקה נוחה – קל להוסיף או לערוך נתיב בלי לגעת בכל הקוד.
# ✅ קריאות גבוהה – האפליקציה בנויה בצורה מסודרת ומודולרית.
# ✅ שיפור סקלאביליות – מאפשר להרחיב את המערכת בקלות בעתיד.
# לדוגמה: ניתן להוסיף auth_register.py ולכלול אותו כאן בקלות עם include_router.
