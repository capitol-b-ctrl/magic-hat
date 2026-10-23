"""Unit tests for Magic Hat submodules and root capability checks."""

from magic_hat.modules.base import is_root, check_tsu
from magic_hat.tools import (
    handle_nmap_menu,
    handle_net_shark,
    handle_web_fuzzer,
    handle_dns_recon,
    handle_tech_fingerprint,
    handle_subnet_sweep,
    handle_hydra_audit,
    handle_ssh_audit,
    handle_powershell_audit,
    handle_hash_identifier,
    handle_exploit_search,
    handle_wireless_recon,
    handle_wireless_bt_scanner,
    handle_monitor_mode,
    handle_bluetooth_recon,
    handle_bluetooth_attacks,
    handle_payload_generator,
    handle_qr_exploit,
    handle_crypto_engine,
    handle_global_target_manager,
    handle_binary_diagnostics,
    handle_webhook_config,
    handle_quick_shell,
    handle_wordlist_manager,
    handle_view_logs
)


def test_root_checks_return_bool():
    """Verify is_root and check_tsu return valid booleans."""
    assert isinstance(is_root(), bool)
    assert isinstance(check_tsu(), bool)


def test_modules_exported_as_callables():
    """Verify all major tool handlers are callable functions."""
    handlers = [
        handle_nmap_menu,
        handle_net_shark,
        handle_web_fuzzer,
        handle_dns_recon,
        handle_tech_fingerprint,
        handle_subnet_sweep,
        handle_hydra_audit,
        handle_ssh_audit,
        handle_powershell_audit,
        handle_hash_identifier,
        handle_exploit_search,
        handle_wireless_recon,
        handle_wireless_bt_scanner,
        handle_monitor_mode,
        handle_bluetooth_recon,
        handle_bluetooth_attacks,
        handle_payload_generator,
        handle_qr_exploit,
        handle_crypto_engine,
        handle_global_target_manager,
        handle_binary_diagnostics,
        handle_webhook_config,
        handle_quick_shell,
        handle_wordlist_manager,
        handle_view_logs
    ]
    for handler in handlers:
        assert callable(handler)
