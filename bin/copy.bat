@echo off
setlocal enabledelayedexpansion

:: 锁文件路径
set "lockfile=%TEMP%\getpaths.lock"

:wait_for_lock
:: 检查是否存在锁文件
if exist "%lockfile%" (
    timeout /t 1 /nobreak >nul
    goto wait_for_lock
)

:: 创建锁文件
echo Locked > "%lockfile%"

:: 获取当前剪贴板内容
for /f "usebackq tokens=* delims=" %%a in (`powershell Get-Clipboard`) do set "clipContent=%%a"

:: 如果剪贴板内容以 [QuickMklink] 开头，则保留它，否则清空变量
if /i "!clipContent:~0,12!"=="[QuickMklink" (
    set "output=!clipContent!"
) else (
    set "output="
)

:: 获取当前文件路径并添加 [QuickMklink] 标签
set "filePath=%~1"
set "output=!output![QuickMklinkCopy]"!filePath!"[/QuickMklinkCopy]"

:: 将新的内容复制回剪贴板
echo !output! | clip

:: 删除锁文件以允许下一个脚本实例运行
del "%lockfile%"

endlocal
