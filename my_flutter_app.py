from flet import *
import sqlite3

conn = sqlite3.connect("dato.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS student(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tx1 TEXT,
        tx2 TEXT,
        tx3 TEXT,
        tx4 TEXT,
        tx5 TEXT,
        mark2 INTEGER,
        mark3 INTEGER,
        mark4 INTEGER,
        mark5 INTEGER,
        mark6 INTEGER,
        mark7 INTEGER
    )
""")
conn.commit()

students_data = []

def main(page: Page):
    page.scroll = "auto"
    page.window.width = 390
    page.window.height = 730
    page.window.top = 20
    page.window.left = 1150
    page.window.resizable = True
    page.window.title_bar_hidden = False
    page.bgcolor = "white"
    page.theme_mode = ThemeMode.LIGHT

    def update_student_count():
        query = 'SELECT COUNT(*) FROM student'
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

    row_count = update_student_count()

    def add(e):
        cursor.execute("INSERT INTO student (tx1, tx2, tx3, tx4, tx5, mark2, mark3, mark4, mark5, mark6, mark7) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (tx1.value, tx2.value, tx3.value, tx4.value, tx5.value, mark2.value, mark3.value, mark4.value, mark5.value, mark6.value, mark7.value))
        tx1.value = ""
        tx2.value = "" 
        tx3.value = "" 
        tx4.value = "" 
        tx5.value = ""
        mark2.value = ""
        mark3.value = ""
        mark4.value = ""
        mark5.value = ""
        mark6.value = ""
        mark7.value = ""
        conn.commit()
        page.snack_bar = SnackBar(Text("تم اضافة الطالب بنجاح"), bgcolor="blue")
        page.snack_bar.open = True
        page.update()
        row_count_text.value = update_student_count()
        page.update()

    def show(e):
        global students_data
        c = conn.cursor()
        c.execute("SELECT * FROM student")
        students_data = c.fetchall()
        page.go("/sig")

    def delete_selected(e):
        selected_ids = [cb.value for cb in checkboxes if cb.value]
        for student_id in selected_ids:
            cursor.execute("DELETE FROM student WHERE id = ?", (student_id,))
        conn.commit()
        page.snack_bar = SnackBar(Text("تم حذف الطلاب المحددين بنجاح"), bgcolor="blue")
        page.snack_bar.open = True
        page.update()
        row_count_text.value = update_student_count()
        page.update()
        show(e)

    

    tx1 = TextField(label="اسم الطالب", bgcolor=colors.GREEN_50, icon=icons.PERSON, rtl=True, height=38)
    tx2 = TextField(label="اسم الاب", bgcolor=colors.GREEN_50, icon=icons.PERSON, rtl=True, height=38)
    tx3 = TextField(label="اسم الام", bgcolor=colors.GREEN_50, icon=icons.PERSON, rtl=True, height=38)
    tx4 = TextField(label="رقم الهاتق", bgcolor=colors.GREEN_50, icon=icons.PHONE, rtl=True, height=38)
    tx5 = TextField(label="العنوان او السكن", bgcolor=colors.GREEN_50, icon=icons.LOCATION_CITY, rtl=True, height=38)

    mark1 = Text("علامات الطالب", text_align="center", color="blue", font_family="Dubai", size=18)
    mark2 = TextField(label="رياضيات", width=110, rtl=True, height=38, bgcolor=colors.GREEN_50)
    mark3 = TextField(label="عربي", width=110, rtl=True, height=38, bgcolor=colors.GREEN_50)
    mark4 = TextField(label="فرنسي", width=110, rtl=True, height=38, bgcolor=colors.GREEN_50)
    mark5 = TextField(label="انجليزي", width=110, rtl=True, height=38, bgcolor=colors.GREEN_50)
    mark6 = TextField(label="ديانة", width=110, rtl=True, height=38, bgcolor=colors.GREEN_50)
    mark7 = TextField(label="كمياء", width=110, rtl=True, height=38, bgcolor=colors.GREEN_50)

    btn1 = ElevatedButton(
        "اضافة طالب جديد",
        width=170,
        style=ButtonStyle(bgcolor="blue", color="white", padding=15),
        on_click=add
    )

    btn2 = ElevatedButton(
        "عرض الطلاب",
        width=170,
        style=ButtonStyle(bgcolor="blue", color="white", padding=15),
        on_click=show
    )

    row_count_text = Text(row_count, size=19, color="black")

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(
                        bgcolor="#437de7",
                        title=Text("برنامج تسجيل الطلاب ", font_family="Farsi Simple", size=25),
                        center_title=True,
                    ),
                    Container(
                        Image(src="image/omar.png", width=250),
                        padding=padding.only(top=100, right=20),
                        alignment=alignment.center
                    ),
                    Container(
                        content=ElevatedButton("أبدء", bgcolor="#437de7", color=colors.WHITE, on_click=lambda e: page.go("/login")),
                        alignment=alignment.center,
                        padding=padding.only(top=40),
                    ),
                ],
                
            ),
        )
        if page.route == "/login":
            page.views.append(
                View(
                    "/login",
                    [
                        AppBar(
                            bgcolor="#437de7",
                            title=Text("مرحبا بكم ", font_family="Farsi Simple", size=25),
                            center_title=True,
                        ),
                        Container(
                            Image(src="image/logo.gif", width=180),
                            alignment=alignment.center,
                            padding=padding.only(top=20)
                        ),
                        Container(
                            Text("تطبيق تسجيل العلامات", size=25, font_family="Farsi Simple", color="black"),
                            alignment=alignment.center
                        ),
                        Row([
                            Text("عدد الطلاب المسجلين :", size=19, font_family="Dubai", color="blue"),
                            row_count_text,
                        ], alignment=MainAxisAlignment.CENTER, rtl=True),
                        tx1, tx2, tx3, tx4, tx5,
                        Container(
                            mark1,
                            alignment=alignment.center,
                        ),
                        Row([
                            mark2, mark3, mark4,
                        ], alignment=MainAxisAlignment.CENTER, rtl=True),
                        Row([
                            mark5, mark6, mark7,
                        ], alignment=MainAxisAlignment.CENTER, rtl=True),
                        Row([
                            btn1, btn2
                        ], alignment=MainAxisAlignment.CENTER, rtl=True),
                    ],
                    scroll="auto"
                ),
            )
        if page.route == "/sig":
            global checkboxes
            checkboxes = []
            student_cards = []
            for user in students_data:
                cb = Checkbox(value=user[0])
                checkboxes.append(cb)
                
                # حساب مجموع الدرجات
                total_marks = sum([user[6], user[7], user[8], user[9], user[10]])
                status = "🥰 ناجح" if total_marks >= 50 else "😱 راسب"
                status_color = colors.GREEN_900 if total_marks >= 50 else "red"
                student_cards.append(
                    Card(
                        elevation=10,  # زيادة تأثير الظل
                        margin=5,
                        color="blue",
                        content=Column([
                            Container(
                                Text("علامات الطلاب", color=colors.BLACK, weight="bold", text_align="center", size=20, font_family="Arial"),
                                alignment=alignment.center,
                                padding=padding.only(top=0,bottom=1)
                                ),
                            cb,
                            Container(
                                Text(f"اسم الطالب: {user[1]}", color=colors.BLACK, weight="bold", text_align="center", size=18, font_family="Arial"),
                                alignment=alignment.center,
                                padding=padding.only(top=0,bottom=100)
                            ),
                            Row([
                                Text(f"رياضيات: {user[6]}", color="white", weight="bold", size=18, font_family="Arial"),
                                Text(f"عربي: {user[7]}", color="white", weight="bold", size=18, font_family="Arial"),
                                Text(f"انجليزي: {user[9]}", color="white", weight="bold", size=18, font_family="Arial")
                            ], alignment="spaceBetween"),
                            Row([
                                Text(f"ديانة: {user[10]}", color="white", weight="bold", size=18, font_family="Arial"),
                                Text(f"كمياء: {user[8]}", color="white", weight="bold", size=18, font_family="Arial"),
                                Text(f"فرنسي: {user[8]}", color="white", weight="bold", size=18, font_family="Arial")
                            ], alignment="spaceBetween"),
                            Container(
                                Text(f"المجموع: {total_marks}", color=colors.BLACK, weight="bold", text_align="center", size=18, font_family="Arial"),
                                alignment=alignment.center,
                                padding=padding.only(top=0,bottom=12)
                                 ),
                            Container(
                                Text(f"الحالة: {status}", color=status_color, weight="bold", text_align="center", size=18, font_family="Arial"),
                                alignment=alignment.center,
                                padding=padding.only(top=0,bottom=40)
                                 ),

                        ]),
                        
                        
                    )
                )
                page.views.append(
                        View(
                            "/sig",
                            [
                                AppBar(
                                    bgcolor="#437de7",
                                    title=Text("صفحة عرض العلامات ", font_family="Farsi Simple", size=25),
                                    center_title=True,
                                
                                ),
                                Column(student_cards, spacing=10), 
                                Container(
                                    ElevatedButton(
                                    "حذف الطلاب المحددين",
                                    width=170,
                                    style=ButtonStyle(bgcolor="red", color="white", padding=15),
                                    on_click=delete_selected),
                                    alignment=alignment.center,
                                ),
                                
                            ],
                            scroll="auto",
                        ),
                        
                    )
        page.update()


    def page_go(view):
        if len(page.views) > 0:
            page.views.pop()
            back_page = page.views[-0]
            page.go(back_page.route)

    page.on_route_change = route_change
    page.on_view_pop = page_go
    page.go(page.route)

app(main)