import subprocess
import sys
from ctypes import windll, byref, c_uint, Structure, POINTER, cast
from ctypes.wintypes import HANDLE, DWORD, BYTE

import loguru


class SID_AND_ATTRIBUTES(Structure):
    _fields_ = [("Sid", POINTER(c_uint)),
                ("Attributes", DWORD)]


class TOKEN_MANDATORY_LABEL(Structure):
    _fields_ = [("Label", SID_AND_ATTRIBUTES)]


class PermissionStrategy:
    def elevate(self) -> bool:
        raise NotImplementedError("Elevate method must be implemented")


class TokenIntegrityLevelStrategy(PermissionStrategy):
    def elevate(self) -> bool:
        try:
            SECURITY_MANDATORY_HIGH_RID = 0x00003000
            TOKEN_QUERY = 0x0008
            TOKEN_MANDATORY_LABEL_TYPE = 25

            token_handle = HANDLE()
            if not windll.advapi32.OpenProcessToken(windll.kernel32.GetCurrentProcess(), TOKEN_QUERY,
                                                    byref(token_handle)):
                loguru.logger.error("TokenIntegrityLevelStrategy: OpenProcessToken failed")
                return False

            size_needed = DWORD()
            windll.advapi32.GetTokenInformation(token_handle, TOKEN_MANDATORY_LABEL_TYPE, None, 0, byref(size_needed))

            buffer = (BYTE * size_needed.value)()
            if not windll.advapi32.GetTokenInformation(token_handle, TOKEN_MANDATORY_LABEL_TYPE, buffer,
                                                       size_needed.value, byref(size_needed)):
                loguru.logger.error("TokenIntegrityLevelStrategy: GetTokenInformation failed")
                return False

            token_mandatory_label = cast(buffer, POINTER(TOKEN_MANDATORY_LABEL)).contents
            sub_authority_count = windll.advapi32.GetSidSubAuthorityCount(token_mandatory_label.Label.Sid)[0]
            sub_authority = cast(
                windll.advapi32.GetSidSubAuthority(token_mandatory_label.Label.Sid, sub_authority_count - 1),
                POINTER(DWORD)).contents

            loguru.logger.debug(f"TokenIntegrityLevelStrategy: Integrity level: {sub_authority.value}")
            return sub_authority.value >= SECURITY_MANDATORY_HIGH_RID
        except Exception:
            loguru.logger.debug("TokenIntegrityLevelStrategy: Failed to elevate permission")
            return False


class ShellExecuteStrategy(PermissionStrategy):
    def elevate(self) -> bool:
        try:
            if windll.shell32.IsUserAnAdmin():
                loguru.logger.debug("ShellExecuteStrategy: Already have admin permission")
                return True

            params = [sys.executable] + sys.argv
            proc_info = windll.shell32.ShellExecuteW(None, "runas", params[0], " ".join(params[1:]), None, 1)
            loguru.logger.debug(f"ShellExecuteStrategy: Process info: {proc_info}")
            return proc_info > 32
        except Exception:
            loguru.logger.debug("ShellExecuteStrategy: Failed to elevate permission")
            return False


class UACStrategy(PermissionStrategy):
    def elevate(self) -> bool:
        try:
            result = subprocess.run(["net", "session"], capture_output=True, text=True)
            if "Access is denied" not in result.stderr:
                loguru.logger.debug("UACStrategy: Already have admin permission")
                return True

            subprocess.run(["powershell", "Start-Process", sys.executable, "-Verb", "runAs"], shell=True)
            loguru.logger.debug("UACStrategy: Elevate permission successfully")
            return False
        except Exception:
            loguru.logger.debug("UACStrategy: Failed to elevate permission")
            return False


class Permission:
    def __init__(self):
        self._strategies = [
            TokenIntegrityLevelStrategy(),
            ShellExecuteStrategy(),
            UACStrategy()
        ]

    def update_to_admin_permission(self) -> bool:
        loguru.logger.debug("Trying to update to admin permission")
        return any(strategy.elevate() for strategy in self._strategies)


if __name__ == "__main__":
    perm = Permission()
    if perm.update_to_admin_permission():
        print("权限已提升")
    else:
        print("无法提升权限")
