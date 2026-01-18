"""
Color and style utilities for Alexandria CLI
"""

class Colors:
    """ANSI color codes"""
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'
    BG_BLUE = '\033[104m'
    BG_MAGENTA = '\033[105m'
    BG_CYAN = '\033[106m'
    BG_WHITE = '\033[107m'
    
    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'
    
    # Combined styles
    SUCCESS = GREEN + BOLD
    ERROR = RED + BOLD
    WARNING = YELLOW + BOLD
    INFO = BLUE + BOLD
    ACCENT = CYAN + BOLD


def colorize(text, color, style=''):
    """Apply color to text"""
    return f"{color}{style}{text}{Colors.RESET}"


def banner():
    """Display Alexandria banner"""
    banner_text = f"""{Colors.BOLD}{Colors.CYAN}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          {Colors.MAGENTA}█████  ██      ███████ ██     ██{Colors.CYAN} ║
    ║          {Colors.MAGENTA}██    ██ ██       ██     ██     ██{Colors.CYAN} ║
    ║          {Colors.MAGENTA}█████  ██  ██      ██     ██     ██{Colors.CYAN} ║
    ║          {Colors.MAGENTA}██    ██    ██     ██     ██     ██{Colors.CYAN} ║
    ║          {Colors.MAGENTA}██    ██     ██    ██      ███████ {Colors.CYAN} ║
    ║                                                           ║
    ║         🏛️  Knowledge & Information Management System   ║
    ║                                                           ║
    ║              A Sophisticated Library Database             ║
    ║           Inspired by CyberStalker's Alexandria          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    return banner_text


def separator(length=60, char='═'):
    """Create a separator line"""
    return f"{Colors.CYAN}{char * length}{Colors.RESET}"


def section_header(title):
    """Create a section header"""
    return f"\n{Colors.BOLD}{Colors.MAGENTA}▶ {title}{Colors.RESET}\n"


def entry_item(title, author, date, is_favorite=False, is_archived=False):
    """Format an entry item"""
    marker = f"{Colors.YELLOW}⭐{Colors.RESET}" if is_favorite else "  "
    archived = f"{Colors.RED}[ARCHIVED]{Colors.RESET} " if is_archived else ""
    return f"{marker} {Colors.BOLD}{title}{Colors.RESET} {archived}\n   {Colors.CYAN}Author:{Colors.RESET} {author} | {Colors.CYAN}Created:{Colors.RESET} {date}"


def help_command(cmd, description, usage=''):
    """Format a help command"""
    cmd_colored = f"{Colors.GREEN}{cmd}{Colors.RESET}"
    desc_colored = f"{Colors.WHITE}{description}{Colors.RESET}"
    result = f"  {cmd_colored:<20} - {desc_colored}"
    if usage:
        result += f"\n                     {Colors.CYAN}Usage: {usage}{Colors.RESET}"
    return result


def status_message(status, message):
    """Create a status message"""
    if status == 'success':
        return f"{Colors.GREEN}✅{Colors.RESET} {Colors.GREEN}{message}{Colors.RESET}"
    elif status == 'error':
        return f"{Colors.RED}❌{Colors.RESET} {Colors.RED}{message}{Colors.RESET}"
    elif status == 'warning':
        return f"{Colors.YELLOW}⚠️ {Colors.RESET}{Colors.YELLOW}{message}{Colors.RESET}"
    elif status == 'info':
        return f"{Colors.BLUE}ℹ️ {Colors.RESET}{Colors.BLUE}{message}{Colors.RESET}"
    else:
        return f"  {message}"


def table(headers, rows, colors_per_col=None):
    """Create a colored table"""
    if not rows:
        return "No data to display"
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build table
    lines = []
    
    # Header
    header_line = "│ "
    for i, h in enumerate(headers):
        header_line += f"{Colors.BOLD}{h:<{col_widths[i]}}{Colors.RESET} │ "
    lines.append(f"{Colors.CYAN}┌─ {Colors.RESET}{header_line.rstrip()}")
    
    # Separator
    sep = "├─"
    for w in col_widths:
        sep += "─" * (w + 2) + "┼─"
    lines.append(f"{Colors.CYAN}{sep.rstrip()}{Colors.RESET}")
    
    # Rows
    for row in rows:
        row_line = "│ "
        for i, cell in enumerate(row):
            cell_str = str(cell)
            if colors_per_col and i < len(colors_per_col):
                cell_str = f"{colors_per_col[i]}{cell_str}{Colors.RESET}"
            row_line += f"{cell_str:<{col_widths[i]}} │ "
        lines.append(row_line)
    
    # Footer
    lines.append(f"{Colors.CYAN}└─{Colors.RESET}")
    
    return "\n".join(lines)


def progress_bar(current, total, width=30, title='Progress'):
    """Create a progress bar"""
    if total == 0:
        percent = 100
    else:
        percent = int((current / total) * 100)
    
    filled = int((percent / 100) * width)
    bar = f"{Colors.GREEN}{'█' * filled}{Colors.RESET}{Colors.GRAY}{'░' * (width - filled)}{Colors.RESET}"
    
    return f"{Colors.CYAN}{title}:{Colors.RESET} {bar} {percent}%"


# Additional color codes
Colors.GRAY = '\033[90m'
Colors.LIGHT_GRAY = '\033[37m'

__all__ = [
    'Colors',
    'colorize',
    'banner',
    'separator',
    'section_header',
    'entry_item',
    'help_command',
    'status_message',
    'table',
    'progress_bar',
]
