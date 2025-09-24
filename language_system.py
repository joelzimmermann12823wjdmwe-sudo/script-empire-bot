# language_system.py
class LanguageSystem:
    def __init__(self):
        self.user_preferences = {}
        self.server_preferences = {}
        self.command_templates = {}
    
    def register_command_template(self, command_key: str, template: dict):
        """Registriert eine Vorlage für einen neuen Command"""
        self.command_templates[command_key] = template
    
    def get_command_text(self, command_key: str, text_type: str, user_id: int = None, guild_id: int = None):
        """Holt Text für einen Command - automatisch für neue Commands"""
        language = self.get_user_language(user_id, guild_id)
        
        # Wenn Template existiert, verwende es
        if command_key in self.command_templates:
            template = self.command_templates[command_key]
            if language in template and text_type in template[language]:
                return template[language][text_type]
        
        # Fallback zu Standard-Texten
        return self.get_text(text_type, user_id, guild_id)
    
    def get_text(self, key: str, user_id: int = None, guild_id: int = None, **kwargs) -> str:
        language = self.get_user_language(user_id, guild_id)
        text = TEXTS[language].get(key, TEXTS["en"].get(key, f"[{key}]"))
        
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        return text
    
    def get_user_language(self, user_id: int = None, guild_id: int = None) -> str:
        if user_id and user_id in self.user_preferences:
            return self.user_preferences[user_id]
        if guild_id and guild_id in self.server_preferences:
            return self.server_preferences[guild_id]
        return "en"
    
    def set_user_language(self, user_id: int, language: str):
        if language in ["de", "en"]:
            self.user_preferences[user_id] = language
            return True
        return False

# AUTOMATISCHE COMMAND-TEMPLATES
COMMAND_TEMPLATES = {
    # Template für HELP-ähnliche Commands
    "help_style": {
        "en": {
            "name": "{command}",
            "description": "Show {topic} information",
            "title": "📋 {topic}",
            "description_text": "Information about {topic}",
            "list_title": "Available {topic}",
            "item_format": "• {item}",
            "footer": "Use /help for more commands"
        },
        "de": {
            "name": "{command}",
            "description": "Zeige {topic} Informationen",
            "title": "📋 {topic}",
            "description_text": "Informationen über {topic}",
            "list_title": "Verfügbare {topic}",
            "item_format": "• {item}",
            "footer": "Verwende /hilfe für mehr Commands"
        }
    },
    
    # Template für INFO-ähnliche Commands
    "info_style": {
        "en": {
            "name": "{command}",
            "description": "Get information about {topic}",
            "title": "ℹ️ {topic} Information",
            "statistics": "{topic} Statistics",
            "details": "{topic} Details",
            "status": "{topic} Status"
        },
        "de": {
            "name": "{command}",
            "description": "Erhalte Informationen über {topic}",
            "title": "ℹ️ {topic} Informationen",
            "statistics": "{topic} Statistiken",
            "details": "{topic} Details",
            "status": "{topic} Status"
        }
    },
    
    # Template für ADMIN-ähnliche Commands
    "admin_style": {
        "en": {
            "name": "{command}",
            "description": "Admin command for {function}",
            "title": "⚡ Admin: {function}",
            "success": "{function} completed successfully",
            "error": "Error during {function}"
        },
        "de": {
            "name": "{command}",
            "description": "Admin Command für {function}",
            "title": "⚡ Admin: {function}",
            "success": "{function} erfolgreich abgeschlossen",
            "error": "Fehler bei {function}"
        }
    }
}

# BASIS-TEXTE FÜR ALLES
TEXTS = {
    "en": {
        # ... deine bestehenden englischen Texte ...
        "new_command": "New Command",
        "topic": "topic",
        "function": "function",
        "item": "item"
    },
    "de": {
        # ... deine bestehenden deutschen Texte ...
        "new_command": "Neuer Command",
        "topic": "Thema",
        "function": "Funktion", 
        "item": "Eintrag"
    }
}

language_system = LanguageSystem()

# Templates registrieren
for template_name, template_data in COMMAND_TEMPLATES.items():
    language_system.register_command_template(template_name, template_data)