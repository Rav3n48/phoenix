import json
import os


class ThemeManager:
    def __init__(self):
        self.current_theme_data = None

    def load_theme(self, app, theme_name):
        path = os.path.join("themes", f"{theme_name}.json")

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as theme_file:
                    self.current_theme_data = json.load(theme_file)
            except:
                self.current_theme_data = None
        else:
            self.current_theme_data = None

        self.apply_theme(app)

    def apply_theme(self, app):
        if self.current_theme_data:
            qss_path = os.path.join("assets", "styles.qss")
            if os.path.exists(qss_path):
                try:
                    with open(qss_path, "r", encoding="utf-8") as styles_file:
                        qss_content = styles_file.read()

                    colors = self.current_theme_data["colors"]
                    for key, value in colors.items():
                        placeholder = "{" + key + "}"
                        qss_content = qss_content.replace(placeholder, value)

                    app.setStyleSheet(qss_content)

                except:
                    return
        else:
            return
