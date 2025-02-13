import curses
import json
from datetime import datetime
from all import IntegratedSystem
import threading

class ChatTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.system = IntegratedSystem()
        self.chat_history = []
        self.input_buffer = []
        self.cursor_x = 0
        self.scroll_position = 0
        self.is_processing = False

        # Initialize basic colors if terminal supports
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # User message
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)  # AI message

        # Get terminal size
        self.height, self.width = self.stdscr.getmaxyx()

        # Create windows
        self.create_windows()

        # Initialize cursor and keypad
        # curses.curs_set(1)
        self.stdscr.keypad(1)

    def create_windows(self):
        # Chat window (3/4 of screen height)
        chat_height = int(self.height * 0.75)
        self.chat_win = curses.newwin(chat_height, self.width, 0, 0)
        self.chat_win.scrollok(True)

        # Input window (1/4 of screen height)
        input_height = self.height - chat_height - 1
        self.input_win = curses.newwin(input_height, self.width, chat_height, 0)
        self.input_win.scrollok(True)

        # Status bar (1 line at the bottom)
        self.status_win = curses.newwin(1, self.width, self.height - 1, 0)

    def run(self):
        self.update_status("Chatbot | Enter: Send | F5: Save Chat | F8: Clear Chat | Ctrl+C: Quit")
        self.refresh_all()

        while True:
            try:
                ch = self.input_win.getch()
                if ch == ord('\n'):  # Enter pressed
                    self.send_message()
                elif ch == curses.KEY_F5:  # F5: Save chat
                    self.save_chat()
                elif ch == curses.KEY_F8:  # F8: Clear chat
                    self.clear_chat()
                elif ch == curses.KEY_BACKSPACE or ch == 127:  # Backspace
                    if self.input_buffer and self.cursor_x > 0:
                        self.input_buffer.pop(self.cursor_x - 1)
                        self.cursor_x -= 1
                elif ch == curses.KEY_LEFT and self.cursor_x > 0:
                    self.cursor_x -= 1
                elif ch == curses.KEY_RIGHT and self.cursor_x < len(self.input_buffer):
                    self.cursor_x += 1
                elif 32 <= ch <= 126 or ch > 128:  # Printable characters
                    self.input_buffer.insert(self.cursor_x, chr(ch))
                    self.cursor_x += 1

                self.refresh_input()

            except KeyboardInterrupt:
                break

    def send_message(self):
        if not self.input_buffer or self.is_processing:
            return

        message = ''.join(self.input_buffer)
        self.input_buffer.clear()
        self.cursor_x = 0

        # Add user message to chat history
        self.add_message("User", message)

        # Set processing flag
        self.is_processing = True
        self.update_status("Processing... Please wait.")
        self.refresh_all()

        # Get AI response in a separate thread
        threading.Thread(target=self.get_ai_response, args=(message,), daemon=True).start()

    def get_ai_response(self, query):
        try:
            response = self.system.process_user_query(query)
            self.add_message("AI", response)
        except Exception as e:
            self.add_message("Error", f"Error: {str(e)}")
        finally:
            self.is_processing = False
            self.update_status("Chatbot | Enter: Send | F5: Save Chat | F8: Clear Chat | Ctrl+C: Quit")
            self.refresh_all()

    def add_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message
        })

        # Add message to chat window
        self.chat_win.addstr(f"[{timestamp}] ", curses.A_DIM)
        if sender == "User":
            self.chat_win.addstr(f"{sender}: ", curses.color_pair(1))
        else:
            self.chat_win.addstr(f"{sender}: ", curses.color_pair(2))
        self.chat_win.addstr(f"{message}\n\n")
        self.chat_win.refresh()

    def save_chat(self):
        filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
            self.update_status(f"Chat saved to {filename}")
        except Exception as e:
            self.update_status(f"Save failed: {str(e)}")
        self.refresh_all()

    def clear_chat(self):
        self.chat_history.clear()
        self.chat_win.clear()
        self.update_status("Chat cleared.")
        self.refresh_all()

    def update_status(self, message):
        self.status_win.clear()
        self.status_win.addstr(0, 0, message)
        self.status_win.refresh()

    def refresh_input(self):
        self.input_win.clear()
        current_input = ''.join(self.input_buffer)
        self.input_win.addstr(0, 0, current_input)
        self.input_win.move(0, self.cursor_x)
        self.input_win.refresh()

    def refresh_all(self):
        self.chat_win.refresh()
        self.refresh_input()
        self.status_win.refresh()

def main():
    def run_interface(stdscr):
        chat_tui = ChatTUI(stdscr)
        chat_tui.run()

    curses.wrapper(run_interface)

if __name__ == "__main__":
    main()
