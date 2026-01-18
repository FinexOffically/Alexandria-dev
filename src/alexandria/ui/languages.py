"""
Multi-language support module for Alexandria.
Supports Russian and English with easy switching.
Default language: Russian (Русский)
"""

from typing import Dict, Optional

# Translation dictionaries
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ru": {  # Russian (Русский) - PRIMARY LANGUAGE
        # ==================== ОСНОВНЫЕ КОМАНДЫ ====================
        "create": "создать",
        "list": "список",
        "view": "показать",
        "edit": "редактировать",
        "delete": "удалить",
        "search": "поиск",
        "category": "категория",
        "tag": "тег",
        "favorite": "избранное",
        "archive": "архив",
        "stats": "статистика",
        "export": "экспорт",
        "import": "импорт",
        "backup": "резервная_копия",
        "restore": "восстановить",
        "language": "язык",
        "clear": "очистить",
        "help": "помощь",
        "exit": "выход",
        "quit": "выход",
        "init": "инициализировать",
        "user": "пользователь",
        "sudo": "sudo",
        "logs": "логи",
        "scan": "сканировать",
        "analyze": "анализировать",
        "find": "найти",
        "grep": "grep",
        "cat": "вывести",
        "head": "начало",
        "tail": "конец",
        "wc": "слова",
        
        # ==================== ОСНОВНЫЕ СООБЩЕНИЯ ====================
        "welcome": "🏛️  Alexandria - Система управления знаниями",
        "banner_title": "Система управления знаниями",
        "prompt": "[{}] ➜",
        "not_logged_in": "не вошли",
        
        # ==================== СОЗДАНИЕ И РЕДАКТИРОВАНИЕ ====================
        "creating_entry": "📝 Создание записи: {}",
        "enter_content": "Введите содержание (введите 'END' в новой строке для завершения):",
        "author_prompt": "Автор (нажмите Enter для 'Неизвестно'):",
        "name_prompt": "Название:",
        "description_prompt": "Описание (опционально, нажмите Enter):",
        "category_prompt": "Категория (нажмите Enter для пропуска):",
        "tags_prompt": "Теги через запятую (нажмите Enter для пропуска):",
        "confirm_delete": "Вы уверены, что хотите удалить эту запись? (да/нет):",
        
        # ==================== СТАТУСНЫЕ СООБЩЕНИЯ ====================
        "entry_created": "✅ Запись создана успешно!",
        "entry_updated": "✅ Запись обновлена!",
        "entry_deleted": "✅ Запись удалена!",
        "entry_not_found": "❌ Запись не найдена!",
        "entry_exists": "❌ Запись с таким ID уже существует!",
        "invalid_id": "❌ Неверный ID записи!",
        "no_entries": "❌ Записей не найдено!",
        "must_be_logged_in": "❌ Необходимо войти в систему!",
        "access_denied": "❌ Доступ запрещен! Требуются права администратора.",
        "operation_cancelled": "⊘ Операция отменена",
        "operation_success": "✅ Операция завершена успешно!",
        
        # ==================== СПИСКИ И ПРОСМОТР ====================
        "all_entries": "📚 ВСЕ ЗАПИСИ",
        "total_entries": "Всего: {} записей",
        "favorites": "⭐ ИЗБРАННЫЕ",
        "archived": "📦 АРХИВНЫЕ",
        "categories": "📂 КАТЕГОРИИ",
        "tags": "🏷️  ТЕГИ",
        "users": "👥 ПОЛЬЗОВАТЕЛИ",
        
        # ==================== ПОИСК И ФИЛЬТРАЦИЯ ====================
        "search_query": "Введите запрос для поиска:",
        "search_results": "🔍 Результаты поиска '{}': {} найдено",
        "no_results": "🔍 Результаты поиска '{}': ничего не найдено",
        "searching": "🔍 Поиск...",
        "advanced_search": "🔎 Продвинутый поиск",
        "regex_pattern": "Введите regex паттерн:",
        "filter_by_category": "Фильтр по категории:",
        "filter_by_tag": "Фильтр по тегу:",
        "filter_by_date": "Фильтр по дате:",
        "sort_by": "Сортировать по:",
        "sort_ascending": "По возрастанию",
        "sort_descending": "По убыванию",
        
        # ==================== ИЗБРАННОЕ И АРХИВ ====================
        "mark_favorite": "⭐ Отмечено как избранное!",
        "unmark_favorite": "☆ Удалено из избранного!",
        "mark_archived": "📦 Архивирована!",
        "unmark_archived": "📂 Восстановлена из архива!",
        "is_favorite": "В избранном",
        "is_archived": "В архиве",
        
        # ==================== КАТЕГОРИИ ====================
        "category_name": "Имя категории:",
        "category_created": "✅ Категория создана!",
        "category_deleted": "✅ Категория удалена!",
        "category_not_found": "❌ Категория не найдена!",
        "category_exists": "❌ Категория уже существует!",
        "select_category": "Выберите категорию (номер):",
        "total_categories": "📂 Всего категорий: {}",
        
        # ==================== ТЕГИ ====================
        "tag_name": "Имя тега:",
        "tag_created": "✅ Тег создан!",
        "tag_deleted": "✅ Тег удален!",
        "tag_added": "✅ Тег добавлен к записи!",
        "tag_removed": "✅ Тег удален из записи!",
        "tag_not_found": "❌ Тег не найден!",
        "tag_exists": "❌ Тег уже существует!",
        "select_tag": "Выберите тег (номер):",
        "total_tags": "🏷️  Всего тегов: {}",
        
        # ==================== СТАТИСТИКА ====================
        "stats_title": "📊 СТАТИСТИКА БИБЛИОТЕКИ",
        "total_categories": "📂 Всего категорий: {}",
        "total_tags": "🏷️  Всего тегов: {}",
        "total_favorites": "⭐ Всего избранных: {}",
        "total_archived": "📦 Всего архивных: {}",
        "database_size": "💾 Размер БД: {}",
        "last_updated": "🕐 Последнее обновление: {}",
        
        # ==================== ЭКСПОРТ И ИМПОРТ ====================
        "library_exported": "✅ Библиотека экспортирована в '{}'",
        "library_imported": "✅ Библиотека импортирована из '{}'",
        "export_format": "Выберите формат экспорта (json/csv/txt):",
        "backup_created": "✅ Резервная копия создана в '{}'",
        "backup_restored": "✅ Резервная копия восстановлена!",
        "select_backup": "Выберите резервную копию:",
        
        # ==================== ПОЛЬЗОВАТЕЛИ И БЕЗОПАСНОСТЬ ====================
        "user_created": "✅ Пользователь создан!",
        "user_deleted": "✅ Пользователь удален!",
        "user_exists": "❌ Пользователь уже существует!",
        "user_not_found": "❌ Пользователь не найден!",
        "password_changed": "✅ Пароль изменен!",
        "wrong_password": "❌ Неверный пароль!",
        "login_failed": "❌ Ошибка входа!",
        "login_success": "✅ Вход успешен!",
        "welcome_message": "✅ Добро пожаловать, {}!",
        "password_prompt": "🔐 Пароль:",
        "username_prompt": "👤 Имя пользователя:",
        "new_password_prompt": "🔑 Новый пароль:",
        "confirm_password_prompt": "🔑 Подтверждение пароля:",
        "passwords_do_not_match": "❌ Пароли не совпадают!",
        "password_too_weak": "⚠️  Пароль слишком слабый!",
        "password_strength": "💪 Сила пароля: {}",
        
        # ==================== ЛОГИРОВАНИЕ ====================
        "logs_title": "📋 ЛОГИ АКТИВНОСТИ",
        "log_entry": "[{}] {} - {} ({})",
        "view_logs": "📖 Просмотр логов",
        "clear_logs": "🗑️  Очистить логи",
        "log_cleared": "✅ Логи очищены!",
        "last_action": "Последнее действие: {}",
        "action_log": "📝 Запись в журнал: {}",
        
        # ==================== СКАНИРОВАНИЕ И АНАЛИЗ ====================
        "scanning": "🔍 Сканирование...",
        "scan_complete": "✅ Сканирование завершено!",
        "vulnerabilities_found": "⚠️  Найдено уязвимостей: {}",
        "no_vulnerabilities": "✅ Уязвимостей не найдено!",
        "vulnerability_score": "🔴 Оценка безопасности: {}%",
        "analyzing": "📊 Анализ...",
        "analysis_complete": "✅ Анализ завершен!",
        "words_found": "📝 Найдено слов: {}",
        "emails_found": "📧 Найдено адресов электронной почты: {}",
        "urls_found": "🔗 Найдено URL: {}",
        "ips_found": "🌐 Найдено IP адресов: {}",
        "api_keys_found": "🔑 Найдено API ключей: {}",
        
        # ==================== УТИЛИТЫ ====================
        "grep_usage": "Используйте: grep <паттерн> [ID]",
        "cat_usage": "Используйте: cat <ID>",
        "head_usage": "Используйте: head <n> или head <n> [ID]",
        "tail_usage": "Используйте: tail <n> или tail <n> [ID]",
        "find_usage": "Используйте: find <паттерн>",
        "no_matches": "❌ Совпадений не найдено!",
        "matches_found": "✅ Найдено совпадений: {}",
        
        # ==================== ЯЗЫКИ ====================
        "languages_available": "🌐 Доступные языки:\n   1. Русский (РУ) - Основной язык\n   2. English (EN)",
        "language_changed": "✅ Язык изменен на {}!",
        "current_language": "📍 Текущий язык: {}",
        "select_language": "Выберите язык (номер):",
        
        # ==================== СПРАВКА ====================
        "help_intro": "📖 СПРАВКА ПО КОМАНДАМ",
        "help_create": "create - Создать новую запись",
        "help_list": "list - Показать список записей",
        "help_view": "view - Показать содержание записи",
        "help_edit": "edit - Отредактировать запись",
        "help_delete": "delete - Удалить запись",
        "help_search": "search - Поиск по записям",
        "help_category": "category - Управление категориями",
        "help_tag": "tag - Управление тегами",
        "help_favorite": "favorite - Отметить как избранное",
        "help_archive": "archive - Архивировать запись",
        "help_stats": "stats - Показать статистику",
        "help_export": "export - Экспортировать библиотеку",
        "help_import": "import - Импортировать библиотеку",
        "help_backup": "backup - Создать резервную копию",
        "help_restore": "restore - Восстановить из резервной копии",
        "help_scan": "scan - Сканировать на уязвимости",
        "help_analyze": "analyze - Анализировать содержание",
        "help_logs": "logs - Просмотреть логи активности",
        "help_user": "user - Управление пользователями",
        "help_sudo": "sudo - Выполнить команду с правами администратора",
        "help_language": "language - Смена языка интерфейса",
        "help_clear": "clear - Очистить экран",
        "help_help": "help - Показать эту справку",
        "help_exit": "exit/quit - Выход из программы",
        
        # ==================== ИНФОРМАЦИЯ ПРИ ВХОДЕ ====================
        "login_user": "👤 Пользователь:",
        "login_role": "🎭 Роль:",
        "login_time": "🕐 Время входа:",
        "login_session": "🔐 Сеанс:",
        "role_admin": "администратор (root)",
        "role_user": "пользователь",
        "system_info": "📊 Информация о системе",
        "system_platform": "🖥️  Платформа:",
        "system_python": "🐍 Python:",
        "system_version": "📦 Версия:",
        "system_ready": "✅ Система готова к работе",
        "database_users": "👥 Всего пользователей:",
        "database_entries": "📚 Всего записей:",
        "database_categories": "📂 Всего категорий:",
        "database_tags": "🏷️  Всего тегов:",
        "logging_directory": "📁 Директория логов:",
        "logging_system": "📋 Системный лог:",
        "logging_access": "🔐 Лог доступа:",
        
        # ==================== ВРЕМЕННАЯ ПОЧТА ====================
        "tempmail_generated": "🔔 Временная почта:",
        "tempmail_help": "Генерирует одноразовый адрес электронной почты",
        "tempmail_usage": "Используйте: tempmail [--name <префикс>] [--save]",
        "tempmail_copied": "✅ Адрес скопирован в буфер обмена!",
        
        # ==================== SSH СОЕДИНЕНИЯ ====================
        "ssh_add": "ssh_add - Добавить SSH соединение",
        "ssh_list": "ssh_list - Список SSH соединений",
        "ssh_test": "ssh_test - Проверить SSH соединение",
        "ssh_info": "ssh_info - Информация о SSH соединении",
        "ssh_delete": "ssh_delete - Удалить SSH соединение",
        "ssh_connection_added": "SSH соединение '{}' успешно добавлено",
        "ssh_connection_deleted": "SSH соединение '{}' успешно удалено",
        "ssh_connection_not_found": "SSH соединение '{}' не найдено",
        "ssh_no_connections": "Нет сохраненных SSH соединений",
        "ssh_connections_list": "📋 SSH Соединения",
        "ssh_connection_info": "🔒 SSH Соединение: {}",
        "ssh_test_success": "✅ Соединение с {} успешно",
        "ssh_test_failed": "❌ Ошибка соединения: {}",
        "ssh_auth_failed": "❌ Ошибка аутентификации",
        "ssh_auth_type": "Тип аутентификации:",
        "ssh_host": "Хост:",
        "ssh_port": "Порт:",
        "ssh_user": "Пользователь:",
        "ssh_key_path": "Путь к ключу:",
        "ssh_created": "Создано:",
        "ssh_last_used": "Последнее использование:",
        "ssh_password_prompt": "Введите пароль для {}@{}: ",
        "ssh_confirm_delete": "Вы уверены, что хотите удалить SSH соединение '{}'? (да/нет): ",
        "ssh_cancelled": "Отменено",
        "tempmail_error": "❌ Ошибка при копировании в буфер обмена",
        
        # ==================== ОШИБКИ И ИСКЛЮЧЕНИЯ ====================
        "error": "❌ Ошибка: {}",
        "error_occurred": "❌ Произошла ошибка: {}",
        "invalid_command": "❌ Неизвестная команда. Введите 'help' для справки.",
        "invalid_input": "❌ Неверный ввод!",
        "invalid_option": "❌ Неверная опция!",
        "file_not_found": "❌ Файл не найден!",
        "file_error": "❌ Ошибка при работе с файлом: {}",
        "database_error": "❌ Ошибка базы данных: {}",
        "connection_error": "❌ Ошибка подключения!",
        
        # ==================== ВЫХОД ====================
        "farewell": "✨ До встречи в Alexandria...",
        "goodbye": "🎭 Спасибо за использование Alexandria!",
        "saving": "💾 Сохранение...",
        "saved": "✅ Сохранено!",
        
        # ==================== ПРОЧЕЕ ====================
        "select_entry": "Выберите запись (номер):",
        "select_option": "Выберите опцию (номер):",
        "enter_value": "Введите значение:",
        "yes": "да",
        "no": "нет",
        "confirm": "Подтвердить (да/нет):",
        "loading": "⏳ Загрузка...",
        "processing": "⚙️  Обработка...",
        "done": "✅ Готово!",
        "skipped": "⊘ Пропущено",
        "warning": "⚠️  Предупреждение: {}",
        "info": "ℹ️  Информация: {}",
    },
    "en": {  # English (English)
        # Commands
        "create": "create",
        "list": "list",
        "view": "view",
        "edit": "edit",
        "delete": "delete",
        "search": "search",
        "category": "category",
        "tag": "tag",
        "favorite": "favorite",
        "archive": "archive",
        "stats": "stats",
        "export": "export",
        "language": "language",
        "clear": "clear",
        "help": "help",
        "exit": "exit",
        
        # Messages
        "welcome": "🏛️  Alexandria - Knowledge Management System",
        "prompt": "[Alexandria] ➜",
        "creating_entry": "📝 Creating entry: {}",
        "enter_content": "Enter content (type 'END' on a new line to finish):",
        "author_prompt": "Author (press Enter for 'Unknown'):",
        "entry_created": "✅ Entry created successfully!",
        "entry_not_found": "❌ Entry not found!",
        "entry_deleted": "✅ Entry deleted!",
        "entry_updated": "✅ Entry updated!",
        "all_entries": "📚 ALL ENTRIES",
        "total_entries": "Total: {} entries",
        "favorites": "⭐ FAVORITES",
        "archived": "📦 ARCHIVED",
        "search_results": "🔍 Search results for '{}': {} found",
        "no_results": "🔍 Search results for '{}': nothing found",
        "search_query": "Enter search query:",
        "mark_favorite": "⭐ Marked as favorite!",
        "unmark_favorite": "☆ Removed from favorites!",
        "mark_archived": "📦 Archived!",
        "unmark_archived": "📂 Restored from archive!",
        "category_created": "✅ Category created!",
        "category_deleted": "✅ Category deleted!",
        "tag_created": "✅ Tag created!",
        "tag_deleted": "✅ Tag deleted!",
        "tag_added": "✅ Tag added to entry!",
        "tag_removed": "✅ Tag removed from entry!",
        "library_exported": "✅ Library exported to '{}'",
        "stats_title": "📊 LIBRARY STATISTICS",
        "total_categories": "📂 Total categories: {}",
        "total_tags": "🏷️  Total tags: {}",
        "total_favorites": "⭐ Total favorites: {}",
        "total_archived": "📦 Total archived: {}",
        "languages_available": "🌐 Available languages:\n   1. Русский (RU)\n   2. English (EN)",
        "language_changed": "✅ Language changed to {}!",
        "farewell": "✨ Farewell from Alexandria...",
        "error": "❌ Error: {}",
        "invalid_command": "❌ Unknown command. Type 'help' for assistance.",
        "invalid_id": "❌ Invalid entry ID!",
        "name_prompt": "Name:",
        "description_prompt": "Description (optional, press Enter):",
        "category_name": "Category name:",
        "tag_name": "Tag name:",
        "select_category": "Select category (number):",
        "select_tag": "Select tag (number):",
        "select_entry": "Select entry (number):",
        "help_intro": "📖 COMMAND REFERENCE",
        "help_create": "create - Create a new entry",
        "help_list": "list - List entries",
        "help_view": "view - View entry content",
        "help_edit": "edit - Edit entry",
        "help_delete": "delete - Delete entry",
        "help_search": "search - Search entries",
        "help_category": "category - Manage categories",
        "help_tag": "tag - Manage tags",
        "help_favorite": "favorite - Mark as favorite",
        "help_archive": "archive - Archive entry",
        "help_stats": "stats - Show statistics",
        "help_export": "export - Export library",
        "help_language": "language - Change language",
        "help_clear": "clear - Clear screen",
        "help_help": "help - Show this help",
        "help_exit": "exit - Exit application",
        "banner_title": "Knowledge & Information Management System",
        
        # New features
        "login_user": "User:",
        "login_role": "Role:",
        "login_time": "Login time:",
        "login_session": "Session:",
        "role_admin": "administrator (root)",
        "role_user": "user",
        "system_info": "📊 System Information",
        "system_platform": "Platform:",
        "system_python": "Python:",
        "system_version": "Version:",
        "database_users": "Total users:",
        "database_entries": "Total entries:",
        "logging_directory": "Log directory:",
        "logging_system": "System log:",
        "logging_access": "Access log:",
        "tempmail_generated": "🔔 Temporary email:",
        "tempmail_help": "Generates a disposable email address",
        
        # SSH Connections
        "ssh_add": "ssh_add - Add SSH connection",
        "ssh_list": "ssh_list - List SSH connections",
        "ssh_test": "ssh_test - Test SSH connection",
        "ssh_info": "ssh_info - Show SSH connection info",
        "ssh_delete": "ssh_delete - Delete SSH connection",
        "ssh_connection_added": "SSH connection '{}' added successfully",
        "ssh_connection_deleted": "SSH connection '{}' deleted successfully",
        "ssh_connection_not_found": "SSH connection '{}' not found",
        "ssh_no_connections": "No SSH connections saved",
        "ssh_connections_list": "📋 SSH Connections",
        "ssh_connection_info": "🔒 SSH Connection: {}",
        "ssh_test_success": "✅ Connection to {} successful",
        "ssh_test_failed": "❌ Connection error: {}",
        "ssh_auth_failed": "❌ Authentication failed",
        "ssh_auth_type": "Auth type:",
        "ssh_host": "Host:",
        "ssh_port": "Port:",
        "ssh_user": "User:",
        "ssh_key_path": "Key path:",
        "ssh_created": "Created:",
        "ssh_last_used": "Last used:",
        "ssh_password_prompt": "Enter password for {}@{}: ",
        "ssh_confirm_delete": "Are you sure you want to delete SSH connection '{}'? (yes/no): ",
        "ssh_cancelled": "Cancelled",
    }
}

class LanguageManager:
    """Manages language selection and translations."""
    
    def __init__(self, default_language: str = "ru"):
        """
        Initialize language manager.
        
        Args:
            default_language: Default language code ('en' or 'ru') - Default is 'ru' (Russian)
        """
        self.current_language = default_language if default_language in TRANSLATIONS else "ru"
    
    def get_text(self, key: str, *args) -> str:
        """
        Get translated text.
        
        Args:
            key: Translation key
            *args: Format arguments
            
        Returns:
            Translated text
        """
        translations = TRANSLATIONS.get(self.current_language, TRANSLATIONS["ru"])
        text = translations.get(key, key)
        
        # Format with arguments if provided
        if args:
            try:
                return text.format(*args)
            except (IndexError, KeyError):
                return text
        return text
    
    def set_language(self, language_code: str) -> bool:
        """
        Set current language.
        
        Args:
            language_code: Language code ('en' or 'ru')
            
        Returns:
            True if successful
        """
        if language_code in TRANSLATIONS:
            self.current_language = language_code
            return True
        return False
    
    def get_language_name(self) -> str:
        """Get current language name."""
        names = {
            "en": "English",
            "ru": "Русский"
        }
        return names.get(self.current_language, "Unknown")
    
    def list_languages(self) -> str:
        """Get list of available languages."""
        return self.get_text("languages_available")
    
    def _(self, key: str, *args) -> str:
        """Shorthand for get_text()."""
        return self.get_text(key, *args)


# Global language manager instance
_language_manager: Optional[LanguageManager] = None

def get_language_manager() -> LanguageManager:
    """Get or create global language manager."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager("ru")  # Default to Russian
    return _language_manager

def set_default_language(language_code: str):
    """Set default language for the application."""
    get_language_manager().set_language(language_code)

def _(key: str, *args) -> str:
    """Quick translation function."""
    return get_language_manager().get_text(key, *args)
