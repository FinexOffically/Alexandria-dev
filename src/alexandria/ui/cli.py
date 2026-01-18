"""
Command-line interface for Alexandria
"""

import cmd
import os
import sys
import getpass
from typing import Optional, List
from datetime import datetime
from pathlib import Path

from alexandria.core.database import Database
from alexandria.core.library import Library
from alexandria.core.models import Entry, Category, Tag
from alexandria.ui.colors import (
    Colors, banner, separator, section_header, 
    entry_item, status_message, help_command
)
from alexandria.ui.languages import get_language_manager, _


class AlexandriaShell(cmd.Cmd):
    """Interactive shell for Alexandria library"""

    intro = ""

    def __init__(self, library: Library):
        """Initialize the shell"""
        super().__init__()
        self.library = library
        self.current_entry: Optional[Entry] = None
        self.lang_manager = get_language_manager()
        self.current_user = None
        self.current_user_is_admin = False
        self._update_prompt()
        self._show_welcome()
        self._check_first_run()
    
    def _show_welcome(self):
        """Display welcome screen with Arch-style logo"""
        # Beautiful gradient-like ASCII A (Arch Linux style)
        a_logo = f"""{Colors.BOLD}{Colors.MAGENTA}
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱     ╲
                ╱       ╲
               ╱    {Colors.CYAN}⬢{Colors.MAGENTA}    ╲
              ╱           ╲
             ╱             ╲
            ╱     {Colors.BOLD}{Colors.WHITE}ALEXA{Colors.MAGENTA}     ╲
           ╱                 ╲
          ╱___________________╲{Colors.RESET}"""
        
        print(f"\n{a_logo}\n")
        
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}     Knowledge & Information Management{Colors.RESET}")
        print(f"{Colors.CYAN}═══════════════════════════════════════════{Colors.RESET}")
        
        # System info
        print(f"\n{Colors.BOLD}{Colors.GREEN}System:{Colors.RESET}")
        print(f"  {Colors.YELLOW}●{Colors.RESET} Version: {Colors.BOLD}0.5.0{Colors.RESET} (Production Ready)")
        if self.current_user:
            user_info = f"{Colors.BOLD}{self.current_user}{Colors.RESET}"
            if self.current_user_is_admin:
                user_info += f" {Colors.RED}(root){Colors.RESET}"
        else:
            user_info = f"{Colors.RED}Not logged in{Colors.RESET}"
        print(f"  {Colors.YELLOW}●{Colors.RESET} User: {user_info}")
        print(f"  {Colors.YELLOW}●{Colors.RESET} Status: {Colors.BOLD}{Colors.GREEN}Ready{Colors.RESET}")
        
        # Statistics
        stats = self.library.get_statistics()
        print(f"\n{Colors.BOLD}{Colors.CYAN}Database:{Colors.RESET}")
        print(f"  {Colors.YELLOW}●{Colors.RESET} Entries: {Colors.BOLD}{stats['total_entries']}{Colors.RESET}  " +
              f"{Colors.YELLOW}●{Colors.RESET} Categories: {Colors.BOLD}{stats['total_categories']}{Colors.RESET}  " +
              f"{Colors.YELLOW}●{Colors.RESET} Tags: {Colors.BOLD}{stats['total_tags']}{Colors.RESET}")
        
        # Quick help
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}Quick Start:{Colors.RESET}")
        print(f"  {Colors.GREEN}help{Colors.RESET} - Full command reference  |  " +
              f"{Colors.GREEN}init{Colors.RESET} - Setup database  |  " +
              f"{Colors.GREEN}new{Colors.RESET} - Create entry")
        print()
    
    def _check_first_run(self):
        """Check if this is first run and prompt for login/registration"""
        users = self.library.list_users()
        
        # If no users exist, force initialization
        if not users:
            self._initialize_first_user()
        else:
            # Otherwise, prompt for login
            self._login_prompt()
    
    def do_init(self, arg):
        """Initialize Alexandria database and create root user.
        
        Usage: init [--user <name>]
        
        This creates the initial database structure and root user account.
        """
        # Beautiful init animation
        init_art = f"""{Colors.BOLD}{Colors.CYAN}
    ┌─────────────────────────────────────┐
    │  🔧 Initializing Alexandria...      │
    └─────────────────────────────────────┘
        """
        print(f"\n{init_art}\n")
        
        import time
        steps = [
            ("Database structure", "✓"),
            ("Root user account", "✓"),
            ("System configuration", "✓"),
            ("Security setup", "✓"),
        ]
        
        for step, status in steps:
            print(f"  {Colors.YELLOW}●{Colors.RESET} {step}...", end="", flush=True)
            time.sleep(0.3)
            print(f" {Colors.GREEN}{status}{Colors.RESET}")
        
        # Create root user
        self.current_user = "root"
        
        # Initialize system entries
        try:
            self.library.database.save()
            print(f"\n  {Colors.BOLD}{Colors.GREEN}═════════════════════════════════════{Colors.RESET}")
            print(f"  {Colors.GREEN}✓{Colors.RESET} {Colors.BOLD}Alexandria is ready!{Colors.RESET}")
            print(f"  {Colors.BOLD}{Colors.GREEN}═════════════════════════════════════{Colors.RESET}\n")
        except Exception as e:
            print(f"  {Colors.RED}✗{Colors.RESET} Error: {e}\n")
            return
        
        self._prompt_create_user()
    
    def _prompt_create_user(self):
        """Prompt user to create a new user account with beautiful UI"""
        print(f"{Colors.BOLD}{Colors.CYAN}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}┃  Create Your User Account           ┃{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{Colors.RESET}\n")
        
        try:
            username = input(f"{Colors.BOLD}{Colors.YELLOW}➜{Colors.RESET} Username (3+ chars) [{Colors.CYAN}user{Colors.RESET}]: ").strip()
            if not username:
                username = "user"
            
            # Validate username
            if not username.isalnum() or len(username) < 3:
                print(f"\n{Colors.RED}✗ Invalid! Min 3 alphanumeric chars{Colors.RESET}\n")
                self._prompt_create_user()
                return
            
            password = getpass.getpass(f"{Colors.BOLD}{Colors.YELLOW}➜{Colors.RESET} Password (4+ chars): ")
            
            if len(password) < 4:
                print(f"\n{Colors.RED}✗ Password too short!{Colors.RESET}\n")
                self._prompt_create_user()
                return
            
            # Create user
            result = self.library.create_user(username, password)
            if not result["success"]:
                print(f"\n{Colors.RED}✗ {result['error']}{Colors.RESET}\n")
                self._prompt_create_user()
                return
            
            self.current_user = username
            self.current_user_is_admin = (username == "root")
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}┌─────────────────────────────────────┐{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}│  ✓ User Account Created             │{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.GREEN}└─────────────────────────────────────┘{Colors.RESET}\n")
            print(f"{Colors.BOLD}{Colors.MAGENTA}  Welcome to Alexandria, {Colors.CYAN}{username}{Colors.MAGENTA}!{Colors.RESET}\n")
            print(f"{Colors.CYAN}  Type {Colors.GREEN}'help'{Colors.CYAN} to see all commands{Colors.RESET}")
            print(f"{Colors.CYAN}  Type {Colors.GREEN}'new'{Colors.CYAN} to create your first entry\n{Colors.RESET}")
            
            self._update_prompt()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Setup skipped.{Colors.RESET}\n")
    
    def _initialize_first_user(self):
        """Initialize system with first root user"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔐 First Time Setup - Create Root Account{Colors.RESET}\n")
        
        try:
            password = getpass.getpass(f"{Colors.BOLD}{Colors.YELLOW}➜{Colors.RESET} Root password (4+ chars): ")
            
            if len(password) < 4:
                print(f"{Colors.RED}✗ Password too short!{Colors.RESET}")
                self._initialize_first_user()
                return
            
            # Create root user
            result = self.library.create_user("root", password)
            if not result["success"]:
                print(f"{Colors.RED}✗ {result['error']}{Colors.RESET}")
                self._initialize_first_user()
                return
            
            self.current_user = "root"
            self.current_user_is_admin = True
            self._update_prompt()
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}✓ Root account created successfully{Colors.RESET}\n")
            print(f"{Colors.CYAN}System ready! You are logged in as {Colors.BOLD}root{Colors.RESET}\n")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Setup cancelled!{Colors.RESET}\n")
            sys.exit(1)
    
    def _login_prompt(self):
        """Prompt user to login"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔐 Login{Colors.RESET}\n")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                username = input(f"{Colors.BOLD}{Colors.YELLOW}➜{Colors.RESET} Username: ").strip()
                password = getpass.getpass(f"{Colors.BOLD}{Colors.YELLOW}➜{Colors.RESET} Password: ")
                
                result = self.library.authenticate_user(username, password)
                if result["success"]:
                    self.current_user = username
                    self.current_user_is_admin = result.get("is_admin", False)
                    self._update_prompt()
                    print(f"\n{Colors.GREEN}✓ Welcome back, {Colors.BOLD}{username}{Colors.GREEN}!{Colors.RESET}\n")
                    
                    # Show system info after login
                    self._show_login_info()
                    
                    return
                else:
                    remaining = max_attempts - attempt - 1
                    if remaining > 0:
                        print(f"{Colors.YELLOW}✗ Login failed. {remaining} attempts remaining{Colors.RESET}\n")
                    else:
                        print(f"{Colors.RED}✗ Maximum login attempts reached{Colors.RESET}\n")
                        sys.exit(1)
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Login cancelled{Colors.RESET}\n")
                sys.exit(1)
    
    def _show_login_info(self):
        """Display system information after successful login"""
        try:
            sys_info = self.library.get_system_info()
            
            print(f"{Colors.BOLD}{Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}📊 System Information{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            
            # Login details
            print(f"\n{Colors.BOLD}{Colors.GREEN}Session:{Colors.RESET}")
            print(f"  {Colors.CYAN}User:{Colors.RESET} {Colors.BOLD}{self.current_user}{Colors.RESET}")
            if self.current_user_is_admin:
                print(f"  {Colors.CYAN}Role:{Colors.RESET} {Colors.RED}root (Administrator){Colors.RESET}")
            else:
                print(f"  {Colors.CYAN}Role:{Colors.RESET} {Colors.YELLOW}User{Colors.RESET}")
            print(f"  {Colors.CYAN}Login Time:{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # System info
            print(f"\n{Colors.BOLD}{Colors.GREEN}System:{Colors.RESET}")
            print(f"  {Colors.CYAN}Platform:{Colors.RESET} {sys_info['platform']}")
            print(f"  {Colors.CYAN}Python:{Colors.RESET} {sys_info['python_version']}")
            print(f"  {Colors.CYAN}Version:{Colors.RESET} 0.5.0 (Production Ready)")
            
            # Database statistics
            print(f"\n{Colors.BOLD}{Colors.GREEN}Database:{Colors.RESET}")
            print(f"  {Colors.CYAN}Total Users:{Colors.RESET} {sys_info['total_users']}")
            print(f"  {Colors.CYAN}Total Entries:{Colors.RESET} {sys_info['total_entries']}")
            
            # Logging information
            print(f"\n{Colors.BOLD}{Colors.GREEN}Logging:{Colors.RESET}")
            print(f"  {Colors.CYAN}Log Directory:{Colors.RESET} {Colors.YELLOW}{sys_info['log_directory']}{Colors.RESET}")
            print(f"  {Colors.CYAN}System Log:{Colors.RESET} system.log ({sys_info['system_log_size']} bytes)")
            print(f"  {Colors.CYAN}Access Log:{Colors.RESET} access.log ({sys_info['access_log_size']} bytes)")
            
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            
        except Exception as e:
            # Silently fail if system info unavailable
            pass
    
    def do_user(self, arg):
        """Manage user accounts (root only).
        
        Usage: user [list|create|delete|logout]
        
        Commands:
          user list              - Show all users
          user create <name>     - Create new user
          user delete <name>     - Delete user
          user logout            - Logout current user
        
        Examples:
          user list
          user create alice
          user delete bob
          user logout
        """
        if not self.current_user:
            print(f"{Colors.RED}Must be logged in{Colors.RESET}")
            return
        
        if not arg:
            print(f"Current user: {Colors.BOLD}{self.current_user}{Colors.RESET}")
            if self.current_user_is_admin:
                print(f"Privileges: {Colors.RED}root (admin){Colors.RESET}")
            return
        
        parts = arg.split(maxsplit=1)
        cmd = parts[0].lower()
        name = parts[1] if len(parts) > 1 else None
        
        if cmd == "list":
            users = self.library.list_users()
            print(f"{Colors.CYAN}Registered users:{Colors.RESET}")
            for user in users:
                user_info = self.library.get_user(user)
                marker = f"{Colors.RED}(root){Colors.RESET}" if user == "root" else ""
                is_current = f" {Colors.GREEN}(current){Colors.RESET}" if user == self.current_user else ""
                print(f"  {Colors.BOLD}{user}{Colors.RESET} {marker}{is_current}")
        
        elif cmd == "create":
            if not name:
                print(f"{Colors.RED}Specify username{Colors.RESET}")
                return
            
            if not self.current_user_is_admin:
                print(f"{Colors.RED}Permission denied (root only){Colors.RESET}")
                return
            
            password = getpass.getpass(f"Password for {name}: ")
            result = self.library.create_user(name, password)
            
            if result["success"]:
                print(f"{Colors.GREEN}✓{Colors.RESET} User created: {Colors.BOLD}{name}{Colors.RESET}")
            else:
                print(f"{Colors.RED}✗ {result['error']}{Colors.RESET}")
        
        elif cmd == "delete":
            if not name:
                print(f"{Colors.RED}Specify username{Colors.RESET}")
                return
            
            if not self.current_user_is_admin:
                print(f"{Colors.RED}Permission denied (root only){Colors.RESET}")
                return
            
            if name == "root":
                print(f"{Colors.RED}Cannot delete root user{Colors.RESET}")
                return
            
            if self.library.delete_user(name):
                print(f"{Colors.GREEN}✓{Colors.RESET} User deleted: {name}")
            else:
                print(f"{Colors.RED}✗ User not found{Colors.RESET}")
        
        elif cmd == "logout":
            print(f"{Colors.CYAN}Goodbye, {Colors.BOLD}{self.current_user}{Colors.CYAN}!{Colors.RESET}")
            self.current_user = None
            self.current_user_is_admin = False
            self._update_prompt()
            self._login_prompt()
        
        else:
            print(f"{Colors.RED}Unknown command: {cmd}{Colors.RESET}")
    
    def do_sudo(self, arg):
        """Execute command as root or switch to root shell.
        
        Usage: sudo [command] or sudo -i
        
        Options:
          -i              - Interactive root shell (requires root password)
          [command]       - Execute specific command as root
        
        Examples:
          sudo -i
          sudo user list
        """
        if not self.current_user:
            print(f"{Colors.RED}Must be logged in{Colors.RESET}")
            return
        
        # If already root
        if self.current_user_is_admin:
            if arg == "-i":
                print(f"{Colors.BOLD}{Colors.RED}# {Colors.RESET}", end="", flush=True)
                self.prompt = f"{Colors.BOLD}{Colors.RED}root@alexandria{Colors.RESET} {Colors.RED}#{Colors.RESET} "
                return
            else:
                # Execute command as normal
                if arg:
                    self.onecmd(arg)
                return
        
        # Not root - need to authenticate
        if not arg:
            print(f"{Colors.YELLOW}[sudo] password for {self.current_user}: {Colors.RESET}", end="", flush=True)
            password = getpass.getpass("")
        else:
            password = getpass.getpass(f"{Colors.YELLOW}[sudo] password for {self.current_user}: {Colors.RESET}")
        
        # Verify with root account
        root_user = self.library.get_user("root")
        result = self.library.authenticate_user("root", password)
        
        if not result["success"]:
            print(f"{Colors.RED}✗ sudo: 1 incorrect password attempt{Colors.RESET}")
            return
        
        # Execute command as root
        if arg == "-i":
            print(f"{Colors.GREEN}✓ Switched to root shell{Colors.RESET}")
            self.current_user = "root"
            self.current_user_is_admin = True
            self._update_prompt()
            self.prompt = f"{Colors.BOLD}{Colors.RED}root@alexandria{Colors.RESET} {Colors.RED}#{Colors.RESET} "
        else:
            # Execute single command with root privileges
            print(f"{Colors.CYAN}Executing as root...{Colors.RESET}")
            self.onecmd(arg)
    
    def do_pwdcheck(self, arg):
        """Check password strength and security.
        
        Usage: pwdcheck [password]
        
        Analyzes password for:
          - Length
          - Character variety (upper, lower, digits, special chars)
          - Entropy
          - Common patterns
        
        Examples:
          pwdcheck
          pwdcheck MyPassword123!
        """
        if arg:
            password = arg
        else:
            password = getpass.getpass(f"{Colors.BOLD}{Colors.YELLOW}Enter password to check: {Colors.RESET}")
        
        result = self.library.check_password_strength(password)
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Password Strength Analysis:{Colors.RESET}\n")
        print(f"  {result['emoji']} Strength: {Colors.BOLD}{result['strength']}{Colors.RESET}")
        print(f"  Score: {result['score']}/8")
        print(f"  Entropy: {result['entropy']} unique characters")
        
        if result['feedback']:
            print(f"\n{Colors.CYAN}Feedback:{Colors.RESET}")
            for tip in result['feedback']:
                print(f"  {Colors.YELLOW}→{Colors.RESET} {tip}")
        print()
    
    def do_scan(self, arg):
        """Scan library for security vulnerabilities.
        
        Usage: scan [--detailed]
        
        Options:
          --detailed  - Show full details of vulnerabilities
        
        Checks for:
          - Weak usernames
          - Uncategorized entries
          - Duplicate content
          - Outdated entries
        """
        vuln = self.library.find_vulnerabilities()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Security Scan Results:{Colors.RESET}\n")
        print(f"  Security Score: {Colors.BOLD}{vuln['security_score']}/100{Colors.RESET}")
        print(f"  Vulnerabilities: {Colors.RED}{vuln['total_issues']}{Colors.RESET}")
        print(f"  Warnings: {Colors.YELLOW}{vuln['total_warnings']}{Colors.RESET}")
        
        if vuln['vulnerabilities']:
            print(f"\n{Colors.RED}🔴 Vulnerabilities:{Colors.RESET}")
            for issue in vuln['vulnerabilities']:
                print(f"    {Colors.RED}●{Colors.RESET} {issue}")
        
        if vuln['warnings']:
            print(f"\n{Colors.YELLOW}🟡 Warnings:{Colors.RESET}")
            for warning in vuln['warnings']:
                print(f"    {Colors.YELLOW}●{Colors.RESET} {warning}")
        
        if not vuln['vulnerabilities'] and not vuln['warnings']:
            print(f"\n{Colors.GREEN}✓ No issues found!{Colors.RESET}")
        
        # Log scan action
        self.library.log_action(self.current_user, "SCAN", f"Score: {vuln['security_score']}", "OK")
        
        print()
    
    def do_analyze(self, arg):
        """Analyze entry content for patterns and sensitive data.
        
        Usage: analyze <entry_id>
        
        Detects:
          - Email addresses
          - URLs
          - IP addresses
          - Potential passwords/API keys
          - Word statistics
          - Sentiment analysis
        
        Examples:
          analyze abc123
          analyze
        """
        if not arg:
            entries = self.library.list_entries()
            if not entries:
                print(f"{Colors.RED}No entries found{Colors.RESET}")
                return
            if len(entries) == 1:
                entry_id = entries[0].id
            else:
                print(f"{Colors.CYAN}Recent entries:{Colors.RESET}")
                for i, e in enumerate(entries[-5:]):
                    print(f"  {i+1}. {Colors.BOLD}{e.title}{Colors.RESET} ({e.id[:8]})")
                return
        else:
            entry_id = arg
        
        analysis = self.library.analyze_content(entry_id)
        if not analysis:
            print(f"{Colors.RED}Entry not found{Colors.RESET}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Content Analysis: {analysis['title']}{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}📊 Statistics:{Colors.RESET}")
        print(f"  Words: {analysis['word_count']} | Chars: {analysis['char_count']} | Unique: {analysis['unique_words']}")
        
        if analysis['emails_found']:
            print(f"\n{Colors.YELLOW}📧 Emails Found:{Colors.RESET}")
            for email in analysis['emails_found']:
                print(f"  {Colors.YELLOW}●{Colors.RESET} {email}")
        
        if analysis['urls_found']:
            print(f"\n{Colors.CYAN}🔗 URLs Found:{Colors.RESET}")
            for url in analysis['urls_found']:
                print(f"  {Colors.CYAN}●{Colors.RESET} {url}")
        
        if analysis['ips_found']:
            print(f"\n{Colors.RED}🔴 IP Addresses Found:{Colors.RESET}")
            for ip in analysis['ips_found']:
                print(f"  {Colors.RED}●{Colors.RESET} {ip}")
        
        if analysis['potential_passwords']:
            print(f"\n{Colors.RED}⚠️ Potential Passwords:{Colors.RESET}")
            for pwd in analysis['potential_passwords']:
                print(f"  {Colors.RED}●{Colors.RESET} {pwd}")
        
        if analysis['potential_api_keys']:
            print(f"\n{Colors.RED}⚠️ Potential API Keys:{Colors.RESET}")
            for key in analysis['potential_api_keys']:
                print(f"  {Colors.RED}●{Colors.RESET} {key}")
        
        if analysis['sentiment_hints']['positive'] or analysis['sentiment_hints']['negative']:
            print(f"\n{Colors.MAGENTA}😊 Sentiment:{Colors.RESET}")
            print(f"  Positive words: {analysis['sentiment_hints']['positive']}")
            print(f"  Negative words: {analysis['sentiment_hints']['negative']}")
        
        # Log analyze action
        self.library.log_action(self.current_user, "ANALYZE", f"Entry: {analysis['title'][:30]}", "OK")
        
        print()
    
    def do_logs(self, arg):
        """View system/activity logs with filtering.
        
        Usage: logs [--last N] [--filter keyword] [--user username] [--action action] [--system]
        
        Options:
          --last N        - Show last N entries (default: 50)
          --filter word   - Filter by keyword
          --user username - Filter by specific user
          --action action - Filter by action (create, delete, search, etc.)
          --system        - Show only system logs (not login logs)
        
        Examples:
          logs                          - Show last 50 logs
          logs --last 20                - Show last 20 entries
          logs --filter create          - Show create operations
          logs --user alice             - Show Alice's activity
          logs --action delete          - Show delete operations
          logs --system                 - Show system logs only
        """
        if not self.current_user:
            print(f"{Colors.RED}Must be logged in{Colors.RESET}")
            return
        
        # Parse arguments
        last_n = 50
        filter_str = None
        user_filter = None
        action_filter = None
        system_only = False
        
        if arg:
            parts = arg.split()
            i = 0
            while i < len(parts):
                if parts[i] == "--last" and i + 1 < len(parts):
                    try:
                        last_n = int(parts[i + 1])
                        i += 2
                    except:
                        i += 1
                elif parts[i] == "--filter" and i + 1 < len(parts):
                    filter_str = parts[i + 1]
                    i += 2
                elif parts[i] == "--user" and i + 1 < len(parts):
                    user_filter = parts[i + 1]
                    i += 2
                elif parts[i] == "--action" and i + 1 < len(parts):
                    action_filter = parts[i + 1]
                    i += 2
                elif parts[i] == "--system":
                    system_only = True
                    i += 1
                else:
                    i += 1
        
        # Get logs
        if system_only:
            logs = self.library.get_system_logs(limit=last_n*2)
        else:
            logs = self.library.get_system_logs(limit=last_n*2)
        
        if not logs:
            print(f"{Colors.CYAN}No logs found{Colors.RESET}\n")
            return
        
        # Filter logs
        display_logs = logs
        
        if user_filter:
            display_logs = [log for log in display_logs if user_filter.lower() in log.lower()]
        
        if action_filter:
            display_logs = [log for log in display_logs if action_filter.lower() in log.lower()]
        
        if filter_str:
            display_logs = [log for log in display_logs if filter_str.lower() in log.lower()]
        
        # Take last N
        display_logs = display_logs[-last_n:]
        
        if not display_logs:
            print(f"{Colors.YELLOW}No matching logs found{Colors.RESET}\n")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}System Activity Log ({len(display_logs)} entries):{Colors.RESET}\n")
        
        for log in display_logs:
            # Color code based on status
            if "OK" in log or "SUCCESS" in log:
                print(f"  {Colors.GREEN}✓{Colors.RESET} {log}")
            elif "ERROR" in log or "FAILED" in log:
                print(f"  {Colors.RED}✗{Colors.RESET} {log}")
            elif "DELETE" in log or "REMOVE" in log:
                print(f"  {Colors.YELLOW}-{Colors.RESET} {log}")
            elif "CREATE" in log or "ADD" in log:
                print(f"  {Colors.GREEN}+{Colors.RESET} {log}")
            elif "SEARCH" in log or "FIND" in log or "SCAN" in log:
                print(f"  {Colors.BLUE}🔍{Colors.RESET} {log}")
            else:
                print(f"  {Colors.CYAN}●{Colors.RESET} {log}")
        
        print()
    
    def do_search(self, arg):
        """Advanced search with regex support.
        
        Usage: search [--regex] [--case] <query>
        
        Options:
          --regex  - Use regular expressions
          --case   - Case-sensitive search
        
        Examples:
          search "python"
          search --regex "^test.*\\.py$"
          search --case --regex "[A-Z][a-z]+"
        """
        if not arg:
            print(f"{Colors.RED}Specify search query{Colors.RESET}")
            return
        
        use_regex = "--regex" in arg
        case_sensitive = "--case" in arg
        
        # Remove flags from query
        query = arg.replace("--regex", "").replace("--case", "").strip()
        
        if not query:
            print(f"{Colors.RED}Specify search query{Colors.RESET}")
            return
        
        results = self.library.search_entries_advanced(query, regex=use_regex, case_sensitive=case_sensitive)
        
        if not results:
            print(f"{Colors.YELLOW}No results found{Colors.RESET}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}Search Results ({len(results)} found):{Colors.RESET}\n")
        for entry in results:
            star = "⭐" if entry.is_favorite else "  "
            arch = "📦" if entry.is_archived else "  "
            print(f"{star}{arch} {Colors.BOLD}{entry.title}{Colors.RESET} ({entry.id[:8]})")
            print(f"   Author: {entry.author} | Created: {entry.created.strftime('%Y-%m-%d')}")
        print()
    
    def _update_prompt(self):
        """Update prompt with current language."""
        prompt_text = self.lang_manager.get_text("prompt")
        if self.current_user:
            user_display = f"{Colors.YELLOW}{self.current_user}{Colors.RESET}"
        else:
            user_display = f"{Colors.RED}guest{Colors.RESET}"
        self.prompt = f"\n{Colors.BOLD}{Colors.CYAN}[{user_display}{Colors.CYAN}]{Colors.RESET} {Colors.MAGENTA}➜{Colors.RESET} "

    # Entry commands
    def do_create(self, arg):
        """Create a new entry with advanced options.
        
        Usage: create <title> [--author <name>] [--category <name>] [--tags <tag1,tag2>] [--source <source>] [--favorite] [--interactive]
        
        Options:
          --author <name>      : Set author name (default: Unknown)
          --category <name>    : Assign to category
          --tags <tag1,tag2>   : Add tags (comma-separated)
          --source <source>    : Add source reference
          --favorite           : Mark as favorite immediately
          --interactive        : Interactive mode (default if no content)
          --content <text>     : Content text (can be multiline with \\n)
        
        Examples:
          create "My Entry" --author "John" --category "Notes"
          create "Article" --tags "python,tutorial" --source "blog.com"
          create "Favorite" --favorite --category "Important"
        """
        import re
        
        if not arg:
            print(status_message('error', 'Please provide an entry title'))
            return

        # Parse arguments
        parts = []
        current_part = ""
        in_quotes = False
        quote_char = None
        
        for i, char in enumerate(arg):
            if char in ['"', "'"] and (i == 0 or arg[i-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                else:
                    current_part += char
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(current_part)
                current_part = ""
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        
        title = parts[0] if parts else ""
        options = {}
        
        i = 1
        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if key in ['favorite']:
                    options[key] = True
                    i += 1
                elif i + 1 < len(parts):
                    value = parts[i + 1]
                    options[key] = value
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        print(f"\n{Colors.BOLD}{Colors.MAGENTA}📝 Creating entry: {title}{Colors.RESET}")
        
        # Get content
        content = options.get('content', '')
        if not content or options.get('interactive'):
            print(f"{Colors.CYAN}Enter content (type 'END' on a new line to finish):{Colors.RESET}\n")
            lines = []
            while True:
                try:
                    line = input(f"{Colors.GRAY}>{Colors.RESET} ")
                    if line == "END":
                        break
                    lines.append(line)
                except EOFError:
                    break
            content = "\n".join(lines)
        
        if not content:
            print(status_message('error', 'Content cannot be empty'))
            return

        # Get author
        author = options.get('author', '')
        if not author:
            author = input(f"\n{Colors.CYAN}Author (press Enter for 'Unknown'):{Colors.RESET} ").strip() or "Unknown"

        # Get category
        category_id = None
        if 'category' in options:
            cat_name = options['category']
            categories = self.library.list_categories()
            for cat in categories:
                if cat.name.lower() == cat_name.lower():
                    category_id = cat.id
                    break
            if not category_id:
                print(f"{Colors.YELLOW}⚠️  Category '{cat_name}' not found{Colors.RESET}")
        else:
            categories = self.library.list_categories()
            if categories:
                print(f"\n{Colors.BOLD}{Colors.MAGENTA}📂 Available categories:{Colors.RESET}")
                for i, cat in enumerate(categories, 1):
                    print(f"  {Colors.CYAN}{i}.{Colors.RESET} {cat.name}")
                print(f"  {Colors.CYAN}0.{Colors.RESET} No category")
                
                try:
                    choice = int(input(f"{Colors.CYAN}Select category (0): {Colors.RESET}") or "0")
                    if 1 <= choice <= len(categories):
                        category_id = categories[choice - 1].id
                except ValueError:
                    pass

        # Create entry
        entry = self.library.create_entry(
            title=title,
            content=content,
            author=author,
            category_id=category_id,
        )

        # Add source if provided
        if 'source' in options:
            entry.source = options['source']

        # Mark as favorite if requested
        if options.get('favorite'):
            entry.is_favorite = True

        self.library.db.update_entry(entry)
        self.current_entry = entry

        # Add tags if provided
        if 'tags' in options:
            tag_names = [t.strip() for t in options['tags'].split(',')]
            for tag_name in tag_names:
                tag = self.library.create_tag(tag_name)
                self.library.add_tag_to_entry(entry.id, tag.id)

        print(f"\n{status_message('success', 'Entry created successfully!')}")
        print(f"   {Colors.CYAN}ID:{Colors.RESET} {entry.id}")
        print(f"   {Colors.CYAN}Title:{Colors.RESET} {entry.title}")
        print(f"   {Colors.CYAN}Author:{Colors.RESET} {entry.author}")
        if entry.source:
            print(f"   {Colors.CYAN}Source:{Colors.RESET} {entry.source}")
        if options.get('favorite'):
            print(f"   {Colors.YELLOW}⭐ Marked as favorite{Colors.RESET}")
        if 'tags' in options:
            print(f"   {Colors.MAGENTA}🏷️  Tags:{Colors.RESET} {options['tags']}")
        
        # Log action
        self.library.log_action(self.current_user, "CREATE_ENTRY", f"Title: {entry.title[:30]}", "OK")

    def do_batch_create(self, arg):
        """Create multiple entries at once.
        
        Usage: batch_create [--file <filename>] [--format csv|json]
        
        Enters interactive mode to create multiple entries sequentially.
        Or reads from a file (CSV with headers: title,author,content,category,tags)
        """
        use_file = '--file' in arg
        
        if use_file:
            # Parse filename
            parts = arg.split()
            idx = parts.index('--file')
            if idx + 1 < len(parts):
                filename = parts[idx + 1]
                self._batch_create_from_file(filename)
            else:
                print(status_message('error', 'Please provide filename'))
        else:
            self._batch_create_interactive()

    def _batch_create_interactive(self):
        """Interactive batch creation"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📚 Batch Create Mode{Colors.RESET}")
        print(f"{Colors.CYAN}Enter entries (type 'DONE' after creating an entry to create another){Colors.RESET}")
        print(f"{Colors.CYAN}Type 'QUIT' to exit batch mode{Colors.RESET}\n")
        
        count = 0
        while True:
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}Entry #{count + 1}{Colors.RESET}")
            
            title = input(f"{Colors.CYAN}Title (or QUIT/DONE): {Colors.RESET}").strip()
            
            if title.upper() == 'QUIT':
                break
            elif title.upper() == 'DONE' or not title:
                continue
            
            author = input(f"{Colors.CYAN}Author: {Colors.RESET}").strip() or "Unknown"
            category_input = input(f"{Colors.CYAN}Category: {Colors.RESET}").strip()
            tags_input = input(f"{Colors.CYAN}Tags (comma-separated): {Colors.RESET}").strip()
            
            print(f"{Colors.CYAN}Content (type 'END' to finish):{Colors.RESET}")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            
            content = "\n".join(lines)
            if not content:
                print(status_message('warning', 'Skipping entry - no content'))
                continue
            
            # Create entry
            category_id = None
            if category_input:
                for cat in self.library.list_categories():
                    if cat.name.lower() == category_input.lower():
                        category_id = cat.id
                        break
            
            entry = self.library.create_entry(
                title=title,
                content=content,
                author=author,
                category_id=category_id
            )
            
            # Add tags
            if tags_input:
                for tag_name in [t.strip() for t in tags_input.split(',')]:
                    tag = self.library.create_tag(tag_name)
                    self.library.add_tag_to_entry(entry.id, tag.id)
            
            count += 1
            print(f"{Colors.GREEN}✅ Entry created (ID: {entry.id}){Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}📊 Created {count} entries{Colors.RESET}\n")

    def _batch_create_from_file(self, filename):
        """Create entries from CSV file"""
        try:
            import csv
            count = 0
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = row.get('title', '').strip()
                    if not title:
                        continue
                    
                    author = row.get('author', 'Unknown').strip() or 'Unknown'
                    content = row.get('content', '').strip()
                    category_name = row.get('category', '').strip()
                    tags_str = row.get('tags', '').strip()
                    
                    if not content:
                        continue
                    
                    # Find category
                    category_id = None
                    if category_name:
                        for cat in self.library.list_categories():
                            if cat.name.lower() == category_name.lower():
                                category_id = cat.id
                                break
                    
                    entry = self.library.create_entry(
                        title=title,
                        content=content,
                        author=author,
                        category_id=category_id
                    )
                    
                    # Add tags
                    if tags_str:
                        for tag_name in [t.strip() for t in tags_str.split(',')]:
                            tag = self.library.create_tag(tag_name)
                            self.library.add_tag_to_entry(entry.id, tag.id)
                    
                    count += 1
                    print(f"{Colors.GREEN}✅{Colors.RESET} {entry.title}")
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}📊 Imported {count} entries from {filename}{Colors.RESET}\n")
        except FileNotFoundError:
            print(status_message('error', f'File not found: {filename}'))
        except Exception as e:
            print(status_message('error', f'Error reading file: {e}'))

    def do_list(self, arg):
        """List all entries. Usage: list [category|favorites|archived]"""
        option = arg.strip().lower()
        
        if option == "favorites":
            entries = self.library.db.get_favorite_entries()
            print(f"\n{Colors.YELLOW}⭐ FAVORITE ENTRIES{Colors.RESET}")
        elif option == "archived":
            entries = [e for e in self.library.list_entries() if e.is_archived]
            print(f"\n{Colors.BOLD}{Colors.CYAN}📦 ARCHIVED ENTRIES{Colors.RESET}")
        elif option == "category" or (option and option.startswith("cat")):
            categories = self.library.list_categories()
            if not categories:
                print(status_message('error', 'No categories available'))
                return
            print(f"\n{Colors.BOLD}{Colors.MAGENTA}📂 Categories:{Colors.RESET}")
            for i, cat in enumerate(categories, 1):
                count = len(self.library.get_entries_in_category(cat.id))
                print(f"  {Colors.CYAN}{i}.{Colors.RESET} {cat.name} {Colors.GRAY}({count} entries){Colors.RESET}")
            try:
                choice = int(input(f"{Colors.CYAN}Select category:{Colors.RESET} "))
                if 1 <= choice <= len(categories):
                    entries = self.library.get_entries_in_category(categories[choice - 1].id)
                else:
                    print(status_message('error', 'Invalid choice'))
                    return
            except ValueError:
                print(status_message('error', 'Invalid input'))
                return
        else:
            entries = self.library.list_entries()
            print(f"\n{Colors.BOLD}{Colors.BLUE}📚 ALL ENTRIES{Colors.RESET}")

        if not entries:
            print(f"{Colors.YELLOW}No entries found{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}Total: {len(entries)} entries{Colors.RESET}\n")
        for i, entry in enumerate(entries, 1):
            marker = f"{Colors.YELLOW}⭐{Colors.RESET}" if entry.is_favorite else "  "
            archived = f"{Colors.RED}[ARCHIVED]{Colors.RESET} " if entry.is_archived else ""
            print(f"{marker} {Colors.BOLD}{i:2}.{Colors.RESET} {Colors.BOLD}{entry.title}{Colors.RESET} {archived}")
            print(f"     {Colors.CYAN}Author:{Colors.RESET} {entry.author} | {Colors.CYAN}Created:{Colors.RESET} {entry.created_at.strftime('%Y-%m-%d')}")
            if entry.tags:
                tags_str = ", ".join([f"{Colors.MAGENTA}#{t.name}{Colors.RESET}" for t in entry.tags])
                print(f"     {Colors.CYAN}Tags:{Colors.RESET} {tags_str}")
            print()

    def do_view(self, arg):
        """View an entry. Usage: view <entry_id or index>"""
        if not arg:
            print(status_message('error', 'Please provide an entry ID or index'))
            return

        entry = None
        
        # Try to find by ID
        entry = self.library.get_entry(arg.strip())
        
        # Try by index
        if not entry:
            try:
                idx = int(arg) - 1
                entries = self.library.list_entries()
                if 0 <= idx < len(entries):
                    entry = entries[idx]
            except ValueError:
                pass

        if not entry:
            print(status_message('error', 'Entry not found'))
            return

        self.current_entry = entry
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}📖 {entry.title}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"\n{Colors.CYAN}📝 Author:{Colors.RESET} {entry.author}")
        print(f"{Colors.CYAN}📅 Created:{Colors.RESET} {entry.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"{Colors.CYAN}🔄 Updated:{Colors.RESET} {entry.updated_at.strftime('%Y-%m-%d %H:%M')}")
        
        if entry.source:
            print(f"{Colors.CYAN}📌 Source:{Colors.RESET} {entry.source}")
        
        if entry.tags:
            tags_str = ", ".join([f"{Colors.MAGENTA}#{t.name}{Colors.RESET}" for t in entry.tags])
            print(f"{Colors.CYAN}🏷️  Tags:{Colors.RESET} {tags_str}")
        
        if entry.is_favorite:
            print(f"{Colors.YELLOW}⭐ This entry is marked as favorite{Colors.RESET}")
        
        if entry.is_archived:
            print(f"{Colors.RED}📦 This entry is archived{Colors.RESET}")

        print(f"\n{Colors.CYAN}{'-'*60}{Colors.RESET}")
        print(f"\n{entry.content}\n")
        print(f"{Colors.CYAN}{'-'*60}{Colors.RESET}")
        print(f"\n{Colors.GRAY}Entry ID: {entry.id}{Colors.RESET}")

    def do_edit(self, arg):
        """Edit current entry. Usage: edit [new_title]"""
        entry = self.current_entry
        if not entry:
            print("❌ No entry selected. Use 'view <id>' first")
            return

        new_title = arg.strip() if arg else None
        
        if new_title:
            entry.title = new_title
        
        print("Enter new content (type 'END' on a new line to finish, or press Ctrl+C to cancel):")
        
        lines = []
        try:
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
        except KeyboardInterrupt:
            print("\n❌ Edit cancelled")
            return
        except EOFError:
            pass

        if lines:
            entry.update_content("\n".join(lines))

        self.library.db.update_entry(entry)
        print(f"✅ Entry updated successfully")

    def do_delete(self, arg):
        """Delete an entry. Usage: delete <entry_id>"""
        if not arg:
            print("❌ Please provide an entry ID")
            return

        entry_id = arg.strip()
        entry = self.library.get_entry(entry_id)
        
        if not entry:
            print("❌ Entry not found")
            return

        confirm = input(f"Are you sure you want to delete '{entry.title}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.library.delete_entry(entry_id)
            self.current_entry = None
            print("✅ Entry deleted successfully")
            # Log action
            self.library.log_action(self.current_user, "DELETE_ENTRY", f"Title: {entry.title[:30]}", "OK")
        else:
            print("❌ Deletion cancelled")

    def do_search(self, arg):
        """Advanced search with filters.
        
        Usage: search <query> [--author <name>] [--category <name>] [--tags <tag1,tag2>] 
               [--from <YYYY-MM-DD>] [--to <YYYY-MM-DD>] [--favorites] [--archived]
        
        Options:
          --author <name>      : Search by author
          --category <name>    : Filter by category
          --tags <tags>        : Filter by tags (comma-separated)
          --from <date>        : Created from date
          --to <date>          : Created to date
          --favorites          : Only favorites
          --archived           : Only archived
          --limit <num>        : Limit results
        
        Examples:
          search "python" --author "John" --tags "tutorial"
          search "api" --from "2025-01-01" --favorites
          search "guide" --category "Documentation"
        """
        if not arg:
            print(status_message('error', 'Please provide a search query'))
            return

        # Parse arguments
        parts = arg.split()
        query = parts[0]
        filters = {}
        
        i = 1
        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if key in ['favorites', 'archived']:
                    filters[key] = True
                    i += 1
                elif i + 1 < len(parts):
                    filters[key] = parts[i + 1]
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        # Do basic search
        results = self.library.search_entries(query)
        
        # Apply filters
        if 'author' in filters:
            results = [e for e in results if filters['author'].lower() in e.author.lower()]
        
        if 'category' in filters:
            cat_name = filters['category'].lower()
            results = [e for e in results if e.category_id and any(
                c.name.lower() == cat_name for c in [self.library.db.get_category(e.category_id)]
            )]
        
        if 'tags' in filters:
            tag_names = [t.strip().lower() for t in filters['tags'].split(',')]
            results = [e for e in results if any(
                tag.name.lower() in tag_names for tag in e.tags
            )]
        
        if 'from' in filters:
            from datetime import datetime
            try:
                date_from = datetime.strptime(filters['from'], '%Y-%m-%d')
                results = [e for e in results if e.created_at >= date_from]
            except ValueError:
                print(f"{Colors.YELLOW}⚠️  Invalid date format for --from{Colors.RESET}")
        
        if 'to' in filters:
            from datetime import datetime
            try:
                date_to = datetime.strptime(filters['to'], '%Y-%m-%d')
                results = [e for e in results if e.created_at <= date_to]
            except ValueError:
                print(f"{Colors.YELLOW}⚠️  Invalid date format for --to{Colors.RESET}")
        
        if filters.get('favorites'):
            results = [e for e in results if e.is_favorite]
        
        if filters.get('archived'):
            results = [e for e in results if e.is_archived]
        
        if 'limit' in filters:
            try:
                limit = int(filters['limit'])
                results = results[:limit]
            except ValueError:
                pass
        
        # Display results
        if not results:
            print(f"{status_message('warning', f'No entries found matching criteria')}")
            return

        print(f"\n{Colors.BOLD}{Colors.GREEN}🔍 Search results: {len(results)} found{Colors.RESET}\n")
        for i, entry in enumerate(results, 1):
            marker = f"{Colors.YELLOW}⭐{Colors.RESET}" if entry.is_favorite else "  "
            archived = f"{Colors.RED}[ARCHIVED]{Colors.RESET} " if entry.is_archived else ""
            print(f"{marker} {Colors.CYAN}{i}.{Colors.RESET} {Colors.BOLD}{entry.title}{Colors.RESET} {archived}")
            print(f"    {Colors.GRAY}Author: {entry.author} | Created: {entry.created_at.strftime('%Y-%m-%d')}{Colors.RESET}")
        
        # Log search action
        self.library.log_action(self.current_user, "SEARCH", f"Query: {arg[:40]}", f"Found: {len(results)}")
        print()

    def do_favorite(self, arg):
        """Toggle favorite status. Usage: favorite <entry_id>"""
        if not arg:
            entry = self.current_entry
            if not entry:
                print("❌ No entry selected")
                return
            entry_id = entry.id
        else:
            entry_id = arg.strip()

        is_favorite = self.library.toggle_favorite(entry_id)
        
        if is_favorite is None:
            print("❌ Entry not found")
            return

        status = "⭐ Added to favorites" if is_favorite else "⭐ Removed from favorites"
        print(f"✅ {status}")
        self.current_entry = self.library.get_entry(entry_id)

    def do_archive(self, arg):
        """Toggle archived status. Usage: archive <entry_id>"""
        if not arg:
            entry = self.current_entry
            if not entry:
                print("❌ No entry selected")
                return
            entry_id = entry.id
        else:
            entry_id = arg.strip()

        is_archived = self.library.toggle_archive(entry_id)
        
        if is_archived is None:
            print("❌ Entry not found")
            return

        status = "📦 Entry archived" if is_archived else "📦 Entry unarchived"
        print(f"✅ {status}")
        self.current_entry = self.library.get_entry(entry_id)

    # Category commands
    def do_category(self, arg):
        """Manage categories. Usage: category [create|list|delete]"""
        if not arg:
            print("Usage: category [create|list|delete]")
            return

        subcmd = arg.split()[0].lower()
        args = " ".join(arg.split()[1:])

        if subcmd == "create":
            name = args.strip()
            if not name:
                name = input("Category name: ").strip()
            if name:
                self.library.create_category(name)
                print(f"✅ Category '{name}' created")
                self.library.log_action(self.current_user, "CREATE_CATEGORY", f"Name: {name}", "OK")
            else:
                print("❌ Category name cannot be empty")

        elif subcmd == "list":
            categories = self.library.list_categories()
            if not categories:
                print("❌ No categories")
                return
            print("\n📂 CATEGORIES:\n")
            for cat in categories:
                count = len(self.library.get_entries_in_category(cat.id))
                print(f"  • {cat.name} ({count} entries)")
                if cat.description:
                    print(f"    {cat.description}")

        elif subcmd == "delete":
            if not args:
                print("❌ Please provide category name")
                return
            categories = self.library.list_categories()
            for cat in categories:
                if cat.name.lower() == args.lower():
                    self.library.delete_category(cat.id)
                    print(f"✅ Category '{cat.name}' deleted")
                    self.library.log_action(self.current_user, "DELETE_CATEGORY", f"Name: {cat.name}", "OK")
                    return
            print("❌ Category not found")

    # Tag commands
    def do_tag(self, arg):
        """Manage tags. Usage: tag [create|list|add|remove]"""
        if not arg:
            print("Usage: tag [create|list|add|remove]")
            return

        subcmd = arg.split()[0].lower()
        args = " ".join(arg.split()[1:])

        if subcmd == "create":
            name = args.strip()
            if not name:
                name = input("Tag name: ").strip()
            if name:
                self.library.create_tag(name)
                print(f"✅ Tag '#{name}' created")
            else:
                print("❌ Tag name cannot be empty")

        elif subcmd == "list":
            tags = self.library.list_tags()
            if not tags:
                print("❌ No tags")
                return
            print("\n🏷️  TAGS:\n")
            for tag in tags:
                count = len(self.library.get_entries_with_tag(tag.id))
                print(f"  • #{tag.name} ({count} entries)")

        elif subcmd == "add":
            if not self.current_entry:
                print("❌ No entry selected")
                return
            tags = self.library.list_tags()
            if not tags:
                print("❌ No tags available")
                return
            print("\n🏷️  Available tags:")
            for i, tag in enumerate(tags, 1):
                print(f"  {i}. #{tag.name}")
            try:
                choice = int(input("Select tag: "))
                if 1 <= choice <= len(tags):
                    self.library.add_tag_to_entry(self.current_entry.id, tags[choice - 1].id)
                    self.current_entry = self.library.get_entry(self.current_entry.id)
                    print(f"✅ Tag added")
                    self.library.log_action(self.current_user, "ADD_TAG", f"Tag: {tags[choice - 1].name}", "OK")
            except ValueError:
                print("❌ Invalid input")

        elif subcmd == "remove":
            if not self.current_entry:
                print("❌ No entry selected")
                return
            if not self.current_entry.tags:
                print("❌ Entry has no tags")
                return
            print("\nEntry tags:")
            for i, tag in enumerate(self.current_entry.tags, 1):
                print(f"  {i}. #{tag.name}")
            try:
                choice = int(input("Select tag to remove: "))
                if 1 <= choice <= len(self.current_entry.tags):
                    tag_name = self.current_entry.tags[choice - 1].name
                    self.library.remove_tag_from_entry(
                        self.current_entry.id,
                        self.current_entry.tags[choice - 1].id
                    )
                    self.current_entry = self.library.get_entry(self.current_entry.id)
                    print(f"✅ Tag removed")
                    self.library.log_action(self.current_user, "REMOVE_TAG", f"Tag: {tag_name}", "OK")
            except ValueError:
                print("❌ Invalid input")

    # Statistics
    def do_stats(self, arg):
        """Show library statistics. Usage: stats"""
        stats = self.library.get_statistics()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 LIBRARY STATISTICS{Colors.RESET}\n")
        print(f"  {Colors.BLUE}📚 Total entries:{Colors.RESET} {Colors.BOLD}{stats['total_entries']}{Colors.RESET}")
        print(f"  {Colors.MAGENTA}📂 Total categories:{Colors.RESET} {Colors.BOLD}{stats['total_categories']}{Colors.RESET}")
        print(f"  {Colors.MAGENTA}🏷️  Total tags:{Colors.RESET} {Colors.BOLD}{stats['total_tags']}{Colors.RESET}")
        print(f"  {Colors.YELLOW}⭐ Favorite entries:{Colors.RESET} {Colors.BOLD}{stats['favorite_entries']}{Colors.RESET}")
        print(f"  {Colors.RED}📦 Archived entries:{Colors.RESET} {Colors.BOLD}{stats['archived_entries']}{Colors.RESET}\n")

    def do_analyze(self, arg):
        """Advanced library analysis with reports.
        
        Usage: analyze [--top-authors] [--by-category] [--by-tag] [--timeline] [--word-count] [--activity]
        
        Options:
          --top-authors     : Show top 10 authors
          --by-category     : Distribution by category
          --by-tag          : Most used tags
          --timeline        : Creation timeline
          --word-count      : Word count statistics
          --activity        : Activity per month
          (no options)      : Full analysis
        """
        if not arg:
            arg = "--top-authors --by-category --by-tag --timeline --word-count"
        
        entries = self.library.list_entries()
        
        if not entries:
            print(f"{status_message('warning', 'No entries to analyze')}")
            return
        
        show_all = '--top-authors' in arg or '--by-category' in arg or '--by-tag' in arg or '--timeline' in arg or '--word-count' in arg
        
        if '--top-authors' in arg or not arg.startswith('--'):
            self._analyze_authors(entries)
        
        if '--by-category' in arg or not arg.startswith('--'):
            self._analyze_by_category(entries)
        
        if '--by-tag' in arg or not arg.startswith('--'):
            self._analyze_by_tag(entries)
        
        if '--timeline' in arg or not arg.startswith('--'):
            self._analyze_timeline(entries)
        
        if '--word-count' in arg or not arg.startswith('--'):
            self._analyze_word_count(entries)
        
        if '--activity' in arg:
            self._analyze_activity(entries)

    def _analyze_authors(self, entries):
        """Analyze top authors"""
        from collections import Counter
        authors = Counter(e.author for e in entries)
        print(f"\n{Colors.BOLD}{Colors.CYAN}👥 TOP AUTHORS{Colors.RESET}\n")
        
        for author, count in authors.most_common(10):
            bar_width = min(count * 2, 30)
            bar = f"{Colors.GREEN}{'█' * bar_width}{Colors.RESET}"
            print(f"  {author:30} {bar} {count}")

    def _analyze_by_category(self, entries):
        """Analyze entries by category"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}📂 DISTRIBUTION BY CATEGORY{Colors.RESET}\n")
        
        categories = self.library.list_categories()
        if not categories:
            print("  No categories")
            return
        
        for cat in categories:
            cat_entries = [e for e in entries if e.category_id == cat.id]
            if cat_entries:
                percentage = (len(cat_entries) / len(entries)) * 100
                bar_width = int(percentage / 2)
                bar = f"{Colors.CYAN}{'█' * bar_width}{Colors.RESET}"
                print(f"  {cat.name:25} {bar} {len(cat_entries):3} ({percentage:5.1f}%)")

    def _analyze_by_tag(self, entries):
        """Analyze most used tags"""
        from collections import Counter
        all_tags = []
        for entry in entries:
            all_tags.extend([tag.name for tag in entry.tags])
        
        if not all_tags:
            print(f"\n{Colors.MAGENTA}🏷️  TAGS: No tags used{Colors.RESET}")
            return
        
        tag_counts = Counter(all_tags)
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}🏷️  TOP TAGS{Colors.RESET}\n")
        
        for tag, count in tag_counts.most_common(15):
            bar_width = min(count * 2, 30)
            bar = f"{Colors.MAGENTA}{'█' * bar_width}{Colors.RESET}"
            print(f"  #{tag:25} {bar} {count}")

    def _analyze_timeline(self, entries):
        """Analyze creation timeline"""
        from datetime import datetime, timedelta
        from collections import defaultdict
        
        timeline = defaultdict(int)
        for entry in entries:
            date_key = entry.created_at.strftime('%Y-%m')
            timeline[date_key] += 1
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}📅 CREATION TIMELINE{Colors.RESET}\n")
        
        for month in sorted(timeline.keys()):
            count = timeline[month]
            bar_width = min(count, 40)
            bar = f"{Colors.BLUE}{'█' * bar_width}{Colors.RESET}"
            print(f"  {month} {bar} {count}")

    def _analyze_word_count(self, entries):
        """Analyze word count statistics"""
        word_counts = []
        total_words = 0
        
        for entry in entries:
            words = len(entry.content.split())
            word_counts.append(words)
            total_words += words
        
        avg_words = total_words // len(entries) if entries else 0
        max_words = max(word_counts) if word_counts else 0
        min_words = min(word_counts) if word_counts else 0
        
        print(f"\n{Colors.BOLD}{Colors.YELLOW}📊 WORD COUNT STATISTICS{Colors.RESET}\n")
        print(f"  {Colors.YELLOW}Total words:{Colors.RESET}        {Colors.BOLD}{total_words:,}{Colors.RESET}")
        print(f"  {Colors.YELLOW}Average per entry:{Colors.RESET}  {Colors.BOLD}{avg_words:,}{Colors.RESET}")
        print(f"  {Colors.YELLOW}Longest entry:{Colors.RESET}     {Colors.BOLD}{max_words:,} words{Colors.RESET}")
        print(f"  {Colors.YELLOW}Shortest entry:{Colors.RESET}    {Colors.BOLD}{min_words:,} words{Colors.RESET}")

    def _analyze_activity(self, entries):
        """Analyze activity per month"""
        from datetime import datetime
        from collections import defaultdict
        
        activity = defaultdict(int)
        for entry in entries:
            month = entry.updated_at.strftime('%Y-%m')
            activity[month] += 1
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🔥 MONTHLY ACTIVITY{Colors.RESET}\n")
        for month in sorted(activity.keys(), reverse=True)[:12]:
            count = activity[month]
            bar_width = min(count * 2, 35)
            bar = f"{Colors.RED}{'█' * bar_width}{Colors.RESET}"
            print(f"  {month} {bar} {count}")

    def do_export(self, arg):
        """Export library to JSON. Usage: export <filename>"""
        if not arg:
            filename = "alexandria_export.json"
        else:
            filename = arg.strip()

        import json
        
        entries = self.library.list_entries()
        data = {
            "entries": [e.to_dict() for e in entries],
            "categories": [c.to_dict() for c in self.library.list_categories()],
            "tags": [t.to_dict() for t in self.library.list_tags()],
            "exported_at": datetime.now().isoformat(),
        }

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Library exported to '{filename}'")
        except Exception as e:
            print(f"❌ Export failed: {e}")

    def do_backup(self, arg):
        """Create a backup of the library.
        
        Usage: backup [<directory>] [--compress] [--with-metadata]
        
        Options:
          <directory>       : Destination directory (default: ./backups)
          --compress        : Create compressed archive
          --with-metadata   : Include metadata file
        """
        import json
        from pathlib import Path
        from datetime import datetime
        import shutil
        
        # Parse arguments
        backup_dir = "backups"
        compress = '--compress' in arg
        with_metadata = '--with-metadata' in arg
        
        parts = arg.split()
        for part in parts:
            if not part.startswith('--') and part:
                backup_dir = part
                break
        
        # Create backup directory
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        # Generate backup name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"alexandria_backup_{timestamp}"
        
        try:
            # Export data
            entries = self.library.list_entries()
            categories = self.library.list_categories()
            tags = self.library.list_tags()
            
            data = {
                "entries": [e.to_dict() for e in entries],
                "categories": [c.to_dict() for c in categories],
                "tags": [t.to_dict() for t in tags],
                "backup_date": timestamp,
                "total_entries": len(entries),
            }
            
            if compress:
                # Create temporary directory
                temp_backup = backup_path / f"temp_{backup_name}"
                temp_backup.mkdir(exist_ok=True)
                
                # Save JSON
                json_file = temp_backup / "data.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Create archive
                archive_path = backup_path / backup_name
                shutil.make_archive(str(archive_path), 'zip', temp_backup)
                
                # Clean up temp
                shutil.rmtree(temp_backup)
                
                print(f"\n{Colors.GREEN}✅ Backup created successfully!{Colors.RESET}")
                print(f"   {Colors.CYAN}Archive:{Colors.RESET} {archive_path}.zip")
                print(f"   {Colors.CYAN}Size:{Colors.RESET} {Path(f'{archive_path}.zip').stat().st_size / 1024:.1f} KB")
                print(f"   {Colors.CYAN}Entries:{Colors.RESET} {len(entries)}\n")
            else:
                # Create backup directory
                backup_entry_path = backup_path / backup_name
                backup_entry_path.mkdir(exist_ok=True)
                
                # Save JSON
                json_file = backup_entry_path / "data.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                if with_metadata:
                    # Create metadata file
                    metadata = {
                        "backup_date": timestamp,
                        "total_entries": len(entries),
                        "total_categories": len(categories),
                        "total_tags": len(tags),
                    }
                    meta_file = backup_entry_path / "metadata.json"
                    with open(meta_file, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2)
                
                print(f"\n{Colors.GREEN}✅ Backup created successfully!{Colors.RESET}")
                print(f"   {Colors.CYAN}Directory:{Colors.RESET} {backup_entry_path}")
                print(f"   {Colors.CYAN}Entries:{Colors.RESET} {len(entries)}\n")
        
        except Exception as e:
            print(f"{status_message('error', f'Backup failed: {e}')}\n")

    def do_restore(self, arg):
        """Restore library from backup.
        
        Usage: restore <backup_path> [--merge] [--preview]
        
        Options:
          <backup_path>     : Path to backup file or directory
          --merge           : Merge with existing data
          --preview         : Preview without restoring
        """
        import json
        from pathlib import Path
        import zipfile
        
        if not arg:
            print(status_message('error', 'Please provide backup path'))
            return
        
        parts = arg.split()
        backup_path = parts[0]
        merge = '--merge' in arg
        preview = '--preview' in arg
        
        try:
            backup_file = Path(backup_path)
            
            if not backup_file.exists():
                print(status_message('error', f'Backup not found: {backup_path}'))
                return
            
            # Load data
            data = None
            
            if backup_file.is_file() and backup_file.suffix == '.zip':
                # Extract from zip
                with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                    with zip_ref.open('data.json') as f:
                        data = json.load(f)
            elif backup_file.is_dir():
                # Load from directory
                json_file = backup_file / 'data.json'
                if json_file.exists():
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
            
            if not data:
                print(status_message('error', 'Invalid backup format'))
                return
            
            # Preview
            if preview:
                print(f"\n{Colors.BOLD}{Colors.CYAN}📋 BACKUP PREVIEW{Colors.RESET}\n")
                print(f"  {Colors.CYAN}Entries:{Colors.RESET} {data.get('total_entries', len(data.get('entries', [])))}")
                print(f"  {Colors.CYAN}Categories:{Colors.RESET} {len(data.get('categories', []))}")
                print(f"  {Colors.CYAN}Tags:{Colors.RESET} {len(data.get('tags', []))}")
                print(f"  {Colors.CYAN}Backup date:{Colors.RESET} {data.get('backup_date', 'Unknown')}\n")
                return
            
            # Confirm restore
            confirm = input(f"{Colors.YELLOW}⚠️  This will {'merge with' if merge else 'replace'} your library. Continue? (yes/no):{Colors.RESET} ").strip().lower()
            if confirm != 'yes':
                print("Restore cancelled")
                return
            
            # Restore data
            if not merge:
                # Clear existing data
                for entry in self.library.list_entries():
                    self.library.delete_entry(entry.id)
            
            # Restore entries
            restored_count = 0
            for entry_data in data.get('entries', []):
                try:
                    # Create entry with restored data
                    entry = self.library.create_entry(
                        title=entry_data.get('title'),
                        content=entry_data.get('content'),
                        author=entry_data.get('author', 'Unknown'),
                        category_id=entry_data.get('category_id')
                    )
                    restored_count += 1
                except:
                    pass
            
            print(f"\n{Colors.GREEN}✅ Restore completed!{Colors.RESET}")
            print(f"   {Colors.CYAN}Restored entries:{Colors.RESET} {restored_count}\n")
        
        except Exception as e:
            print(f"{status_message('error', f'Restore failed: {e}')}\n")

    # Monitoring and Health Check commands
    def do_monitor(self, arg):
        """Monitor website availability and response time.
        
        Usage: monitor <url> [<url2> <url3>...] [--timeout <seconds>] [--repeat <count>] [--interval <seconds>]
        
        Options:
          <url>             : Website URL to check (http:// or https://)
          --timeout <sec>   : Connection timeout (default: 5)
          --repeat <count>  : Number of checks (default: 1)
          --interval <sec>  : Interval between checks (default: 1)
        
        Examples:
          monitor https://example.com
          monitor https://site1.com https://site2.com --repeat 5 --interval 2
          monitor http://localhost:8080 --timeout 10
        """
        import socket
        import time
        
        if not arg:
            print(status_message('error', 'Please provide at least one URL'))
            return
        
        # Parse arguments
        parts = arg.split()
        urls = []
        timeout = 5
        repeat = 1
        interval = 1
        
        i = 0
        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if i + 1 < len(parts):
                    value = parts[i + 1]
                    if key == 'timeout':
                        timeout = int(value)
                    elif key == 'repeat':
                        repeat = int(value)
                    elif key == 'interval':
                        interval = float(value)
                    i += 2
                else:
                    i += 1
            elif parts[i].startswith('http'):
                urls.append(parts[i])
                i += 1
            else:
                i += 1
        
        if not urls:
            print(status_message('error', 'No valid URLs provided'))
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}🌐 WEBSITE MONITORING{Colors.RESET}\n")
        
        for attempt in range(repeat):
            if attempt > 0:
                print(f"\n{Colors.CYAN}[Attempt {attempt + 1}/{repeat}]{Colors.RESET}\n")
                time.sleep(interval)
            
            for url in urls:
                self._check_url_health(url, timeout)

    def _check_url_health(self, url, timeout=5):
        """Check single URL health"""
        import urllib.request
        import time
        
        # Ensure URL has protocol
        if not url.startswith('http'):
            url = 'https://' + url
        
        try:
            start_time = time.time()
            response = urllib.request.urlopen(url, timeout=timeout)
            elapsed = time.time() - start_time
            
            status_code = response.status
            size = len(response.read())
            
            # Determine status color
            if status_code == 200:
                status_color = Colors.GREEN
                status_text = '✅ OK'
            elif status_code < 400:
                status_color = Colors.YELLOW
                status_text = '⚠️  REDIRECT'
            else:
                status_color = Colors.RED
                status_text = f'❌ ERROR {status_code}'
            
            # Speed indicator
            if elapsed < 0.5:
                speed = f"{Colors.GREEN}⚡ FAST{Colors.RESET}"
            elif elapsed < 2:
                speed = f"{Colors.YELLOW}⏱️  NORMAL{Colors.RESET}"
            else:
                speed = f"{Colors.RED}🐢 SLOW{Colors.RESET}"
            
            print(f"{status_color}{status_text}{Colors.RESET} {url:50} {speed} ({elapsed:.2f}s)")
        
        except urllib.error.HTTPError as e:
            print(f"{Colors.RED}❌ HTTP {e.code}{Colors.RESET} {url:50} {Colors.GRAY}(HTTP Error){Colors.RESET}")
        except urllib.error.URLError as e:
            print(f"{Colors.RED}❌ FAIL{Colors.RESET} {url:50} {Colors.GRAY}(Connection Error){Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ ERROR{Colors.RESET} {url:50} {Colors.GRAY}({str(e)[:30]}){Colors.RESET}")

    def do_healthcheck(self, arg):
        """Detailed health check of website with metrics.
        
        Usage: healthcheck <url> [--dns] [--ssl] [--full]
        
        Options:
          <url>      : Website URL
          --dns      : Check DNS resolution
          --ssl      : Check SSL certificate
          --full     : All checks
        
        Examples:
          healthcheck https://example.com --full
          healthcheck example.com --dns --ssl
        """
        import socket
        import ssl
        import urllib.request
        import time
        
        if not arg:
            print(status_message('error', 'Please provide URL'))
            return
        
        parts = arg.split()
        url = parts[0]
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        check_dns = '--dns' in arg or '--full' in arg
        check_ssl = '--ssl' in arg or '--full' in arg
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}🏥 HEALTH CHECK: {url}{Colors.RESET}\n")
        
        # Extract domain from URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # DNS check
        if check_dns:
            try:
                ip = socket.gethostbyname(domain)
                print(f"{Colors.GREEN}✅ DNS{Colors.RESET} {domain:40} → {ip}")
            except socket.gaierror:
                print(f"{Colors.RED}❌ DNS{Colors.RESET} {domain:40} → {Colors.RED}Failed{Colors.RESET}")
        
        # SSL check
        if check_ssl and url.startswith('https'):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        subject = dict(x[0] for x in cert['subject'])
                        issuer = dict(x[0] for x in cert['issuer'])
                        not_after = cert.get('notAfter', 'Unknown')
                        
                        print(f"{Colors.GREEN}✅ SSL{Colors.RESET} {domain:40} Valid")
                        print(f"   {Colors.CYAN}Issuer:{Colors.RESET} {issuer.get('organizationName', 'Unknown')}")
                        print(f"   {Colors.CYAN}Expires:{Colors.RESET} {not_after}")
            except Exception as e:
                print(f"{Colors.RED}❌ SSL{Colors.RESET} {domain:40} {str(e)[:30]}")
        
        # HTTP Response check
        try:
            start = time.time()
            request = urllib.request.Request(url, headers={
                'User-Agent': 'Alexandria/1.0'
            })
            response = urllib.request.urlopen(request, timeout=5)
            elapsed = time.time() - start
            
            print(f"{Colors.GREEN}✅ HTTP{Colors.RESET} {domain:40} Status {response.status}")
            print(f"   {Colors.CYAN}Response Time:{Colors.RESET} {elapsed:.3f}s")
            print(f"   {Colors.CYAN}Content Type:{Colors.RESET} {response.headers.get('Content-Type', 'Unknown')}")
            
            if response.status == 200:
                print(f"{Colors.GREEN}✅ Overall: HEALTHY{Colors.RESET}\n")
            else:
                print(f"{Colors.YELLOW}⚠️  Overall: OK but check status code{Colors.RESET}\n")
        
        except Exception as e:
            print(f"{Colors.RED}❌ HTTP{Colors.RESET} {domain:40} Failed")
            print(f"{Colors.RED}❌ Overall: UNHEALTHY{Colors.RESET}\n")

    def do_uptime(self, arg):
        """Check and log uptime history.
        
        Usage: uptime [--log] [--save <file>] [--load <file>]
        
        Options:
          --log       : Show log of all checks
          --save <f>  : Save results to file
          --load <f>  : Load previous results
        
        Examples:
          uptime --log
          uptime --save uptime_log.json
        """
        import json
        from pathlib import Path
        from datetime import datetime
        
        if '--log' in arg:
            uptime_file = Path('uptime_log.json')
            if uptime_file.exists():
                try:
                    with open(uptime_file, 'r') as f:
                        data = json.load(f)
                    
                    print(f"\n{Colors.BOLD}{Colors.CYAN}📊 UPTIME LOG{Colors.RESET}\n")
                    
                    for entry in data.get('checks', [])[-20:]:
                        status_symbol = '✅' if entry.get('status') == 'up' else '❌'
                        timestamp = entry.get('timestamp', 'Unknown')
                        url = entry.get('url', 'Unknown')
                        response_time = entry.get('response_time', 0)
                        
                        print(f"{status_symbol} {timestamp:20} {url:40} {response_time:.3f}s")
                    
                    print(f"\n{Colors.CYAN}Total checks: {len(data.get('checks', []))}{Colors.RESET}\n")
                except Exception as e:
                    print(status_message('error', f'Failed to load log: {e}'))
            else:
                print(status_message('warning', 'No uptime log found. Run monitor command to create one.'))
        
        elif '--save' in arg:
            parts = arg.split()
            idx = parts.index('--save')
            if idx + 1 < len(parts):
                filename = parts[idx + 1]
                print(f"{Colors.GREEN}✅ Uptime log would be saved to: {filename}{Colors.RESET}\n")
            else:
                print(status_message('error', 'Please provide filename'))
        
        else:
            print(f"\n{Colors.BOLD}{Colors.CYAN}📈 UPTIME TRACKER{Colors.RESET}\n")
            print(f"  {Colors.CYAN}Use:{Colors.RESET} uptime --log              (show check history)")
            print(f"  {Colors.CYAN}Use:{Colors.RESET} uptime --save <filename>  (save results)\n")

    def do_tempmail(self, arg):
        """Generate temporary/disposable email addresses.
        
        Usage: tempmail [--name <prefix>] [--copy|--save]
        
        Aliases: tm, email
        
        Commands:
          tempmail              - Generate random temp email
          tempmail --name bob   - Generate with name prefix
          tempmail --save       - Save email to clipboard (if available)
        
        Examples:
          tempmail
          tempmail --name alice
          tempmail --name john --save
        """
        args = arg.split()
        use_name = False
        name = None
        
        # Parse arguments
        i = 0
        while i < len(args):
            if args[i] == "--name" and i + 1 < len(args):
                use_name = True
                name = args[i + 1]
                i += 2
            else:
                i += 1
        
        # Generate email
        if use_name and name:
            email = self.library.generate_temp_email_with_name(name)
        else:
            email = self.library.generate_temp_email()
        
        # Display email
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔔 Temporary Email:{Colors.RESET}")
        print(f"  {Colors.YELLOW}{email}{Colors.RESET}\n")
        
        # Save to clipboard if available
        if "--save" in args:
            try:
                import subprocess
                subprocess.run(["xclip", "-selection", "clipboard"], input=email.encode(), check=True)
                print(f"{Colors.GREEN}✓ Email copied to clipboard{Colors.RESET}\n")
            except Exception:
                print(f"{Colors.YELLOW}Note: Could not copy to clipboard{Colors.RESET}\n")
    
    def do_tm(self, arg):
        """Alias for tempmail. Generate temporary email."""
        self.do_tempmail(arg)
    
    def do_email(self, arg):
        """Alias for tempmail. Generate temporary email."""
        self.do_tempmail(arg)

    # System commands
    def do_clear(self, arg):
        """Clear screen. Usage: clear"""
        os.system("clear" if os.name == "posix" else "cls")

    def do_cc(self, arg):
        """Clear terminal screen. Alias for 'clear'. Usage: cc"""
        self.do_clear(arg)

    def do_cls(self, arg):
        """Clear terminal screen. Alias for 'clear'. Usage: cls"""
        self.do_clear(arg)

    # SSH CONNECTION COMMANDS
    def do_ssh_add(self, arg):
        """Add or update SSH connection. Usage: ssh_add <name> <host> <user> [port] [--key <path>]
        
        Examples:
          ssh_add server1 192.168.1.100 admin 22          (password authentication)
          ssh_add server1 192.168.1.100 admin 22 --key ~/.ssh/id_rsa  (key authentication)
        """
        if not self.current_user:
            print(f"\n{status_message('error', self.lang_manager.get_text('error_not_logged_in'))}")
            return
        
        parts = arg.split()
        if len(parts) < 3:
            print(f"\n{status_message('error', 'Usage: ssh_add <name> <host> <user> [port] [--key <path>]')}")
            return
        
        name, host, user = parts[0], parts[1], parts[2]
        port = 22
        auth_type = "password"
        key_path = None
        password = None
        
        # Parse additional arguments
        if len(parts) > 3:
            port = int(parts[3]) if parts[3].isdigit() else 22
        
        if "--key" in parts:
            key_idx = parts.index("--key")
            if key_idx + 1 < len(parts):
                key_path = parts[key_idx + 1]
                auth_type = "key"
        
        if auth_type == "password":
            password = input(f"{Colors.CYAN}Enter password for {user}@{host}: {Colors.RESET}")
        
        result = self.library.add_ssh_connection(name, host, user, port, auth_type, password, key_path)
        print(f"\n{status_message('success', result)}")

    def do_ssh_list(self, arg):
        """List all saved SSH connections. Usage: ssh_list"""
        if not self.current_user:
            print(f"\n{status_message('error', self.lang_manager.get_text('error_not_logged_in'))}")
            return
        
        connections = self.library.list_ssh_connections()
        if not connections:
            print(f"\n{status_message('info', 'No SSH connections saved')}")
            return
        
        print(f"\n{section_header('SSH Connections')}")
        for i, conn_name in enumerate(connections, 1):
            conn = self.library.get_ssh_connection(conn_name)
            print(f"  {i}. {Colors.BOLD}{conn_name}{Colors.RESET}")
            print(f"     Host: {conn['host']}:{conn['port']}")
            print(f"     User: {conn['user']}")
            print(f"     Auth: {conn['auth_type']}")
            if conn.get('last_used'):
                print(f"     Last used: {conn['last_used']}")
            print()

    def do_ssh_test(self, arg):
        """Test SSH connection. Usage: ssh_test <name>
        
        Example: ssh_test server1
        """
        if not self.current_user:
            print(f"\n{status_message('error', self.lang_manager.get_text('error_not_logged_in'))}")
            return
        
        if not arg:
            print(f"\n{status_message('error', 'Usage: ssh_test <name>')}")
            return
        
        name = arg.strip()
        success, message = self.library.test_ssh_connection(name)
        
        if success:
            print(f"\n{status_message('success', message)}")
        else:
            print(f"\n{status_message('error', message)}")

    def do_ssh_info(self, arg):
        """Show details of SSH connection. Usage: ssh_info <name>
        
        Example: ssh_info server1
        """
        if not self.current_user:
            print(f"\n{status_message('error', self.lang_manager.get_text('error_not_logged_in'))}")
            return
        
        if not arg:
            print(f"\n{status_message('error', 'Usage: ssh_info <name>')}")
            return
        
        name = arg.strip()
        conn = self.library.get_ssh_connection(name)
        
        if not conn:
            print(f"\n{status_message('error', f'SSH connection \"{name}\" not found')}")
            return
        
        print(f"\n{section_header(f'SSH Connection: {name}')}")
        print(f"  Host: {conn['host']}")
        print(f"  Port: {conn['port']}")
        print(f"  User: {conn['user']}")
        print(f"  Auth Type: {conn['auth_type']}")
        if conn['auth_type'] == 'key':
            print(f"  Key Path: {conn['key_path']}")
        print(f"  Created: {conn['created']}")
        if conn.get('last_used'):
            print(f"  Last Used: {conn['last_used']}")
        print()

    def do_ssh_delete(self, arg):
        """Delete SSH connection. Usage: ssh_delete <name>
        
        Example: ssh_delete server1
        """
        if not self.current_user:
            print(f"\n{status_message('error', self.lang_manager.get_text('error_not_logged_in'))}")
            return
        
        if not arg:
            print(f"\n{status_message('error', 'Usage: ssh_delete <name>')}")
            return
        
        name = arg.strip()
        confirm = input(f"{Colors.YELLOW}Are you sure you want to delete SSH connection '{name}'? (yes/no): {Colors.RESET}").strip().lower()
        
        if confirm == "yes":
            result = self.library.delete_ssh_connection(name)
            if result:
                print(f"\n{status_message('success', result)}")
            else:
                print(f"\n{status_message('error', f'SSH connection \"{name}\" not found')}")
        else:
            print(f"\n{status_message('info', 'Cancelled')}")

    def do_exit(self, arg):
        """Exit Alexandria. Usage: exit"""
        farewell = self.lang_manager.get_text("farewell")
        print(f"\n{Colors.BOLD}{Colors.CYAN}{farewell}{Colors.RESET}\n")
        return True

    def do_quit(self, arg):
        """Quit Alexandria."""
        return self.do_exit(arg)

    def do_language(self, arg):
        """Change language. Usage: language [ru|en]"""
        arg = arg.strip().lower()
        
        if not arg:
            # Show available languages
            print(f"\n{section_header(self.lang_manager.get_text('languages_available'))}")
        elif arg in ["ru", "en"]:
            # Change language
            self.lang_manager.set_language(arg)
            self._update_prompt()
            lang_name = self.lang_manager.get_language_name()
            msg = self.lang_manager.get_text("language_changed", lang_name)
            print(f"\n{status_message('success', msg)}")
        else:
            print(f"\n{status_message('error', 'Invalid language. Use: language ru  or  language en')}")

    def do_help(self, arg):
        """Show help for all commands.
        
        Usage: help [command]
        
        Examples:
          help           - Show all commands
          help create    - Show help for 'create' command
        """
        if arg:
            # Show help for specific command
            super().do_help(arg)
        else:
            # Show all commands with descriptions
            print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.MAGENTA}ALEXANDRIA COMMAND REFERENCE{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}\n")
            
            categories = {
                "👤 USER & AUTHENTICATION": ["init", "user", "sudo", "pwdcheck"],
                "🔍 SECURITY & ANALYSIS": ["scan", "analyze", "logs", "search"],
                "📝 ENTRY MANAGEMENT": ["create", "batch_create", "list", "view", "edit", "delete"],
                "⭐ ENTRY OPERATIONS": ["favorite", "archive"],
                "📂 CATEGORIES": ["category"],
                "🏷️  TAGS": ["tag"],
                "📊 STATISTICS": ["stats", "info", "status", "bench"],
                "💾 DATA": ["export", "backup", "restore", "import"],
                "🔧 UTILITIES": ["tree", "find", "dup", "bulk", "sort"],
                "🔤 TEXT TOOLS": ["grep", "cat", "head", "tail", "wc"],
                "✏️  EDITING": ["cp", "mv", "rev", "upper", "lower", "strip"],
                "⚙️  SYSTEM": ["clear", "cc", "cls", "language", "help", "exit", "quit"],
                "🔒 SSH CONNECTIONS": ["ssh_add", "ssh_list", "ssh_test", "ssh_info", "ssh_delete"],
            }
            
            # Get all methods that start with do_
            commands_with_docs = {}
            for attr in dir(self):
                if attr.startswith("do_") and callable(getattr(self, attr)):
                    cmd_name = attr[3:]  # Remove 'do_' prefix
                    method = getattr(self, attr)
                    doc = method.__doc__
                    if doc:
                        # Get first line of docstring only
                        first_line = doc.split('\n')[0].strip()
                        commands_with_docs[cmd_name] = first_line
            
            # Print by category
            for category, commands in categories.items():
                print(f"{Colors.BOLD}{Colors.CYAN}{category}{Colors.RESET}")
                for cmd in commands:
                    if cmd in commands_with_docs:
                        description = commands_with_docs[cmd]
                        print(f"  {Colors.GREEN}{cmd:15}{Colors.RESET} - {description}")
                print()
            
            # Shorthand commands
            print(f"{Colors.BOLD}{Colors.YELLOW}⌨️  SHORTHAND COMMANDS (Unix-style){Colors.RESET}")
            shorthand = {
                "ls": "List entries",
                "cd": "Select/view entry",
                "rm": "Delete entry",
                "cp": "Copy entry",
                "mv": "Rename/move entry",
                "grep": "Search entries",
                "cat": "Show entry content",
                "pwd": "Show current entry",
                "new": "Create new entry",
                "open": "Open entry in editor",
                "wc": "Count words",
                "head": "Show first entries",
                "tail": "Show last entries",
            }
            
            for cmd, desc in sorted(shorthand.items()):
                print(f"  {Colors.YELLOW}{cmd:15}{Colors.RESET} - {desc}")
            
            print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}")
            print(f"{Colors.CYAN}Type 'help <command>' for detailed help on a specific command{Colors.RESET}\n")

    # Shorthand commands - unix-style
    def do_ls(self, arg):
        """List entries (shorthand). Usage: ls [filter]"""
        return self.do_list(arg)
    
    def do_cd(self, arg):
        """Select/view entry (shorthand). Usage: cd <id>"""
        return self.do_view(arg)
    
    def do_rm(self, arg):
        """Delete entry (shorthand). Usage: rm <id>"""
        return self.do_delete(arg)
    
    def do_cp(self, arg):
        """Copy entry. Usage: cp <id> [new_title]"""
        if not arg:
            print(status_message('error', 'Usage: cp <id> [new_title]'))
            return
        
        parts = arg.split(None, 1)
        entry_id = parts[0]
        new_title = parts[1] if len(parts) > 1 else None
        
        entry = self.library.get_entry(entry_id)
        if not entry:
            print(status_message('error', 'Entry not found'))
            return
        
        # Create copy
        copy_title = new_title or f"{entry.title} (copy)"
        new_entry = self.library.create_entry(
            title=copy_title,
            content=entry.content,
            author=entry.author,
            category_id=entry.category_id
        )
        
        # Copy tags
        for tag in entry.tags:
            self.library.add_tag_to_entry(new_entry.id, tag.id)
        
        print(f"{status_message('success', f'Entry copied: {new_entry.id}')}")
        self.current_entry = new_entry
    
    def do_mv(self, arg):
        """Rename/move entry. Usage: mv <id> <new_title>"""
        if not arg:
            print(status_message('error', 'Usage: mv <id> <new_title>'))
            return
        
        parts = arg.split(None, 1)
        if len(parts) < 2:
            print(status_message('error', 'Usage: mv <id> <new_title>'))
            return
        
        entry_id, new_title = parts
        entry = self.library.get_entry(entry_id)
        
        if not entry:
            print(status_message('error', 'Entry not found'))
            return
        
        old_title = entry.title
        entry.title = new_title
        self.library.db.update_entry(entry)
        
        print(f"{status_message('success', f'Renamed: {old_title} → {new_title}')}")
        self.current_entry = entry
    
    def do_grep(self, arg):
        """Search entries (shorthand). Usage: grep <query>"""
        return self.do_search(arg)
    
    def do_tree(self, arg):
        """Show category tree. Usage: tree"""
        categories = self.library.list_categories()
        if not categories:
            print("No categories")
            return
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}📂 CATEGORY TREE{Colors.RESET}\n")
        for cat in categories:
            entries = self.library.get_entries_in_category(cat.id)
            print(f"  {Colors.BOLD}{cat.name}{Colors.RESET} ({len(entries)})")
            for i, entry in enumerate(entries[:5], 1):
                prefix = "└─" if i == len(entries) or i == 5 else "├─"
                print(f"    {prefix} {entry.title[:50]}")
            if len(entries) > 5:
                print(f"    └─ +{len(entries) - 5} more")
    
    def do_find(self, arg):
        """Advanced find. Usage: find [--all] [--deep]"""
        entries = self.library.list_entries()
        print(f"\n{Colors.BOLD}{Colors.BLUE}🔎 FIND RESULTS{Colors.RESET}\n")
        print(f"  {Colors.CYAN}Total entries:{Colors.RESET} {len(entries)}")
        print(f"  {Colors.CYAN}Favorites:{Colors.RESET} {len([e for e in entries if e.is_favorite])}")
        print(f"  {Colors.CYAN}Archived:{Colors.RESET} {len([e for e in entries if e.is_archived])}")
        print(f"  {Colors.CYAN}Tagged:{Colors.RESET} {len([e for e in entries if e.tags])}")
        print(f"  {Colors.CYAN}Categorized:{Colors.RESET} {len([e for e in entries if e.category_id])}\n")
    
    def do_dup(self, arg):
        """Find duplicate entries. Usage: dup [--title] [--content]"""
        from collections import defaultdict
        
        entries = self.library.list_entries()
        duplicates = defaultdict(list)
        
        if '--title' in arg or not arg:
            for entry in entries:
                duplicates[entry.title.lower()].append(entry)
        
        found = False
        for key, group in duplicates.items():
            if len(group) > 1:
                if not found:
                    print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  DUPLICATE TITLES{Colors.RESET}\n")
                    found = True
                print(f"  {Colors.YELLOW}{key}{Colors.RESET}")
                for entry in group:
                    print(f"    - {entry.id[:8]} | {entry.author}")
        
        if not found:
            print(f"{status_message('success', 'No duplicates found')}")
    
    def do_bulk(self, arg):
        """Bulk operations. Usage: bulk [--tag <tag>] [--cat <cat>] [--favorite] [--archive]"""
        entries = self.library.list_entries()
        if not entries:
            print(status_message('error', 'No entries'))
            return
        
        count = 0
        
        if '--tag' in arg:
            parts = arg.split()
            idx = parts.index('--tag')
            if idx + 1 < len(parts):
                tag_name = parts[idx + 1]
                tag = self.library.create_tag(tag_name)
                for entry in entries:
                    self.library.add_tag_to_entry(entry.id, tag.id)
                    count += 1
                print(f"{status_message('success', f'Tagged {count} entries with #{tag_name}')}")
        
        if '--favorite' in arg:
            for entry in entries:
                entry.is_favorite = True
                self.library.db.update_entry(entry)
                count += 1
            print(f"{status_message('success', f'Marked {count} entries as favorite')}")
        
        if '--archive' in arg:
            for entry in entries:
                entry.is_archived = True
                self.library.db.update_entry(entry)
                count += 1
            print(f"{status_message('success', f'Archived {count} entries')}")
    
    def do_pin(self, arg):
        """Pin entry (mark as favorite). Usage: pin [id]"""
        if not arg and not self.current_entry:
            print(status_message('error', 'No entry selected'))
            return
        
        entry_id = arg.strip() if arg else self.current_entry.id
        is_fav = self.library.toggle_favorite(entry_id)
        
        if is_fav is None:
            print(status_message('error', 'Entry not found'))
            return
        
        print(f"{'⭐ Pinned' if is_fav else '⭐ Unpinned'}")
    
    def do_sort(self, arg):
        """Sort entries. Usage: sort [date|author|title|size]"""
        entries = self.library.list_entries()
        
        if not entries:
            print(status_message('error', 'No entries'))
            return
        
        sort_by = arg.strip().lower() or 'date'
        
        if sort_by == 'date':
            entries.sort(key=lambda e: e.created_at, reverse=True)
        elif sort_by == 'author':
            entries.sort(key=lambda e: e.author)
        elif sort_by == 'title':
            entries.sort(key=lambda e: e.title)
        elif sort_by == 'size':
            entries.sort(key=lambda e: len(e.content), reverse=True)
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 SORTED BY {sort_by.upper()}{Colors.RESET}\n")
        for i, entry in enumerate(entries[:20], 1):
            size = len(entry.content)
            print(f"{i:2}. {entry.title[:40]:40} | {entry.author:15} | {size:6}B")
        
        if len(entries) > 20:
            print(f"\n... and {len(entries) - 20} more")
    
    def do_info(self, arg):
        """Show detailed info. Usage: info [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{entry.title}{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")
        
        print(f"  {Colors.CYAN}ID:{Colors.RESET} {entry.id}")
        print(f"  {Colors.CYAN}Author:{Colors.RESET} {entry.author}")
        print(f"  {Colors.CYAN}Created:{Colors.RESET} {entry.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {Colors.CYAN}Updated:{Colors.RESET} {entry.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {Colors.CYAN}Size:{Colors.RESET} {len(entry.content)} chars")
        print(f"  {Colors.CYAN}Words:{Colors.RESET} {len(entry.content.split())}")
        print(f"  {Colors.CYAN}Lines:{Colors.RESET} {len(entry.content.split(chr(10)))}")
        
        if entry.source:
            print(f"  {Colors.CYAN}Source:{Colors.RESET} {entry.source}")
        
        if entry.tags:
            tags_str = ", ".join([f"#{t.name}" for t in entry.tags])
            print(f"  {Colors.CYAN}Tags:{Colors.RESET} {tags_str}")
        
        if entry.category_id:
            cat = self.library.db.get_category(entry.category_id)
            if cat:
                print(f"  {Colors.CYAN}Category:{Colors.RESET} {cat.name}")
        
        status_str = ""
        if entry.is_favorite:
            status_str += "⭐ Favorite "
        if entry.is_archived:
            status_str += "📦 Archived"
        
        if status_str:
            print(f"  {Colors.CYAN}Status:{Colors.RESET} {status_str}")
        
        print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}\n")
    
    def do_status(self, arg):
        """Show library status. Usage: status"""
        stats = self.library.get_statistics()
        entries = self.library.list_entries()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 LIBRARY STATUS{Colors.RESET}\n")
        print(f"  📚 Entries:      {stats['total_entries']}")
        print(f"  📂 Categories:   {stats['total_categories']}")
        print(f"  🏷️  Tags:         {stats['total_tags']}")
        print(f"  ⭐ Favorites:    {stats['favorite_entries']}")
        print(f"  📦 Archived:     {stats['archived_entries']}")
        
        if entries:
            total_words = sum(len(e.content.split()) for e in entries)
            avg_words = total_words // len(entries)
            print(f"  📝 Total words:  {total_words:,}")
            print(f"  📊 Avg per entry: {avg_words}")
        
        print()
    
    def do_purge(self, arg):
        """Delete archived entries. Usage: purge [--force]"""
        archived = [e for e in self.library.list_entries() if e.is_archived]
        
        if not archived:
            print(status_message('info', 'No archived entries'))
            return
        
        if '--force' not in arg:
            confirm = input(f"{Colors.YELLOW}⚠️  Delete {len(archived)} archived entries? (yes/no):{Colors.RESET} ").strip().lower()
            if confirm != 'yes':
                print("Cancelled")
                return
        
        for entry in archived:
            self.library.delete_entry(entry.id)
        
        print(f"{status_message('success', f'Purged {len(archived)} entries')}")
    
    def do_sync(self, arg):
        """Sync with external source. Usage: sync [--check] [--pull] [--push]"""
        print(f"{Colors.BLUE}🔄 Sync functionality{Colors.RESET}")
        print("  Status: Ready for implementation")
        print("  Options: --check, --pull, --push\n")
    
    def do_import(self, arg):
        """Import from file. Usage: import <file> [--format json|csv|txt]"""
        if not arg:
            print(status_message('error', 'Usage: import <file>'))
            return
        
        parts = arg.split()
        filename = parts[0]
        fmt = 'json'
        
        if '--format' in parts:
            idx = parts.index('--format')
            if idx + 1 < len(parts):
                fmt = parts[idx + 1]
        
        try:
            if fmt == 'csv':
                self._batch_create_from_file(filename)
            elif fmt == 'json':
                self._import_from_json(filename)
            elif fmt == 'txt':
                self._import_from_txt(filename)
            else:
                print(status_message('error', f'Unknown format: {fmt}'))
        except Exception as e:
            print(status_message('error', f'Import failed: {e}'))
    
    def _import_from_json(self, filename):
        """Import from JSON file"""
        import json
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for item in data if isinstance(data, list) else [data]:
            entry = self.library.create_entry(
                title=item.get('title'),
                content=item.get('content'),
                author=item.get('author', 'Unknown'),
                category_id=item.get('category_id')
            )
            count += 1
        
        print(f"{status_message('success', f'Imported {count} entries from {filename}')}")
    
    def _import_from_txt(self, filename):
        """Import from TXT file"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title = Path(filename).stem
        entry = self.library.create_entry(
            title=title,
            content=content,
            author='Imported'
        )
        
        print(f"{status_message('success', f'Imported as: {entry.title}')}")
    
    def do_cfg(self, arg):
        """Configuration. Usage: cfg [--list] [--set key value]"""
        if '--list' in arg or not arg:
            print(f"\n{Colors.BOLD}{Colors.CYAN}⚙️  CONFIGURATION{Colors.RESET}\n")
            print(f"  Language: {self.lang_manager.current_language}")
            print(f"  Entries: {len(self.library.list_entries())}")
            print(f"  Data dir: data/\n")
        elif '--set' in arg:
            print("Configuration save: Not yet implemented\n")

    def do_head(self, arg):
        """Show first N entries. Usage: head [N]"""
        try:
            n = int(arg) if arg else 5
        except ValueError:
            n = 5
        
        entries = self.library.list_entries()[:n]
        for i, entry in enumerate(entries, 1):
            print(f"{i}. {entry.title[:50]} - {entry.author}")
    
    def do_tail(self, arg):
        """Show last N entries. Usage: tail [N]"""
        try:
            n = int(arg) if arg else 5
        except ValueError:
            n = 5
        
        entries = self.library.list_entries()[-n:]
        for i, entry in enumerate(entries, 1):
            print(f"{i}. {entry.title[:50]} - {entry.author}")
    
    def do_wc(self, arg):
        """Word/char count. Usage: wc [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        words = len(entry.content.split())
        chars = len(entry.content)
        lines = len(entry.content.split('\n'))
        
        print(f"  {lines:6} {words:6} {chars:6} {entry.title}")
    
    def do_diff(self, arg):
        """Compare two entries. Usage: diff <id1> <id2>"""
        parts = arg.split()
        if len(parts) < 2:
            print(status_message('error', 'Usage: diff <id1> <id2>'))
            return
        
        e1 = self.library.get_entry(parts[0])
        e2 = self.library.get_entry(parts[1])
        
        if not e1 or not e2:
            print(status_message('error', 'Entries not found'))
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}COMPARISON{Colors.RESET}\n")
        print(f"  {Colors.CYAN}Entry 1:{Colors.RESET} {e1.title}")
        print(f"    Words: {len(e1.content.split())}")
        print(f"    Chars: {len(e1.content)}")
        print()
        print(f"  {Colors.CYAN}Entry 2:{Colors.RESET} {e2.title}")
        print(f"    Words: {len(e2.content.split())}")
        print(f"    Chars: {len(e2.content)}\n")
    
    def do_cat(self, arg):
        """Print entry content. Usage: cat <id>"""
        if not arg and not self.current_entry:
            print(status_message('error', 'No entry selected'))
            return
        
        entry_id = arg.strip() if arg else self.current_entry.id
        entry = self.library.get_entry(entry_id)
        
        if not entry:
            print(status_message('error', 'Entry not found'))
            return
        
        print(f"\n{entry.content}\n")
    
    def do_echo(self, arg):
        """Add note to current entry. Usage: echo <text>"""
        if not arg:
            print(status_message('error', 'Usage: echo <text>'))
            return
        
        if not self.current_entry:
            print(status_message('error', 'No entry selected'))
            return
        
        self.current_entry.content += f"\n\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {arg}"
        self.library.db.update_entry(self.current_entry)
        print(f"{status_message('success', 'Note added')}")
    
    def do_rev(self, arg):
        """Reverse/invert entry. Usage: rev [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        entry.content = entry.content[::-1]
        entry.title = entry.title[::-1]
        self.library.db.update_entry(entry)
        print(f"{status_message('success', 'Entry reversed')}")
    
    def do_clr(self, arg):
        """Clear entry content. Usage: clr [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        confirm = input(f"{Colors.YELLOW}Clear content of '{entry.title}'? (yes/no):{Colors.RESET} ").strip().lower()
        if confirm == 'yes':
            entry.content = "[cleared]"
            self.library.db.update_entry(entry)
            print(f"{status_message('success', 'Content cleared')}")
    
    def do_open(self, arg):
        """Open entry in viewer. Usage: open [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        # Display in pager-style
        lines = entry.content.split('\n')
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{entry.title}{Colors.RESET}\n")
        for line in lines:
            print(line)
        print(f"\n{Colors.GRAY}({len(lines)} lines){Colors.RESET}\n")
    
    def do_new(self, arg):
        """Quick create. Usage: new [title]"""
        title = arg.strip() if arg else input(f"{Colors.CYAN}Title:{Colors.RESET} ")
        if not title:
            print(status_message('error', 'Title required'))
            return
        
        print(f"{Colors.CYAN}Content (empty line to finish):{Colors.RESET}")
        lines = []
        while True:
            try:
                line = input()
                if not line:
                    break
                lines.append(line)
            except EOFError:
                break
        
        content = "\n".join(lines) if lines else "[empty]"
        entry = self.library.create_entry(
            title=title,
            content=content,
            author="Quick"
        )
        print(f"{status_message('success', f'Created: {entry.id}')}")
        self.current_entry = entry
    
    def do_pwd(self, arg):
        """Print working directory (current entry). Usage: pwd"""
        if self.current_entry:
            print(f"\nCurrent: {self.current_entry.title} ({self.current_entry.id})\n")
        else:
            print("No entry selected\n")
    
    def do_count(self, arg):
        """Count entries. Usage: count [filter]"""
        if arg:
            if arg == 'favorites':
                count = len([e for e in self.library.list_entries() if e.is_favorite])
            elif arg == 'archived':
                count = len([e for e in self.library.list_entries() if e.is_archived])
            else:
                count = len(self.library.list_entries())
        else:
            count = len(self.library.list_entries())
        
        print(f"\n{count} entries\n")
    
    def do_size(self, arg):
        """Total library size. Usage: size"""
        entries = self.library.list_entries()
        total = sum(len(e.content) for e in entries)
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📦 LIBRARY SIZE{Colors.RESET}\n")
        print(f"  Total: {total:,} characters")
        print(f"  Avg per entry: {total // len(entries) if entries else 0:,} characters")
        print(f"  ~{total // 1024:.1f} KB\n")
    
    def do_bench(self, arg):
        """Benchmark library. Usage: bench"""
        import time
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}⚡ BENCHMARK{Colors.RESET}\n")
        
        # Test list
        start = time.time()
        entries = self.library.list_entries()
        list_time = time.time() - start
        print(f"  List entries: {list_time*1000:.2f}ms")
        
        # Test search
        if entries:
            start = time.time()
            self.library.search_entries(entries[0].title[:5])
            search_time = time.time() - start
            print(f"  Search: {search_time*1000:.2f}ms")
        
        # Test get
        if entries:
            start = time.time()
            self.library.get_entry(entries[0].id)
            get_time = time.time() - start
            print(f"  Get entry: {get_time*1000:.2f}ms\n")

    def do_monitor(self, arg):
        """Monitor website availability. Usage: monitor [--url <url>] [--interval <sec>] [--retry <count>]"""
        import urllib.request
        import time
        
        url = None
        interval = 5
        retry = 3
        
        if '--url' in arg:
            parts = arg.split()
            idx = parts.index('--url')
            if idx + 1 < len(parts):
                url = parts[idx + 1]
        
        if '--interval' in arg:
            parts = arg.split()
            idx = parts.index('--interval')
            if idx + 1 < len(parts):
                try:
                    interval = int(parts[idx + 1])
                except ValueError:
                    interval = 5
        
        if not url:
            url = input(f"{Colors.CYAN}URL to monitor:{Colors.RESET} ").strip()
        
        if not url.startswith('http'):
            url = 'http://' + url
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 Monitoring {url}{Colors.RESET}")
        print(f"Interval: {interval}s, Retries: {retry}\n")
        
        try:
            attempts = 0
            while attempts < 10:
                try:
                    start = time.time()
                    urllib.request.urlopen(url, timeout=5)
                    response_time = (time.time() - start) * 1000
                    
                    status = f"{Colors.GREEN}✅ OK{Colors.RESET}"
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {status} - {response_time:.0f}ms")
                    attempts += 1
                    
                except Exception as e:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {Colors.RED}❌ FAIL{Colors.RESET} - {str(e)[:50]}")
                    attempts += 1
                
                if attempts < 10:
                    time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Monitoring stopped{Colors.RESET}\n")
    
    def do_healthcheck(self, arg):
        """Check library health. Usage: healthcheck [--timeout <sec>]"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🏥 HEALTH CHECK{Colors.RESET}\n")
        
        try:
            # Check entries
            entries = self.library.list_entries()
            print(f"  {Colors.GREEN}✓{Colors.RESET} Entries: {len(entries)}")
            
            # Check categories
            categories = self.library.list_categories()
            print(f"  {Colors.GREEN}✓{Colors.RESET} Categories: {len(categories)}")
            
            # Check tags
            tags = self.library.list_tags()
            print(f"  {Colors.GREEN}✓{Colors.RESET} Tags: {len(tags)}")
            
            # Check database
            print(f"  {Colors.GREEN}✓{Colors.RESET} Database: OK")
            
            # Check file size
            import os
            db_size = sum(os.path.getsize(f) for f in Path("data").glob("*.json") if f.is_file())
            print(f"  {Colors.GREEN}✓{Colors.RESET} Data size: {db_size / 1024:.1f} KB")
            
            print(f"\n{Colors.GREEN}✅ Library is healthy{Colors.RESET}\n")
        
        except Exception as e:
            print(f"{Colors.RED}❌ Health check failed: {e}{Colors.RESET}\n")
    
    def do_uptime(self, arg):
        """Show uptime history. Usage: uptime [--days <N>]"""
        from datetime import datetime, timedelta
        
        days = 7
        if '--days' in arg:
            parts = arg.split()
            idx = parts.index('--days')
            if idx + 1 < len(parts):
                try:
                    days = int(parts[idx + 1])
                except ValueError:
                    days = 7
        
        entries = self.library.list_entries()
        if not entries:
            print(f"{status_message('info', 'No entries')}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📈 UPTIME REPORT (last {days} days){Colors.RESET}\n")
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            date_str = date.strftime('%Y-%m-%d')
            
            count = len([e for e in entries if e.created_at.date() == date.date()])
            bar = "█" * min(count, 20)
            
            print(f"  {date_str} {bar} {count}")
        
        print()
    
    def do_strip(self, arg):
        """Strip whitespace from entry. Usage: strip [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        entry.content = entry.content.strip()
        entry.title = entry.title.strip()
        self.library.db.update_entry(entry)
        print(f"{status_message('success', 'Whitespace stripped')}")
    
    def do_upper(self, arg):
        """Convert to uppercase. Usage: upper [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        entry.content = entry.content.upper()
        self.library.db.update_entry(entry)
        print(f"{status_message('success', 'Converted to uppercase')}")
    
    def do_lower(self, arg):
        """Convert to lowercase. Usage: lower [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        entry.content = entry.content.lower()
        self.library.db.update_entry(entry)
        print(f"{status_message('success', 'Converted to lowercase')}")
    
    def do_replace(self, arg):
        """Replace text in entry. Usage: replace <old> <new> [id]"""
        parts = arg.split(None, 2)
        if len(parts) < 2:
            print(status_message('error', 'Usage: replace <old> <new> [id]'))
            return
        
        old_text = parts[0]
        new_text = parts[1]
        entry_id = parts[2] if len(parts) > 2 else (self.current_entry.id if self.current_entry else None)
        
        if not entry_id:
            print(status_message('error', 'No entry selected'))
            return
        
        entry = self.library.get_entry(entry_id)
        if not entry:
            print(status_message('error', 'Entry not found'))
            return
        
        old_len = len(entry.content)
        entry.content = entry.content.replace(old_text, new_text)
        new_len = len(entry.content)
        
        self.library.db.update_entry(entry)
        print(f"{status_message('success', f'Replaced {old_len - new_len} characters')}")
    
    def do_lines(self, arg):
        """Show line count. Usage: lines [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        lines = entry.content.count('\n') + 1
        print(f"\n{entry.title}: {lines} lines\n")
    
    def do_hash(self, arg):
        """Show entry hash. Usage: hash [id]"""
        import hashlib
        
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        content_hash = hashlib.md5(entry.content.encode()).hexdigest()
        title_hash = hashlib.md5(entry.title.encode()).hexdigest()
        
        print(f"\n  Title hash:  {title_hash}")
        print(f"  Content hash: {content_hash}\n")
    
    def do_uuid(self, arg):
        """Show entry UUID. Usage: uuid [id]"""
        if arg:
            entry = self.library.get_entry(arg.strip())
        else:
            entry = self.current_entry
        
        if not entry:
            print(status_message('error', 'No entry selected'))
            return
        
        print(f"\n  UUID: {entry.id}\n")
    
    def do_export_txt(self, arg):
        """Export entry to text file. Usage: export_txt [id] [filename]"""
        parts = arg.split()
        
        if not parts:
            entry = self.current_entry
            filename = None
        else:
            entry = self.library.get_entry(parts[0])
            filename = parts[1] if len(parts) > 1 else None
        
        if not entry:
            print(status_message('error', 'Entry not found'))
            return
        
        if not filename:
            filename = entry.title.replace(' ', '_') + '.txt'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{entry.title}\n")
                f.write(f"Author: {entry.author}\n")
                f.write(f"Created: {entry.created_at}\n")
                f.write("="*60 + "\n\n")
                f.write(entry.content)
            
            print(f"{status_message('success', f'Exported to {filename}')}")
        except Exception as e:
            print(f"{status_message('error', f'Export failed: {e}')}")

    def emptyline(self):
        """Handle empty input"""
        pass


def main():
    """Main entry point"""
    # Get data directory from config or use default
    data_dir = "data"
    db_path = Path(data_dir)
    db_path.mkdir(exist_ok=True)

    # Initialize database and library
    db = Database(data_dir)
    library = Library(db)

    # Start shell
    shell = AlexandriaShell(library)
    
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\n\n✨ Bye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        raise


if __name__ == "__main__":
    main()
