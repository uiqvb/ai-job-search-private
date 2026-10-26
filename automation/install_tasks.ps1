# Register the scheduled job-search tasks in Windows Task Scheduler.
#
#   powershell -ExecutionPolicy Bypass -File automation\install_tasks.ps1            # create or update
#   powershell -ExecutionPolicy Bypass -File automation\install_tasks.ps1 -Remove    # delete them
#
# Jobs run overnight; ntfy holds the pushes until 07:30 (config "deliver_at").
# Each task fires at its night time (WakeToRun, StartWhenAvailable) AND 2 min after sign-in or
# unlock, because wake timers don't work on this laptop and the catch-up is unreliable after
# hibernate (checked 2026-10-25). automation/daily.py skips a job already done today.
# Tasks run as the logged-on user, because claude.exe uses that user's login.

param([switch]$Remove)

$Repo   = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\python.exe"
$Folder = "\JobSearch\"
$User   = "$env:USERDOMAIN\$env:USERNAME"
$UnlockClass = Get-CimClass -Namespace ROOT\Microsoft\Windows\TaskScheduler -ClassName MSFT_TaskSessionStateChangeTrigger

$Jobs = @(
    @{ Name = "gmail_sync";      At = "01:00"; Days = 1; Args = "automation\run_job.py gmail_sync";  Limit = 50 },
    @{ Name = "scrape";          At = "03:00"; Days = 1; Args = "automation\run_job.py scrape";      Limit = 70 },
    @{ Name = "event_reminders"; At = "05:00"; Days = 1; Args = "automation\event_reminders.py";      Limit = 5 }
)

foreach ($j in $Jobs) {
    if ($Remove) {
        Unregister-ScheduledTask -TaskPath $Folder -TaskName $j.Name -Confirm:$false -ErrorAction SilentlyContinue
        Write-Host "removed $($j.Name)"
        continue
    }
    $action   = New-ScheduledTaskAction -Execute $Python -Argument $j.Args -WorkingDirectory $Repo
    $daily    = New-ScheduledTaskTrigger -Daily -DaysInterval $j.Days -At $j.At
    $logon    = New-ScheduledTaskTrigger -AtLogOn -User $User
    $logon.Delay = "PT2M"
    $unlock   = New-CimInstance -CimClass $UnlockClass -ClientOnly
    $unlock.StateChange = 8   # TASK_SESSION_UNLOCK
    $unlock.UserId = $User
    $unlock.Delay = "PT2M"
    $trigger  = @($daily, $logon, $unlock)
    $settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable `
                  -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
                  -ExecutionTimeLimit (New-TimeSpan -Minutes $j.Limit) -MultipleInstances IgnoreNew
    $principal = New-ScheduledTaskPrincipal -UserId $User -LogonType Interactive -RunLevel Limited
    Register-ScheduledTask -TaskPath $Folder -TaskName $j.Name -Action $action -Trigger $trigger `
        -Settings $settings -Principal $principal -Force | Out-Null
    Write-Host "registered $($j.Name) every $($j.Days) day(s) at $($j.At), plus at sign-in and unlock"
}
