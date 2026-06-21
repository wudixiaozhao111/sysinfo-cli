#!/usr/bin/env python3
"""
SysInfo CLI - System Information Monitor for Linux Servers
Pure command-line, no desktop required, supports all Linux distributions
"""
import sys
import os
import time
import platform
import psutil
from datetime import datetime

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    
    # Light colors
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


def clear_screen():
    """Clear the screen"""
    print('\033[2J\033[H', end='')


def move_cursor(x, y):
    """Move cursor to specified position"""
    print(f'\033[{y};{x}H', end='')


def format_bytes(bytes_val):
    """Format byte count to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


def get_uptime():
    """Get system uptime"""
    uptime_seconds = time.time() - psutil.boot_time()
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    
    return ' '.join(parts)


def get_distro_name():
    """Get distribution name"""
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if line.startswith('PRETTY_NAME='):
                    return line.split('=')[1].strip().strip('"')
    except:
        pass
    return platform.system()


def draw_progress_bar(percent, width=30, color=Colors.GREEN):
    """Draw a progress bar"""
    filled = int(width * percent / 100)
    bar = '█' * filled + '░' * (width - filled)
    
    # Change color based on usage
    if percent >= 90:
        bar_color = Colors.RED
    elif percent >= 70:
        bar_color = Colors.YELLOW
    else:
        bar_color = color
    
    return f"{bar_color}{bar}{Colors.RESET}"


def draw_box(title, content_lines, width=60):
    """Draw a box with border"""
    lines = []
    
    # Top border
    top = f"{Colors.LIGHT_BLUE}╔{'═' * (width - 2)}╗{Colors.RESET}"
    lines.append(top)
    
    # Title
    title_line = f"{Colors.LIGHT_BLUE}║{Colors.RESET} {Colors.BOLD}{Colors.LIGHT_CYAN}{title}{Colors.RESET}"
    title_padding = width - len(title) - 3
    lines.append(title_line + ' ' * title_padding + f"{Colors.LIGHT_BLUE}║{Colors.RESET}")
    
    # Separator
    separator = f"{Colors.LIGHT_BLUE}╠{'═' * (width - 2)}╣{Colors.RESET}"
    lines.append(separator)
    
    # Content
    for line in content_lines:
        visible_len = len(line)
        content_line = f"{Colors.LIGHT_BLUE}║{Colors.RESET} {line}"
        padding = width - visible_len - 3
        if padding < 0:
            padding = 0
        lines.append(content_line + ' ' * padding + f"{Colors.LIGHT_BLUE}║{Colors.RESET}")
    
    # Bottom border
    bottom = f"{Colors.LIGHT_BLUE}╚{'═' * (width - 2)}╝{Colors.RESET}"
    lines.append(bottom)
    
    return '\n'.join(lines)


def show_system_info():
    """Display system information"""
    clear_screen()
    
    # Title - compact, 100 chars wide
    print(f"""
{Colors.BOLD}{Colors.LIGHT_CYAN}
  ╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
  ║  ⚡ SysInfo CLI - System Monitor                                          Server Edition v1.0.0  ║
  ╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
""")
    
    # System information
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu_count = psutil.cpu_count(logical=True)
    cpu_physical = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    
    # Warm up CPU percent measurement
    psutil.cpu_percent(interval=0.1)
    cpu_usage = psutil.cpu_percent(interval=None)
    
    # Left column: System + CPU
    left_col = []
    left_col.append(f"{Colors.BOLD}{Colors.LIGHT_BLUE}┌─ System ──────────────────────────────────────────┐{Colors.RESET}")
    
    distro = get_distro_name()
    if len(distro) > 38:
        distro = distro[:35] + "..."
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}OS:{Colors.RESET}       {Colors.GREEN}{distro:<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    
    kernel = platform.release()
    if len(kernel) > 38:
        kernel = kernel[:35] + "..."
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Kernel:{Colors.RESET}   {Colors.WHITE}{kernel:<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    
    hostname = platform.node()
    if len(hostname) > 38:
        hostname = hostname[:35] + "..."
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Hostname:{Colors.RESET} {Colors.WHITE}{hostname:<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Arch:{Colors.RESET}     {Colors.WHITE}{platform.machine():<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Uptime:{Colors.RESET}   {Colors.YELLOW}{get_uptime():<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Time:{Colors.RESET}     {Colors.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    left_col.append(f"{Colors.LIGHT_BLUE}└───────────────────────────────────────────────────┘{Colors.RESET}")
    
    left_col.append("")
    left_col.append(f"{Colors.BOLD}{Colors.LIGHT_BLUE}┌─ CPU ─────────────────────────────────────────────┐{Colors.RESET}")
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Cores:{Colors.RESET}    {Colors.GREEN}{cpu_physical} physical / {cpu_count} logical{Colors.RESET}")
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Freq:{Colors.RESET}     {Colors.WHITE}{cpu_freq.current:.2f} MHz{Colors.RESET}" if cpu_freq else f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Freq:{Colors.RESET}     {Colors.WHITE}N/A{Colors.RESET}")
    
    cpu_bar = draw_progress_bar(cpu_usage, 22, Colors.RED)
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Usage:{Colors.RESET}    {cpu_bar} {Colors.BOLD}{cpu_usage:.1f}%{Colors.RESET}")
    
    cpu_model = platform.processor() or 'Unknown'
    if len(cpu_model) > 38:
        cpu_model = cpu_model[:35] + "..."
    left_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Model:{Colors.RESET}    {Colors.WHITE}{cpu_model:<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    left_col.append(f"{Colors.LIGHT_BLUE}└───────────────────────────────────────────────────┘{Colors.RESET}")
    
    # Right column: Memory + Swap
    right_col = []
    right_col.append(f"{Colors.BOLD}{Colors.LIGHT_BLUE}┌─ Memory ─────────────────────────────────────────┐{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Total:{Colors.RESET}    {Colors.GREEN}{format_bytes(mem.total):<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Used:{Colors.RESET}     {Colors.YELLOW}{format_bytes(mem.used):<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Free:{Colors.RESET}     {Colors.CYAN}{format_bytes(mem.available):<41}{Colors.RESET}{Colors.LIGHT_BLUE}│{Colors.RESET}")
    
    mem_bar = draw_progress_bar(mem.percent, 25)
    right_col.append(f"{Colors.LIGHT_BLUE}│{Colors.RESET} {Colors.GRAY}Usage:{Colors.RESET}    {mem_bar} {Colors.BOLD}{mem.percent:.1f}%{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_BLUE}└───────────────────────────────────────────────────┘{Colors.RESET}")
    
    right_col.append("")
    right_col.append(f"{Colors.BOLD}{Colors.LIGHT_MAGENTA}┌─ Swap ───────────────────────────────────────────┐{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_MAGENTA}│{Colors.RESET} {Colors.GRAY}Total:{Colors.RESET}    {Colors.GREEN}{format_bytes(swap.total):<41}{Colors.RESET}{Colors.LIGHT_MAGENTA}│{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_MAGENTA}│{Colors.RESET} {Colors.GRAY}Used:{Colors.RESET}     {Colors.YELLOW}{format_bytes(swap.used):<41}{Colors.RESET}{Colors.LIGHT_MAGENTA}│{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_MAGENTA}│{Colors.RESET} {Colors.GRAY}Free:{Colors.RESET}     {Colors.CYAN}{format_bytes(swap.free):<41}{Colors.RESET}{Colors.LIGHT_MAGENTA}│{Colors.RESET}")
    
    swap_bar = draw_progress_bar(swap.percent, 25, Colors.MAGENTA)
    right_col.append(f"{Colors.LIGHT_MAGENTA}│{Colors.RESET} {Colors.GRAY}Usage:{Colors.RESET}    {swap_bar} {Colors.BOLD}{swap.percent:.1f}%{Colors.RESET}")
    right_col.append(f"{Colors.LIGHT_MAGENTA}└───────────────────────────────────────────────────┘{Colors.RESET}")
    
    # Two column layout - total ~108 chars wide
    max_lines = max(len(left_col), len(right_col))
    
    for i in range(max_lines):
        line = "  "
        
        # Left column (52 chars)
        if i < len(left_col) and left_col[i]:
            line += left_col[i]
            # Pad to 52 visible chars
            visible = len(left_col[i].replace('\033[', '').replace('m', '').replace('0123456789;', ''))
            # Simple padding
            line += " " * (52 - len(left_col[i]))
        else:
            line += " " * 52
        
        line += "  "
        
        # Right column (52 chars)
        if i < len(right_col) and right_col[i]:
            line += right_col[i]
        else:
            line += " " * 52
        
        print(line)
    
    # Disk section
    print()
    print(f"  {Colors.BOLD}{Colors.LIGHT_YELLOW}💾 Disk Usage{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 100}{Colors.RESET}")
    print(f"  {Colors.GRAY}{'Device':<14} {'Mount':<22} {'Total':<10} {'Used':<10} {'Free':<10} {'Usage':<28}{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 100}{Colors.RESET}")
    
    # Skip virtual filesystems
    skip_fs = ['proc', 'sysfs', 'devtmpfs', 'devpts', 'tmpfs', 'cgroup', 
               'cgroup2', 'pstore', 'bpf', 'tracefs', 'securityfs',
               'debugfs', 'hugetlbfs', 'mqueue', 'autofs', 'fusectl',
               'configfs', 'binfmt_misc', 'rpc_pipefs']
    
    for partition in psutil.disk_partitions(all=True):
        # Skip virtual filesystems
        if partition.fstype in skip_fs:
            continue
        # Skip read-only and pseudo mounts
        if 'ro' in partition.opts and 'rw' not in partition.opts:
            continue
            
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            # Skip zero-size filesystems
            if usage.total == 0:
                continue
                
            bar = draw_progress_bar(usage.percent, 18, Colors.YELLOW)
            
            device = partition.device
            if len(device) > 13:
                device = device[:10] + "..."
            
            mount = partition.mountpoint
            if len(mount) > 21:
                mount = mount[:18] + "..."
            
            print(f"  {Colors.CYAN}{device:<14}{Colors.RESET} {Colors.WHITE}{mount:<22}{Colors.RESET} {format_bytes(usage.total):<10} {Colors.YELLOW}{format_bytes(usage.used):<10}{Colors.RESET} {Colors.GREEN}{format_bytes(usage.free):<10}{Colors.RESET} {bar} {Colors.BOLD}{usage.percent:.1f}%{Colors.RESET}")
        except:
            pass
    
    # Network section
    print()
    print(f"  {Colors.BOLD}{Colors.LIGHT_MAGENTA}🌐 Network Interfaces{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 100}{Colors.RESET}")
    print(f"  {Colors.GRAY}{'Interface':<14} {'IP Address':<18} {'Sent':<14} {'Received':<14} {'Packets':<16}{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 100}{Colors.RESET}")
    
    net_io = psutil.net_io_counters(pernic=True)
    addrs = psutil.net_if_addrs()
    
    for iface, addr_list in addrs.items():
        ip = "N/A"
        for addr in addr_list:
            if addr.family == 2:  # AF_INET
                ip = addr.address
                break
        
        if iface in net_io:
            io = net_io[iface]
            iface_name = iface
            if len(iface_name) > 13:
                iface_name = iface_name[:10] + "..."
            
            print(f"  {Colors.CYAN}{iface_name:<14}{Colors.RESET} {Colors.WHITE}{ip:<18}{Colors.RESET} {Colors.GREEN}{format_bytes(io.bytes_sent):<14}{Colors.RESET} {Colors.YELLOW}{format_bytes(io.bytes_recv):<14}{Colors.RESET} {io.packets_sent + io.packets_recv}")
    
    print()
    print(f"  {Colors.GRAY}💡 Keys: 1=System Info  2=Realtime Monitor  3=Processes  q=Quit{Colors.RESET}")
    print()


def show_realtime_monitor():
    """Realtime monitoring mode"""
    clear_screen()
    
    # Initialize network data
    last_net_io = psutil.net_io_counters()
    last_time = time.time()
    
    try:
        while True:
            clear_screen()
            
            current_time = time.time()
            time_diff = current_time - last_time
            
            print(f"""
{Colors.BOLD}{Colors.LIGHT_GREEN}
  ╔══════════════════════════════════════════════════════════════╗
  ║           📈  SysInfo CLI - Realtime Monitor                ║
  ║                Server Edition v1.0.0                        ║
  ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
            """)
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=None)
            cpu_percents = psutil.cpu_percent(interval=None, percpu=True)
            
            print(f"  {Colors.BOLD}{Colors.LIGHT_RED}⚡ CPU Usage{Colors.RESET}")
            print(f"  {Colors.GRAY}{'─' * 80}{Colors.RESET}")
            
            # Overall CPU
            cpu_bar = draw_progress_bar(cpu_percent, 50, Colors.RED)
            print(f"  Total: {cpu_bar} {Colors.BOLD}{cpu_percent:.1f}%{Colors.RESET}")
            print()
            
            # Each core
            print(f"  {Colors.GRAY}Per Core:{Colors.RESET}")
            for i, pct in enumerate(cpu_percents):
                bar = draw_progress_bar(pct, 30, Colors.RED)
                core_num = f"CPU{i:2d}"
                print(f"  {Colors.CYAN}{core_num}{Colors.RESET}: {bar} {pct:5.1f}%", end='')
                if (i + 1) % 2 == 0:
                    print()
                else:
                    print("   ", end='')
            
            print()
            print()
            
            # Memory
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            print(f"  {Colors.BOLD}{Colors.LIGHT_GREEN}💾 Memory Usage{Colors.RESET}")
            print(f"  {Colors.GRAY}{'─' * 80}{Colors.RESET}")
            
            mem_bar = draw_progress_bar(mem.percent, 60, Colors.GREEN)
            print(f"  Memory: {mem_bar} {Colors.BOLD}{mem.percent:.1f}%{Colors.RESET}")
            print(f"  {Colors.GRAY}Used: {format_bytes(mem.used)} / Total: {format_bytes(mem.total)} / Free: {format_bytes(mem.available)}{Colors.RESET}")
            print()
            
            swap_bar = draw_progress_bar(swap.percent, 60, Colors.MAGENTA)
            print(f"  Swap: {swap_bar} {Colors.BOLD}{swap.percent:.1f}%{Colors.RESET}")
            print(f"  {Colors.GRAY}Used: {format_bytes(swap.used)} / Total: {format_bytes(swap.total)}{Colors.RESET}")
            print()
            
            # System load
            try:
                load1, load5, load15 = os.getloadavg()
                print(f"  {Colors.BOLD}{Colors.LIGHT_YELLOW}📊 System Load{Colors.RESET}")
                print(f"  {Colors.GRAY}{'─' * 80}{Colors.RESET}")
                print(f"  1min: {Colors.CYAN}{load1:.2f}{Colors.RESET}   5min: {Colors.YELLOW}{load5:.2f}{Colors.RESET}   15min: {Colors.GREEN}{load15:.2f}{Colors.RESET}")
                print()
            except:
                pass
            
            # Network traffic
            current_net_io = psutil.net_io_counters()
            if time_diff > 0:
                sent_speed = (current_net_io.bytes_sent - last_net_io.bytes_sent) / time_diff
                recv_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / time_diff
                
                print(f"  {Colors.BOLD}{Colors.LIGHT_CYAN}🌐 Network Traffic{Colors.RESET}")
                print(f"  {Colors.GRAY}{'─' * 80}{Colors.RESET}")
                print(f"  📤 Upload Speed: {Colors.GREEN}{format_bytes(sent_speed)}/s{Colors.RESET}")
                print(f"  📥 Download Speed: {Colors.YELLOW}{format_bytes(recv_speed)}/s{Colors.RESET}")
                print(f"  {Colors.GRAY}Total Sent: {format_bytes(current_net_io.bytes_sent)} / Total Received: {format_bytes(current_net_io.bytes_recv)}{Colors.RESET}")
                print()
            
            last_net_io = current_net_io
            last_time = current_time
            
            # Disk IO
            disk_io = psutil.disk_io_counters()
            if disk_io:
                print(f"  {Colors.BOLD}{Colors.LIGHT_MAGENTA}💿 Disk IO{Colors.RESET}")
                print(f"  {Colors.GRAY}{'─' * 80}{Colors.RESET}")
                print(f"  Read: {format_bytes(disk_io.read_bytes)}   Write: {format_bytes(disk_io.write_bytes)}")
                print(f"  Read Count: {disk_io.read_count}   Write Count: {disk_io.write_count}")
                print()
            
            print(f"  {Colors.GRAY}💡 Press Ctrl+C to return to main menu{Colors.RESET}")
            print()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        return


def show_processes():
    """Process management"""
    clear_screen()
    
    print(f"""
{Colors.BOLD}{Colors.LIGHT_MAGENTA}
  ╔══════════════════════════════════════════════════════════════╗
  ║           📊  SysInfo CLI - Process Manager                 ║
  ║                Server Edition v1.0.0                        ║
  ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    # Get process list
    processes = []
    total_processes = 0
    running = 0
    sleeping = 0
    other = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info', 'status', 'username']):
        try:
            p = proc.info
            total_processes += 1
            
            if p['status'] == psutil.STATUS_RUNNING:
                running += 1
            elif p['status'] == psutil.STATUS_SLEEPING:
                sleeping += 1
            else:
                other += 1
            
            processes.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    
    # Process statistics
    print(f"  {Colors.BOLD}Process Statistics:{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 80}{Colors.RESET}")
    print(f"  Total: {Colors.CYAN}{total_processes}{Colors.RESET}   Running: {Colors.GREEN}{running}{Colors.RESET}   Sleeping: {Colors.YELLOW}{sleeping}{Colors.RESET}   Other: {other}")
    print()
    
    # Process list
    print(f"  {Colors.BOLD}Process List (sorted by CPU%, top 30):{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 100}{Colors.RESET}")
    print(f"  {Colors.GRAY}{'PID':<8} {'Name':<25} {'CPU%':<8} {'MEM%':<8} {'Memory':<12} {'Status':<12} {'User':<15}{Colors.RESET}")
    print(f"  {Colors.GRAY}{'─' * 100}{Colors.RESET}")
    
    for p in processes[:30]:
        pid = p['pid']
        name = p['name'] or 'Unknown'
        cpu_pct = p['cpu_percent'] or 0.0
        mem_pct = p['memory_percent'] or 0.0
        mem_bytes = p['memory_info'].rss if p['memory_info'] else 0
        status = p['status'] or 'unknown'
        user = p['username'] or 'unknown'
        
        # Truncate long names
        if len(name) > 24:
            name = name[:21] + '...'
        if len(user) > 14:
            user = user[:11] + '...'
        
        # High CPU in red
        cpu_color = Colors.RED if cpu_pct > 50 else Colors.GREEN if cpu_pct < 10 else Colors.YELLOW
        
        print(f"  {Colors.CYAN}{pid:<8}{Colors.RESET} {Colors.WHITE}{name:<25}{Colors.RESET} {cpu_color}{cpu_pct:<8.1f}{Colors.RESET} {Colors.YELLOW}{mem_pct:<8.1f}{Colors.RESET} {format_bytes(mem_bytes):<12} {status:<12} {user:<15}")
    
    print()
    print(f"  {Colors.GRAY}💡 Press r=Refresh  q=Return to main menu{Colors.RESET}")
    print()


def print_help():
    """Print help information"""
    print(f"""
{Colors.BOLD}{Colors.LIGHT_CYAN}
  ╔══════════════════════════════════════════════════════════════╗
  ║           ⚡  SysInfo CLI - System Monitor                  ║
  ║                Server Edition v1.0.0                        ║
  ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}

  {Colors.BOLD}Usage:{Colors.RESET} sysinfo-cli [options]

  {Colors.BOLD}Options:{Colors.RESET}
    {Colors.GREEN}-h, --help{Colors.RESET}       Show this help message
    {Colors.GREEN}-v, --version{Colors.RESET}    Show version information
    {Colors.GREEN}-s, --system{Colors.RESET}     Show system information (default)
    {Colors.GREEN}-m, --monitor{Colors.RESET}    Realtime monitoring mode
    {Colors.GREEN}-p, --process{Colors.RESET}    Process manager

  {Colors.BOLD}Interactive Mode Keys:{Colors.RESET}
    {Colors.CYAN}1{Colors.RESET}  System Information
    {Colors.CYAN}2{Colors.RESET}  Realtime Monitor
    {Colors.CYAN}3{Colors.RESET}  Process Manager
    {Colors.CYAN}q{Colors.RESET}  Quit

  {Colors.BOLD}Examples:{Colors.RESET}
    sysinfo-cli              {Colors.GRAY}# Show system info{Colors.RESET}
    sysinfo-cli -m           {Colors.GRAY}# Start realtime monitor{Colors.RESET}
    sysinfo-cli -p           {Colors.GRAY}# Show process manager{Colors.RESET}

  {Colors.BOLD}Supported Distributions:{Colors.RESET}
    Ubuntu, Debian, Fedora, CentOS, Arch, Manjaro, openSUSE, etc.

  {Colors.BOLD}License:{Colors.RESET} MIT
  {Colors.BOLD}Repository:{Colors.RESET} https://github.com/sysinfo/sysinfo-cli
""")


def print_version():
    """Print version information"""
    print("SysInfo CLI v1.0.0")
    print("System Information Monitor for Linux Servers")
    print("License: MIT")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='SysInfo CLI - System Information Monitor for Linux Servers',
        add_help=False
    )
    parser.add_argument('-h', '--help', action='store_true', help='Show help message')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    parser.add_argument('-s', '--system', action='store_true', help='Show system information')
    parser.add_argument('-m', '--monitor', action='store_true', help='Realtime monitoring mode')
    parser.add_argument('-p', '--process', action='store_true', help='Process manager')
    
    args = parser.parse_args()
    
    if args.help:
        print_help()
        return
    
    if args.version:
        print_version()
        return
    
    # If specific mode selected
    if args.monitor:
        show_realtime_monitor()
        return
    
    if args.process:
        show_processes()
        # Wait for user input
        try:
            while True:
                choice = input(f"  {Colors.BOLD}{Colors.LIGHT_CYAN}Select function [r/q]: {Colors.RESET}").strip().lower()
                if choice == 'r':
                    show_processes()
                elif choice == 'q':
                    print(f"\n  {Colors.GREEN}Goodbye! 👋{Colors.RESET}\n")
                    break
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Colors.GREEN}Goodbye! 👋{Colors.RESET}\n")
        return
    
    if args.system:
        show_system_info()
        return
    
    # Default: interactive mode
    while True:
        show_system_info()
        
        try:
            choice = input(f"  {Colors.BOLD}{Colors.LIGHT_CYAN}Select function [1/2/3/q]: {Colors.RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Colors.GREEN}Goodbye! 👋{Colors.RESET}\n")
            break
        
        if choice == '1':
            show_system_info()
        elif choice == '2':
            show_realtime_monitor()
        elif choice == '3':
            show_processes()
            try:
                while True:
                    sub_choice = input(f"  {Colors.BOLD}{Colors.LIGHT_CYAN}Select function [r/q]: {Colors.RESET}").strip().lower()
                    if sub_choice == 'r':
                        show_processes()
                    elif sub_choice == 'q':
                        break
            except (EOFError, KeyboardInterrupt):
                break
        elif choice == 'q':
            print(f"\n  {Colors.GREEN}Goodbye! 👋{Colors.RESET}\n")
            break
        else:
            print(f"  {Colors.YELLOW}Invalid option, please try again{Colors.RESET}")
            time.sleep(1)


if __name__ == '__main__':
    main()
