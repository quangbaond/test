import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from ttkthemes import ThemedTk

from database import Database
from script1 import script1

import threading


class Application():
    def __init__(self):
        self.root = self.create_main_window()
        self.db = Database()
        self.threadParent = []
        self.threads = []

    def create_main_window(self):
        self.version = '0.0.1'
        root = ThemedTk(theme="black")
        root.geometry('1200x800')
        root.resizable(False, False)
        root.title('SEO Tool version:' + ' ' + self.version)
        root.wm_iconbitmap(r'D:/toolcuong/icon.ico')
        self.add_menu_bar(root)
        self.add_layout(root)
        return root

    def add_menu_bar(self, root):
        menu_bar = tk.Menu(root)

        # add direct options to the menu bar
        menu_bar.add_command(label="Proxy", command=self.open_proxy_window)
        menu_bar.add_command(label="User-Agent",
                             command=self.open_user_agent_window)

        # set menu bar
        root.config(menu=menu_bar)

    def add_layout(self, root):
        frame1 = ttk.Frame(root)
        frame2 = ttk.Frame(root)

        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # create table on the left
        self.tree = ttk.Treeview(frame1)
        self.tree["columns"] = ("stt", "name", "proxy",
                                "tu_khoa", "trang_thai", "user_agent", "url_seo", 'number_thread', 'num_seo')
        self.tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
        self.tree.column("stt", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("name", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("proxy", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("tu_khoa", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("trang_thai", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("user_agent", width=100, minwidth=80, stretch=tk.NO)
        self.tree.column("url_seo", width=200, minwidth=80, stretch=tk.NO)
        self.tree.column("number_thread", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("num_seo", width=80, minwidth=80, stretch=tk.NO)

        self.tree.heading("stt", text="STT")
        self.tree.heading("name", text="Name")
        self.tree.heading("proxy", text="Proxy")
        self.tree.heading("tu_khoa", text="Từ khóa")
        self.tree.heading("trang_thai", text="Trạng Thái")
        self.tree.heading("user_agent", text="User-Agent")
        self.tree.heading("url_seo", text="Đường dẫn cần SEO")
        self.tree.heading("number_thread", text="Số luồng")
        self.tree.heading("num_seo", text="Số lần SEO")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # create entry fields id chrome
        chrome_id_label = ttk.Label(frame2, text="ID Chrome:")
        chrome_id_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.chrome_id_entry = ttk.Entry(frame2, width=30)
        self.chrome_id_entry.grid(row=1, column=0, sticky='e', padx=5, pady=5)

        # create entry fields on the right
        ua_label = ttk.Label(frame2, text="Chọn user-agent:")
        ua_label.grid(row=2, column=0, sticky='w')
        self.ua_user_agent = ttk.Combobox(
            frame2, width=30, state='readonly')
        # get all user-agent from database

        self.ua = Database().get_user_agents()
        self.user_agents = map(lambda x: x[2], self.ua)
        self.ua_user_agent['values'] = ('', *self.user_agents)
        self.ua_user_agent.grid(row=3, column=0, sticky='e', padx=5, pady=5)

        # create proxy combobox
        proxy_label = ttk.Label(frame2, text="Chọn proxy:")
        proxy_label.grid(row=4, column=0, sticky='w')
        self.proxy_combobox = ttk.Combobox(
            frame2, width=30, state='readonly')
        self.proxies = Database().get_proxies()
        # get ip and port from proxies
        self.proxies = map(lambda x: x[1]+':'+x[2], self.proxies)
        self.proxy_combobox['values'] = ('', *self.proxies)
        self.proxy_combobox.grid(row=5, column=0, sticky='e', padx=5, pady=5)

        # create entry fields list script
        keyword_label = ttk.Label(frame2, text="Từ khóa tìm kiếm:")
        keyword_label.grid(row=6, column=0, sticky='w', padx=5, pady=5)
        self.keyword = ttk.Entry(frame2, width=30)
        self.keyword.grid(row=7, column=0, sticky='e', padx=5, pady=5)

        url_seo_label = ttk.Label(frame2, text="Đường dẫn cần Seo:")
        url_seo_label.grid(row=8, column=0, sticky='w', padx=5, pady=5)
        self.url_seo = ttk.Entry(frame2, width=30)
        self.url_seo.grid(row=9, column=0, sticky='e', padx=5, pady=5)

        # create entry fields number of threads
        thread_label = ttk.Label(frame2, text="Số luồng:")
        thread_label.grid(row=12, column=0, sticky='w', padx=5, pady=5)

        self.thread_entry = ttk.Entry(frame2, width=30)
        self.thread_entry.grid(row=13, column=0, sticky='e', padx=5, pady=5)

        # create entry fields number of seo
        seo_label = ttk.Label(frame2, text="Số lần SEO:")
        seo_label.grid(row=14, column=0, sticky='w', padx=5, pady=5)

        self.seo_entry = ttk.Entry(frame2, width=30)
        self.seo_entry.grid(row=15, column=0, sticky='e', padx=5, pady=5)

        # create button add new
        add_button = ttk.Button(
            frame2, text="Thêm mới", width=30, padding=5, cursor="hand2", style="Accent.TButton", command=self.add_new_chrome)
        add_button.grid(row=16, column=0, sticky='e', padx=5, pady=5)

        # create button start
        start_button = ttk.Button(
            frame2, text="Bắt đầu", width=30, padding=5, cursor="hand2", style="Accent.TButton", command=self.run_script)
        start_button.grid(row=18, column=0, sticky='e', padx=5, pady=5)

    def open_user_agent_window(self):
        def add_user_agent_to_db():
            name = name_entry.get()
            user_agent = user_agent_entry.get()
            self.db.insert_user_agent(name, user_agent)
            refresh_tree()

        def refresh_tree():
            for i in self.tree.get_children():
                self.tree.delete(i)

            for count, row in enumerate(self.db.get_user_agents(), start=1):
                self.tree.insert('', 'end', values=(count, *row[1:]))

        def confirm_and_delete(item):
            # Access the item's values
            item_values = self.tree.item(item)['values']
            if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa user agent này?"):
                # The id is found in the first column
                self.db.remove_user_agent(item_values[0])
                refresh_tree()

        def show_context_menu(event):
            self.tree.identify_row(event.y)
            item = self.tree.identify('item', event.x, event.y)
            if item:
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(
                    label="Xóa", command=lambda: confirm_and_delete(item))
                menu.post(event.x_root, event.y_root)

        user_agent_window = tk.Toplevel(self.root)
        user_agent_window.title("User-Agent Settings")
        user_agent_window.geometry('800x600')

        # create table
        columns = ("STT", "Name", "User Agent")
        self.tree = ttk.Treeview(user_agent_window,
                                 columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w")
        self.tree.bind("<Button-3>", show_context_menu)

        # create input fields and update button within a LabelFrame
        input_frame = ttk.LabelFrame(
            user_agent_window, text="User-Agent Input", padding="10 20 10 20")

        name_label = ttk.Label(input_frame, text='Name')
        name_label.grid(column=0, row=0, padx=10, pady=10)
        name_entry = ttk.Entry(input_frame)
        name_entry.grid(column=0, row=1, padx=10, pady=10)

        user_agent_label = ttk.Label(input_frame, text='User Agent')
        user_agent_label.grid(column=1, row=0, padx=10, pady=10)
        user_agent_entry = ttk.Entry(input_frame)
        user_agent_entry.grid(column=1, row=1, padx=10, pady=10)

        update_button = ttk.Button(
            input_frame, text='Cập nhật', command=add_user_agent_to_db)
        update_button.grid(column=2, row=1, padx=10, pady=10)

        # grid and pack the frames
        self.tree.grid(column=0, row=0, pady=20, sticky="nsew")
        input_frame.grid(column=0, row=1, pady=20)

        # configure the grid
        user_agent_window.grid_columnconfigure(0, weight=1)
        user_agent_window.grid_rowconfigure(0, weight=1)
        refresh_tree()

    def open_proxy_window(self):
        def add_proxy_to_db():
            ip = ip_entry.get()
            port = port_entry.get()
            username = username_entry.get()
            password = password_entry.get()
            self.db.insert_proxy(ip, port, username, password)
            refresh_tree()

        def refresh_tree():
            for i in self.tree.get_children():
                self.tree.delete(i)

            for count, row in enumerate(self.db.get_proxies(), start=1):
                self.tree.insert('', 'end', values=(count, *row[1:]))

        def confirm_and_delete(item):
            # Access the item's values
            item_values = self.tree.item(item)['values']
            if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa proxy này?"):
                # The id is found in the second column
                self.db.remove_proxy(item_values[0])
                refresh_tree()

        def show_context_menu(event):
            self.tree.identify_row(event.y)
            item = self.tree.identify('item', event.x, event.y)
            if item:
                menu = tk.Menu(self.root, tearoff=0)
                menu.add_command(
                    label="Xóa", command=lambda: confirm_and_delete(item))
                menu.post(event.x_root, event.y_root)

        def getProxy():
            return self.db.get_proxies()
        proxy_window = tk.Toplevel(self.root)
        proxy_window.title("Proxy Settings")
        proxy_window.geometry('800x600')

        # create table
        columns = ("STT", "IP", "Port", "Username", "Password")
        self.tree = ttk.Treeview(
            proxy_window, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.bind("<Button-3>", show_context_menu)
        # create input fields and update button within a LabelFrame
        input_frame = ttk.LabelFrame(
            proxy_window, text="Proxy Input", padding="10 20 10 20")

        ip_label = ttk.Label(input_frame, text='IP')
        ip_label.grid(column=0, row=0, padx=10, pady=10)
        ip_entry = ttk.Entry(input_frame)
        ip_entry.grid(column=0, row=1, padx=10, pady=10)

        port_label = ttk.Label(input_frame, text='Port')
        port_label.grid(column=1, row=0, padx=10, pady=10)
        port_entry = ttk.Entry(input_frame)
        port_entry.grid(column=1, row=1, padx=10, pady=10)

        username_label = ttk.Label(input_frame, text='Username')
        username_label.grid(column=2, row=0, padx=10, pady=10)
        username_entry = ttk.Entry(input_frame)
        username_entry.grid(column=2, row=1, padx=10, pady=10)

        password_label = ttk.Label(input_frame, text='Password')
        password_label.grid(column=3, row=0, padx=10, pady=10)
        password_entry = ttk.Entry(input_frame)
        password_entry.grid(column=3, row=1, padx=10, pady=10)

        update_button = ttk.Button(
            input_frame, text='Cập nhật', command=add_proxy_to_db)
        update_button.grid(column=4, row=1, padx=10, pady=10)

        # grid and pack the frames
        self.tree.grid(column=0, row=0, pady=20, sticky="nsew")
        input_frame.grid(column=0, row=1, pady=20)

        # configure the grid
        proxy_window.grid_columnconfigure(0, weight=1)
        proxy_window.grid_rowconfigure(0, weight=1)
        refresh_tree()

        # proxy_window.mainloop()

    def add_new_chrome(self):
        id_chrome = self.chrome_id_entry.get()
        if not id_chrome:
            showinfo("Thông báo", "Vui lòng nhập ID Chrome!")
            return
        keyword = self.keyword.get()
        if not keyword:
            showinfo("Thông báo", "Vui lòng nhập từ khóa!")
            return
        url_seo = self.url_seo.get()
        if not url_seo:
            showinfo("Thông báo", "Vui lòng nhập đường dẫn cần SEO!")
            return
        number_thread = self.thread_entry.get()
        num_seo = self.seo_entry.get()

        user_agent = self.ua_user_agent.get() or None
        proxy = self.proxy_combobox.get() or None

        # add treeview
        last_row = len(self.tree.get_children()) + 1
        self.tree.insert('', 'end', values=(
            last_row, id_chrome, proxy, keyword, 'Sẵn sàng', user_agent, url_seo, number_thread, num_seo))
        # clear entry fields
        self.chrome_id_entry.delete(0, 'end')
        self.keyword.delete(0, 'end')
        self.url_seo.delete(0, 'end')
        self.thread_entry.delete(0, 'end')
        self.seo_entry.delete(0, 'end')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Application()
    app.run()
