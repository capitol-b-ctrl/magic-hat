"""Magic Hat operational modules package."""

from magic_hat.modules.base import (
    is_root,
    check_tsu,
    require_root,
    print_target_context,
    select_target_interactive,
    parse_open_ports,
    parse_nmap_deep_telemetry
)

from magic_hat.modules.recon import (
    handle_nmap_menu,
    handle_net_shark,
    handle_web_fuzzer,
    handle_dns_recon,
    handle_tech_fingerprint,
    handle_subnet_sweep
)

from magic_hat.modules.auditing import (
    handle_hydra_audit,
    handle_ssh_audit,
    handle_powershell_audit,
    handle_hash_identifier,
    handle_exploit_search
)

from magic_hat.modules.wireless import (
    handle_wireless_recon,
    handle_wireless_bt_scanner,
    handle_monitor_mode,
    handle_bluetooth_recon,
    handle_bluetooth_attacks
)

from magic_hat.modules.payloads import (
    handle_payload_generator,
    handle_qr_exploit,
    handle_crypto_engine
)

from magic_hat.modules.system import (
    handle_global_target_manager,
    handle_binary_diagnostics,
    handle_webhook_config,
    handle_quick_shell,
    handle_wordlist_manager,
    handle_view_logs
)

__all__ = [
    "is_root",
    "check_tsu",
    "require_root",
    "print_target_context",
    "select_target_interactive",
    "parse_open_ports",
    "parse_nmap_deep_telemetry",
    "handle_nmap_menu",
    "handle_net_shark",
    "handle_web_fuzzer",
    "handle_dns_recon",
    "handle_tech_fingerprint",
    "handle_subnet_sweep",
    "handle_hydra_audit",
    "handle_ssh_audit",
    "handle_powershell_audit",
    "handle_hash_identifier",
    "handle_exploit_search",
    "handle_wireless_recon",
    "handle_wireless_bt_scanner",
    "handle_monitor_mode",
    "handle_bluetooth_recon",
    "handle_bluetooth_attacks",
    "handle_payload_generator",
    "handle_qr_exploit",
    "handle_crypto_engine",
    "handle_global_target_manager",
    "handle_binary_diagnostics",
    "handle_webhook_config",
    "handle_quick_shell",
    "handle_wordlist_manager",
    "handle_view_logs"
]
