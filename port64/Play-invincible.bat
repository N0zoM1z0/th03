@echo off
setlocal
set "TH03_PATCH_BAT=%~f0"
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "$text=[IO.File]::ReadAllText($env:TH03_PATCH_BAT); $mark=':__TH03_PS__'; Invoke-Expression $text.Substring($text.LastIndexOf($mark)+$mark.Length)"
if errorlevel 1 (
  echo No-hit launch failed. The game files were not patched.
  pause
  exit /b 1
)
exit /b 0
:__TH03_PS__
$ErrorActionPreference = 'Stop'
$source = @'
using System;
using System.Diagnostics;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Runtime.InteropServices;
public static class Th03RuntimeNoHit {
 public const string SupportedHash="78568d9d0716c94a28a121ae1f0f38d5003f11af4493695fb448bdd1848c77fe";
 const int CollisionHitRva=0x43240;
 static readonly byte[] Prologue={0x41,0x57,0x41,0x56,0x41,0x55,0x41,0x54,0x55,0x57,0x56,0x53,0x48,0x81,0xec,0x88,0,0,0};
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] struct Start {
  public int size;public string reserved,desktop,title;public int x,y,width,height,columns,rows,fill,flags;
  public short show,reservedSize;public IntPtr reservedPointer,input,output,error;
 }
 [StructLayout(LayoutKind.Sequential)] struct Child {public IntPtr process,thread;public uint pid,tid;}
 [StructLayout(LayoutKind.Sequential)] struct Basic {public IntPtr reserved,peb,r1,r2,pid,parent;}
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern bool CreateProcess(string exe,StringBuilder args,IntPtr pa,IntPtr ta,bool inherit,uint flags,IntPtr env,string cwd,ref Start startup,out Child child);
 [DllImport("ntdll.dll")] static extern int NtQueryInformationProcess(IntPtr process,int kind,out Basic info,uint size,out uint returned);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool ReadProcessMemory(IntPtr p,IntPtr at,byte[] data,UIntPtr size,out UIntPtr read);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool WriteProcessMemory(IntPtr p,IntPtr at,byte[] data,UIntPtr size,out UIntPtr written);
 [DllImport("kernel32.dll",SetLastError=true)] static extern IntPtr VirtualAllocEx(IntPtr p,IntPtr at,UIntPtr size,uint allocation,uint protection);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool VirtualProtectEx(IntPtr p,IntPtr at,UIntPtr size,uint protection,out uint old);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool FlushInstructionCache(IntPtr p,IntPtr at,UIntPtr size);
 [DllImport("kernel32.dll",SetLastError=true)] static extern uint ResumeThread(IntPtr thread);
 [DllImport("kernel32.dll")] static extern bool TerminateProcess(IntPtr p,uint code);
 [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr handle);
 static void Require(bool ok,string why){if(!ok)throw new Exception(why+" (Win32 "+Marshal.GetLastWin32Error()+")");}
 public static string Hash(string path){using(var hash=SHA256.Create())using(var stream=File.OpenRead(path))return BitConverter.ToString(hash.ComputeHash(stream)).Replace("-","").ToLowerInvariant();}
 static byte[] Read(IntPtr p,IntPtr at,int size){var data=new byte[size];UIntPtr count;Require(ReadProcessMemory(p,at,data,new UIntPtr((uint)size),out count)&&count.ToUInt64()==(ulong)size,"Process read");return data;}
 static void Write(IntPtr p,IntPtr at,byte[] data){UIntPtr count;Require(WriteProcessMemory(p,at,data,new UIntPtr((uint)data.Length),out count)&&count.ToUInt64()==(ulong)data.Length,"Process write");Require(BitConverter.ToString(Read(p,at,data.Length))==BitConverter.ToString(data),"Patch readback");}
 static byte[] Jump(long address){var code=new byte[12];code[0]=0x48;code[1]=0xb8;Array.Copy(BitConverter.GetBytes(address),0,code,2,8);code[10]=0xff;code[11]=0xe0;return code;}
 static void Apply(IntPtr process,long image){
  var entry=new IntPtr(image+CollisionHitRva);
  Require(BitConverter.ToString(Read(process,entry,Prologue.Length))==BitConverter.ToString(Prologue),"Unsupported CollisionMap.hit instructions");
  // Patch CollisionMap::hit: player_hit is inlined in player_update.
  // Win64 hidden optional<Point> result is RCX; the Player reference is R9.
  // Human: clear is_hit (Player+6), return an empty optional (result+4),
  // and return its address in RAX. CPU: replay the 19-byte prologue unchanged.
  // The displaced pushes/sub have no relative operands; all four args survive.
  byte[] gate={0x41,0x80,0x79,0x05,0,0x75,0x0d,0x41,0xc6,0x41,0x06,0,0xc6,0x41,0x04,0,0x48,0x89,0xc8,0xc3};
  var stub=new byte[gate.Length+Prologue.Length+12];Array.Copy(gate,stub,gate.Length);Array.Copy(Prologue,0,stub,gate.Length,Prologue.Length);Array.Copy(Jump(entry.ToInt64()+Prologue.Length),0,stub,gate.Length+Prologue.Length,12);
  var memory=VirtualAllocEx(process,IntPtr.Zero,new UIntPtr((uint)stub.Length),0x3000,4);Require(memory!=IntPtr.Zero,"Allocate owned trampoline");Write(process,memory,stub);
  uint old;Require(VirtualProtectEx(process,memory,new UIntPtr((uint)stub.Length),0x20,out old),"Protect trampoline");Require(FlushInstructionCache(process,memory,new UIntPtr((uint)stub.Length)),"Trampoline instruction cache");
  var patch=new byte[Prologue.Length];for(int i=0;i<patch.Length;i++)patch[i]=0x90;Array.Copy(Jump(memory.ToInt64()),patch,12);
  Require(VirtualProtectEx(process,entry,new UIntPtr((uint)patch.Length),0x40,out old),"Protect owned entry");
  try{Write(process,entry,patch);Require(FlushInstructionCache(process,entry,new UIntPtr((uint)patch.Length)),"Entry instruction cache");}
  finally{uint ignored;Require(VirtualProtectEx(process,entry,new UIntPtr((uint)patch.Length),old,out ignored),"Restore entry protection");}
 }
 public static Process Launch(string exe,string arguments,string directory,string desktop){
  Require(Environment.Is64BitProcess,"64-bit PowerShell is required");
  Require(Hash(exe)==SupportedHash,"Unsupported th03-port64.exe; this BAT targets preview-4");
  var start=new Start();start.size=Marshal.SizeOf(typeof(Start));start.desktop=desktop;Child child;
  Require(CreateProcess(exe,new StringBuilder(Quote(exe)+" "+arguments),IntPtr.Zero,IntPtr.Zero,false,0x08000004,IntPtr.Zero,directory,ref start,out child),"Create owned suspended game");
  bool resumed=false;
  try{
   Basic basic;uint size;Require(NtQueryInformationProcess(child.process,0,out basic,(uint)Marshal.SizeOf(typeof(Basic)),out size)==0,"Read owned PEB");
   long image=BitConverter.ToInt64(Read(child.process,new IntPtr(basic.peb.ToInt64()+16),8),0);Require(Read(child.process,new IntPtr(image),2)[0]==0x4d,"Owned image header");
   Require(Hash(exe)==SupportedHash,"Executable changed during launch");Apply(child.process,image);
   var result=Process.GetProcessById((int)child.pid);var keepHandle=result.Handle;
   Require(ResumeThread(child.thread)!=0xffffffff,"Resume no-hit game");resumed=true;return result;
  }finally{if(!resumed)TerminateProcess(child.process,1);CloseHandle(child.thread);CloseHandle(child.process);}
 }
 public static string Quote(string value){if(value.IndexOf('"')>=0||value.IndexOf('\n')>=0||value.IndexOf('\r')>=0)throw new ArgumentException("Invalid path");return "\""+value+"\"";}
}
'@
Add-Type -TypeDefinition $source
# Launch only a new process; the EXE, HDI and normal saves remain untouched.
$directory = [IO.Path]::GetDirectoryName($env:TH03_PATCH_BAT)
foreach ($file in @('th03-port64.exe','th03.hdi','FREECG98.BMP','ym2608_adpcm_rom.bin')) {
    if (!(Test-Path -LiteralPath (Join-Path $directory $file))) { throw "Missing $file beside this BAT." }
}
$gameArguments = '--hdi ' + [Th03RuntimeNoHit]::Quote((Join-Path $directory 'th03.hdi')) + ' --font-bmp ' + [Th03RuntimeNoHit]::Quote((Join-Path $directory 'FREECG98.BMP')) + ' --save-dir ' + [Th03RuntimeNoHit]::Quote((Join-Path $directory 'save-invincible')) + ' --audio --pmd-driver pmd86 --opna-rom ' + [Th03RuntimeNoHit]::Quote((Join-Path $directory 'ym2608_adpcm_rom.bin'))
$game = [Th03RuntimeNoHit]::Launch((Join-Path $directory 'th03-port64.exe'),$gameArguments,$directory,$null)
Write-Host ('Human-player no-hit patch active. PID ' + $game.Id + '; saves: save-invincible')
$game.Dispose()
