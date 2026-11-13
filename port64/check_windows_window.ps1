param([string]$Game,[string]$Disk,[string]$Font,[string]$Save)
$ErrorActionPreference='Stop'
if (!$Game -or !$Disk -or !$Font -or !$Save) { throw 'Supply -Game EXE -Disk HDI -Font BMP -Save NEW_DIRECTORY' }
if (Test-Path $Save) { throw 'Choose a fresh private save directory' }
Add-Type -TypeDefinition @'
using System;
using System.Text;
using System.Runtime.InteropServices;
using System.Threading;
public class TH03DesktopSmoke {
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct STARTUPINFO {
  public int cb;public string reserved,desktop,title;public int x,y,xsize,ysize,xchars,ychars,fill,flags;public short show,reserved2;public IntPtr reservedPointer,input,output,error;
 }
 [StructLayout(LayoutKind.Sequential)] struct PROCESSINFO {public IntPtr process,thread;public uint pid,tid;}
 [StructLayout(LayoutKind.Sequential)] struct RECT {public int left,top,right,bottom;}
 delegate bool EnumWindow(IntPtr window,IntPtr unused);
 [DllImport("user32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr CreateDesktop(string name,IntPtr device,IntPtr mode,int flags,uint access,IntPtr security);
 [DllImport("user32.dll")] static extern bool CloseDesktop(IntPtr desktop);
 [DllImport("user32.dll")] static extern bool EnumDesktopWindows(IntPtr desktop,EnumWindow callback,IntPtr unused);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr window,out uint pid);
 [DllImport("user32.dll")] static extern bool GetClientRect(IntPtr window,out RECT rect);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetClassName(IntPtr window,StringBuilder text,int count);
 [DllImport("user32.dll")] static extern bool PostMessage(IntPtr window,uint message,IntPtr w,IntPtr l);
 [DllImport("user32.dll")] static extern bool SetWindowPos(IntPtr window,IntPtr after,int x,int y,int width,int height,uint flags);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern bool CreateProcess(string name,StringBuilder command,IntPtr psec,IntPtr tsec,bool inherit,uint flags,IntPtr environment,string directory,ref STARTUPINFO startup,out PROCESSINFO process);
 [DllImport("kernel32.dll")] static extern uint WaitForSingleObject(IntPtr handle,uint milliseconds);
 [DllImport("kernel32.dll")] static extern bool GetExitCodeProcess(IntPtr process,out uint code);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
 [DllImport("kernel32.dll")] static extern bool GetProcessAffinityMask(IntPtr process,out UIntPtr mask,out UIntPtr system);
 [DllImport("kernel32.dll")] static extern bool SetProcessAffinityMask(IntPtr process,UIntPtr mask);
 public static string Run(string game,string disk,string font,string save) {
  string name="TH03-test-"+Guid.NewGuid().ToString("N");IntPtr desktop=CreateDesktop(name,IntPtr.Zero,IntPtr.Zero,0,0x1ff,IntPtr.Zero);
  if(desktop==IntPtr.Zero)throw new Exception("CreateDesktop: "+Marshal.GetLastWin32Error());
  PROCESSINFO process=new PROCESSINFO();IntPtr window=IntPtr.Zero;
  try {
   STARTUPINFO startup=new STARTUPINFO();startup.cb=Marshal.SizeOf(startup);startup.desktop=name;
   string args="\""+game+"\" --hdi \""+disk+"\" --font-bmp \""+font+"\" --save-dir \""+save+"\" --mute --frames 600";
   if(!CreateProcess(game,new StringBuilder(args),IntPtr.Zero,IntPtr.Zero,false,0x08004000,IntPtr.Zero,null,ref startup,out process))throw new Exception("CreateProcess: "+Marshal.GetLastWin32Error());
   UIntPtr allowed,system;if(GetProcessAffinityMask(process.process,out allowed,out system)){ulong a=allowed.ToUInt64();SetProcessAffinityMask(process.process,new UIntPtr(a&(~a+1)));}
   for(int retry=0;retry<100&&window==IntPtr.Zero;retry++) {
    EnumDesktopWindows(desktop,delegate(IntPtr candidate,IntPtr unused){uint pid;GetWindowThreadProcessId(candidate,out pid);StringBuilder cls=new StringBuilder(64);GetClassName(candidate,cls,64);if(pid==process.pid&&cls.ToString()=="TH03Port64")window=candidate;return true;},IntPtr.Zero);
    if(WaitForSingleObject(process.process,50)==0)break;
   }
   if(window==IntPtr.Zero)throw new Exception("native window was not created on private desktop");
   RECT before,after;GetClientRect(window,out before);
   SetWindowPos(window,IntPtr.Zero,0,0,1000,700,0x14);Thread.Sleep(350);GetClientRect(window,out after);
   if(after.right<=0||after.bottom<=0||before.right==after.right&&before.bottom==after.bottom)throw new Exception("window resize failed");
   PostMessage(window,0x10,IntPtr.Zero,IntPtr.Zero);
   if(WaitForSingleObject(process.process,15000)!=0)throw new Exception("WM_CLOSE did not stop native window");
   uint exit;GetExitCodeProcess(process.process,out exit);if(exit!=0)throw new Exception("native window exit "+exit);
   return "Native private-desktop window created, resized from "+before.right+"x"+before.bottom+" to "+after.right+"x"+after.bottom+", and closed normally; pid "+process.pid;
  } finally {
   if(process.process!=IntPtr.Zero){if(WaitForSingleObject(process.process,0)!=0&&window!=IntPtr.Zero)PostMessage(window,0x10,IntPtr.Zero,IntPtr.Zero);WaitForSingleObject(process.process,15000);CloseHandle(process.thread);CloseHandle(process.process);}CloseDesktop(desktop);
  }
 }
}
'@
[TH03DesktopSmoke]::Run($Game,$Disk,$Font,$Save)
if (!(Test-Path (Join-Path $Save 'YUME.CFG'))) { throw 'native GUI did not save configuration on close' }
