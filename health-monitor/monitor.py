import time

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from alerts import log_alert, overall_status, play_sound, status_for
from checks import get_system_stats, scan_open_ports

REFRESH_SECONDS = 3

STATUS_COLORS = {"ok": "green", "warning": "yellow", "critical": "red"}
VIBE_LINES = {
    "ok": "All systems chill. Nothing to see here.",
    "warning": "Getting a little warm in here...",
    "critical": "Uh oh. Someone wake up the on-call.",
}

console = Console()


def build_dashboard(stats: dict, ports: list, status: str) -> Panel:
    stats_table = Table(title="System Vitals", expand=True)
    stats_table.add_column("Metric")
    stats_table.add_column("Value")
    stats_table.add_column("Status")

    for name, value in stats.items():
        metric_status = status_for(value)
        color = STATUS_COLORS[metric_status]
        stats_table.add_row(name.upper(), f"{value:.1f}%", Text(metric_status.upper(), style=color))

    ports_table = Table(title="Open Ports (localhost)", expand=True)
    ports_table.add_column("Port")
    ports_table.add_column("Service")
    if ports:
        for port, service in ports:
            ports_table.add_row(str(port), service)
    else:
        ports_table.add_row("-", "No common ports open")

    header = Text(f"HEALTH MONITOR  |  {time.strftime('%H:%M:%S')}", style="bold")
    vibe = Text(VIBE_LINES[status], style=STATUS_COLORS[status])

    body = Table.grid(expand=True)
    body.add_row(header)
    body.add_row(vibe)
    body.add_row(stats_table)
    body.add_row(ports_table)

    return Panel(body, border_style=STATUS_COLORS[status], title="VIBE STATE: ACTIVE")


def main():
    last_status = None
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            stats = get_system_stats()
            ports = scan_open_ports()
            status = overall_status(stats)

            live.update(build_dashboard(stats, ports, status))

            if status != last_status:
                play_sound(status)
                if status != "ok":
                    log_alert(f"Status changed to {status.upper()} — {stats}")
                last_status = status

            time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold]Health monitor stopped.[/bold]")
