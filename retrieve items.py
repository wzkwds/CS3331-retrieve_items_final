import tkinter as tk
from tkinter import messagebox, simpledialog


class Item:
    def __init__(self, name, description, address, contact_phone, email, additional_attributes=None):
        self.name = name
        self.description = description
        self.address = address
        self.contact_phone = contact_phone
        self.email = email
        self.additional_attributes = additional_attributes if additional_attributes else {}

    def __str__(self):
        attrs = "\n".join(f"{key}: {value}" for key, value in self.additional_attributes.items())
        return (
            f"名称: {self.name}\n描述: {self.description}\n地址: {self.address}\n" +
            f"联系电话号码: {self.contact_phone}\n邮箱: {self.email}\n{attrs}\n"
        )


class ItemType:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes


class ReviveItems:
    def __init__(self):
        self.items = []
        self.item_types = {}

    def add_item_type(self, type_name, attributes):
        if type_name in self.item_types:
            return f"物品类型 '{type_name}' 已经存在."
        self.item_types[type_name] = ItemType(type_name, attributes)
        return f"物品类型 '{type_name}' 已经被添加."

    def modify_item_type(self, type_name, attributes):
        if type_name not in self.item_types:
            return f"物品类型 '{type_name}' 不存在."
        self.item_types[type_name].attributes = attributes
        return f"物品类型 '{type_name}' 已经被修改."

    def add_item(self, item_type, name, description, address, contact_phone, email, additional_attributes):
        if item_type not in self.item_types:
            return f"物品 '{item_type}' 不存在."
        expected_attributes = self.item_types[item_type].attributes
        if not all(attr in additional_attributes for attr in expected_attributes):
            return "缺失该物品类型的一些属性，请检查."
        item = Item(name, description, address, contact_phone, email, additional_attributes)
        self.items.append(item)
        return f"物品 '{name}' 已经被添加."

    def show_items(self):
        if not self.items:
            return "目前不存在物品."
        return "\n".join(str(item) for item in self.items)

    def delete_item(self, name):
        for item in self.items:
            if item.name == name:
                self.items.remove(item)
                return f"物品 '{name}' 已经被删除."
        return f"未找到物品 '{name}' ."

    def find_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return str(item)
        return f"没有找到名称为 '{item_name}' 的物品."

class User:
    def __init__(self, username, address, contact_info):
        self.username = username
        self.address = address
        self.contact_info = contact_info
        self.is_approved = False


class UserManager:
    def __init__(self):
        self.users = []

    def register_user(self, username, address, contact_info):
        if any(user.username == username for user in self.users):
            return f"用户 '{username}' 已经存在."
        user = User(username, address, contact_info)
        self.users.append(user)
        return f"用户 '{username}' 已经被注册并等待被批准."

    def approve_user(self, username):
        for user in self.users:
            if user.username == username:
                user.is_approved = True
                return f"用户 '{username}' 的注册已经被批准."
        return f"未找到用户 '{username}' ."


class GUIApp:
    def __init__(self, root):
        self.revive_items = ReviveItems()
        self.user_manager = UserManager()
        self.root = root
        self.root.title("物品复活系统")

        # Main label
        self.label = tk.Label(root, text="物品复活系统", font=("Microsoft YaHei", 16))
        self.label.pack(pady=10)

        # Role selection buttons
        self.admin_login_button = tk.Button(root, text="以管理员身份登录", command=self.admin_login)
        self.admin_login_button.pack(pady=5)

        self.user_login_button = tk.Button(root, text="以普通用户身份登录", command=self.user_login)
        self.user_login_button.pack(pady=5)

        self.register_user_button = tk.Button(root, text="注册普通用户", command=self.register_user)
        self.register_user_button.pack(pady=5)

        # Output text box
        self.output_text = tk.Text(root, width=60, height=20)
        self.output_text.pack(pady=10)

    def admin_login(self):
        password = simpledialog.askstring("管理员登录", "请输入管理员密码:", show="*")
        if password == "12345":
            self.admin_panel()
        else:
            messagebox.showerror("错误", "密码错误！")

    def user_login(self):
        username = simpledialog.askstring("用户登录", "请输入用户名:")
        for user in self.user_manager.users:
            if user.username == username and user.is_approved:
                self.user_panel(username)
                return
        messagebox.showerror("错误", "用户未注册或未被批准！")

    def register_user(self):
        username = simpledialog.askstring("用户注册", "请输入用户名:")
        if username:
            address = simpledialog.askstring("用户注册", "请输入住址:")
            contact_info = simpledialog.askstring("用户注册", "请输入联系信息:")
            result = self.user_manager.register_user(username, address, contact_info)
            self.output_text.insert(tk.END, result + "\n")

    def admin_panel(self):
        def add_item_type():
            type_name = simpledialog.askstring("添加物品类型", "请输入物品类型名:")
            if type_name:
                attrs_input = simpledialog.askstring("添加物品类型", "请输入属性（用逗号分隔）:")
                attributes_list = attrs_input.split(",") if attrs_input else []
                result = self.revive_items.add_item_type(type_name, attributes_list)
                self.output_text.insert(tk.END, result + "\n")

        def modify_item_type():
            type_name = simpledialog.askstring("修改物品类型", "请输入物品类型名:")
            if type_name:
                attrs_input = simpledialog.askstring("修改物品类型", "请输入属性（用逗号分隔）:")
                attributes_list = attrs_input.split(",") if attrs_input else []
                result = self.revive_items.modify_item_type(type_name, attributes_list)
                self.output_text.insert(tk.END, result + "\n")

        def approve_user():
            username = simpledialog.askstring("批准用户注册", "请输入用户名:")
            if username:
                result = self.user_manager.approve_user(username)
                self.output_text.insert(tk.END, result + "\n")

        panel = tk.Toplevel(self.root)
        panel.title("管理员面板")
        tk.Button(panel, text="添加物品类型", command=add_item_type).pack(pady=5)
        tk.Button(panel, text="修改物品类型", command=modify_item_type).pack(pady=5)
        tk.Button(panel, text="批准用户注册", command=approve_user).pack(pady=5)

    def user_panel(self, username):
        def add_item():
            item_type = simpledialog.askstring("添加物品", "请输入物品类型名:")
            if item_type:
                name = simpledialog.askstring("添加物品", "请输入物品名称:")
                description = simpledialog.askstring("添加物品", "请输入物品说明:")
                address = simpledialog.askstring("添加物品", "请输入物品所在地址:")
                contact_phone = simpledialog.askstring("添加物品", "请输入联系人手机号码:")
                email = simpledialog.askstring("添加物品", "请输入邮箱:")
                additional_attributes = {}
                if item_type in self.revive_items.item_types:
                    for attr in self.revive_items.item_types[item_type].attributes:
                        value = simpledialog.askstring("添加物品", f"请输入 {attr}:")
                        additional_attributes[attr] = value
                result = self.revive_items.add_item(item_type, name, description, address, contact_phone, email, additional_attributes)
                self.output_text.insert(tk.END, result + "\n")

        def find_item():
            item_type = simpledialog.askstring("寻找物品", "请输入物品类型:")
            if item_type:
                item_name = simpledialog.askstring("寻找物品", "请输入物品名称:")
                if item_name:
                    result = self.revive_items.find_item(item_name)
                    self.output_text.insert(tk.END, result + "\n")

        def show_items():
            result = self.revive_items.show_items()
            self.output_text.insert(tk.END, result + "\n")

        def delete_item():
            name = simpledialog.askstring("删除物品", "请输入要删除的物品名称:")
            if name:
                result = self.revive_items.delete_item(name)
                self.output_text.insert(tk.END, result + "\n")


        panel = tk.Toplevel(self.root)
        panel.title(f"用户面板 - {username}")
        tk.Button(panel, text="添加物品", command=add_item).pack(pady=5)
        tk.Button(panel, text="寻找物品", command=find_item).pack(pady=5)
        tk.Button(panel, text="显示所有物品", command=show_items).pack(pady=5)
        tk.Button(panel, text="删除物品", command=delete_item).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()
