import tkinter as tk
from tkinter import scrolledtext
import datetime
import os
import all

class ChatGUI:
    def __init__(self, root, integrated_system):
        """
        初始化图形化界面
        Args:
            root: Tkinter 根窗口
            integrated_system: 集成的查询和对话系统
        """
        self.root = root
        self.integrated_system = integrated_system
        self.setup_ui()

        # 创建日志文件
        self.log_file = self.create_log_file()

    def setup_ui(self):
        """设置图形化界面布局"""
        self.root.title("DeepSeek 故障诊断助手")
        self.root.geometry("800x600")

        # 输入框
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.input_label = tk.Label(self.input_frame, text="请输入查询内容:")
        self.input_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, width=70)
        self.input_entry.pack(side=tk.LEFT, padx=10)
        self.input_entry.bind("<Return>", self.process_input)  # 绑定回车键

        self.submit_button = tk.Button(self.input_frame, text="提交", command=self.process_input)
        self.submit_button.pack(side=tk.LEFT)

        # 输出框
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.output_label = tk.Label(self.output_frame, text="对话记录:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # 清空按钮
        self.clear_button = tk.Button(self.root, text="清空对话", command=self.clear_output)
        self.clear_button.pack(pady=10)

    def process_input(self, event=None):
        """处理用户输入"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        # 显示用户输入
        self.output_text.insert(tk.END, f"用户: {user_input}\n")
        self.output_text.insert(tk.END, "-" * 50 + "\n")

        # 调用集成系统处理查询
        response = self.integrated_system.process_user_query(user_input)

        # 显示系统回复
        self.output_text.insert(tk.END, f"助手: {response}\n")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")

        # 保存对话到日志文件
        self.save_to_log(user_input, response)

        # 清空输入框
        self.input_entry.delete(0, tk.END)

    def clear_output(self):
        """清空输出框"""
        self.output_text.delete(1.0, tk.END)

    def create_log_file(self):
        """创建日志文件"""
        log_dir = "chat_logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"chat_log_{timestamp}.txt")
        return log_file

    def save_to_log(self, user_input, response):
        """保存对话到日志文件"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"用户: {user_input}\n")
            f.write(f"助手: {response}\n")
            f.write("=" * 50 + "\n\n")


def main():
    # 初始化集成系统
    integrated_system = all.IntegratedSystem()

    # 创建图形化界面
    root = tk.Tk()
    chat_gui = ChatGUI(root, integrated_system)
    root.mainloop()


if __name__ == "__main__":
    main()